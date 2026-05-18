import bisect
import os
import json
import traceback
import sys
from typing import *

BOT_NAME = "MyBot"
BOT_AVATAR = "robot_1"

# 1. Direct path resolution
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BOT_DIR, 'data')
LOG_FILE = os.path.join(BOT_DIR, "debug.log")

def log(message):
    """Logs to stderr (for sandbox/runner) and debug.log (for local)."""
    msg = str(message)
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()
    try:
        with open(LOG_FILE, "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass

# Initialize log file
try:
    with open(LOG_FILE, "w") as f:
        f.write("--- MATCH START ---\n")
except Exception:
    pass

RANGES = {}
if os.path.exists(DATA_DIR):
    for fn in os.listdir(DATA_DIR):
        if fn.endswith('.json'):
            scenario = fn.split('.')[0]
            path = os.path.join(DATA_DIR, fn)
            try:
                if os.path.getsize(path) > 0:
                    with open(path) as f:
                        RANGES[scenario] = json.load(f)
                else:
                    log(f"WARNING: Skipping empty data file: {fn}")
            except Exception as e:
                log(f"ERROR: Could not load {fn}: {e}")


def log_state(game_state):
    log(f"HandID : {game_state.get('hand_id','')} | Street : {game_state.get('street','')} | Hand : {cards_to_key(game_state.get('your_cards',[]))} | Stack : {get_stack_as_bb(game_state)}")


###### STACK_BINS must be ascending for bisect to work
STACK_BINS = [8, 10, 12, 15, 20, 25, 30, 40, 60, 100]
PREFLOP_ORDER = ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
POSTFLOP_ORDER = ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']

RFI_SIZES = {
    'UTG': 2.5,
    'HJ':  2.5,
    'CO':  2.25,
    'BTN': 2.0,
    'SB':  3.0,
}

def cards_to_key(cards: List[str]) -> str:
    # Guard against empty hand arrays sent during showdowns
    if not cards or len(cards) < 2:
        return "None"
        
    # Converts ['As', 'Kh'] -> 'AKo', ['8s', '8h'] -> '88'
    ranks = "23456789TJQKA"
    r1, s1 = cards[0][0], cards[0][1]
    r2, s2 = cards[1][0], cards[1][1]
    
    i1, i2 = ranks.index(r1), ranks.index(r2)
    if i1 < i2:
        r1, r2, s1, s2 = r2, r1, s2, s1
        
    if r1 == r2:
        return r1 + r2
    
    suited = "s" if s1 == s2 else "o"
    return r1 + r2 + suited

def get_position_name(game_state: dict,seat_no:int):
    num_players = len(game_state['players'])
    try:
        sb_seat = next(a['seat'] for a in game_state['action_log'] if a['action'] == 'small_blind')
    except (StopIteration, KeyError):
        return "Unknown"
    
    btn_seat = sb_seat if num_players == 2 else (sb_seat - 1) % num_players
    dist = (seat_no - btn_seat) % num_players
    
    if num_players == 2:
        return {0: "BTN", 1: "BB"}.get(dist, "Unknown")

    return {0: "BTN", 1: "SB", 2: "BB", 3: "UTG", 4: "HJ", 5: "CO"}.get(dist, f"Seat_{dist}")

def get_stack_as_bb(game_state):
    bb_amount = next((a['amount'] for a in game_state['action_log'] if a['action'] == 'big_blind'), 100)
    return game_state.get('your_stack', 1) / bb_amount

def floor_to_custom_bin(stack_size):
    if stack_size >= STACK_BINS[-1]:
        return STACK_BINS[-1]
    index = bisect.bisect_right(STACK_BINS, stack_size) - 1
    if index < 0: return STACK_BINS[0]
    
    # round to nearest bin instead of always flooring
    lower = STACK_BINS[index]
    upper = STACK_BINS[index + 1]
    if (stack_size - lower) > (upper - stack_size):
        return upper
    return lower

def get_range(pos: str, stack_size: float, scenario: str) -> List[str]:
    
    split_scenario = scenario.split(' ')
    base_scenario = split_scenario[0]

    stack_bin = floor_to_custom_bin(stack_size)
    
    scenario_data = RANGES.get(base_scenario, {})
    
    bin_data = scenario_data.get(f'{stack_bin}bb', {})
    
    pos_data = bin_data.get(pos, {})
    
    if base_scenario == 'FRFI':
        pos_data = pos_data.get(split_scenario[1],{})

    return list(pos_data.keys())

def get_preflop_scenario(game_state: dict) -> str:
    actions = game_state.get('action_log', [])
    raises = [a for a in actions if a.get('action') in ('raise', 'all_in')]
    n_raises = len(raises)
    if n_raises == 0: 
        return 'RFI'
        
    if n_raises == 1: 
        position_raised = get_position_name(game_state,raises[0].get('seat'))
        return f'FRFI vs_{position_raised}'
    
    if n_raises == 2: 
        return '3BET'
    return '3BET_PLUS'

def get_raise_amount(game_state:dict):
    raises = [a for a in game_state.get('action_log',[]) if a['action'] in ('raise','all_in')]
    if not raises:
        return next((a['amount'] for a in game_state['action_log'] if a['action'] == 'big_blind'), 100)

    return raises[-1]['amount']

def is_ip_vs(my_pos: str, villain_pos: str) -> bool:
    my_idx = POSTFLOP_ORDER.index(my_pos) if my_pos in POSTFLOP_ORDER else 0
    vil_idx = POSTFLOP_ORDER.index(villain_pos) if villain_pos in POSTFLOP_ORDER else 0
    return my_idx > vil_idx

def handle_preflop(game_state) -> dict:
    pos = get_position_name(game_state, game_state.get('seat_to_act', 0))
    stack = get_stack_as_bb(game_state)
    scenario = get_preflop_scenario(game_state)
    hand_key = cards_to_key(game_state['your_cards'])

    hand_range = get_range(pos, stack, scenario)
    in_range = hand_key in hand_range

    log(f'scenario: {scenario} | pos: {pos} | hand: {hand_key} | in_range: {in_range}')

    if not in_range:
        if game_state.get('can_check',False):
            return {'action':'check'}
        return {'action': 'fold'}

    bb_amount = next((a['amount'] for a in game_state['action_log'] if a['action'] == 'big_blind'), 100)
    stack_chips = game_state.get('your_stack', 0)

    if scenario == 'RFI':
        size = RFI_SIZES.get(pos, 2.5)
        amount = int(size * bb_amount)
        amount = min(amount, stack_chips)
        log(f'RFI > {amount} @ {pos} with {hand_key} | stack: {stack:.1f}bb bin: {floor_to_custom_bin(stack)}')
        return {'action': 'raise', 'amount': amount}

    elif scenario.startswith('FRFI'):
        villain_pos = scenario.split('vs_')[-1]
        multiplier = 2.75 if is_ip_vs(pos, villain_pos) else 3.25
        raise_amount = get_raise_amount(game_state)
        amount = int(multiplier * raise_amount)
        amount = max(game_state.get('min_raise_to', 0), amount)
        amount = min(amount, stack_chips)
        log(f'3bet > {amount} @ {pos} vs {villain_pos} with {hand_key}')
        return {'action': 'raise', 'amount': amount}

    elif scenario == '3BET':
        raise_amount = get_raise_amount(game_state)
        amount = int(2.25 * raise_amount)
        amount = max(game_state.get('min_raise_to', 0), amount)
        amount = min(amount, stack_chips)
        log(f'4bet > {amount} @ {pos} with {hand_key}')
        return {'action': 'raise', 'amount': amount}

    elif scenario == '3BET_PLUS':
        log(f'Shove > {stack_chips} @ {pos} with {hand_key}')
        return {'action': 'raise', 'amount': stack_chips}

    if game_state.get('can_check',False):
        return {'action':'check'}
    
    return {'action': 'fold'}

# returns pot odds as float [0, 1]
def get_pot_odds(game_state) -> float:
    # * get amount you need to put in to call
    # * get total pot amnt for if you call
    # * return ratio of call amnt / pot size

    if game_state.get('can_check',False):
        return 0.0

    pot_size_raw = sum (a.get('amount',0) for a in game_state.get('action_log',[]))
    amount_to_call = game_state.get('amount_owed',0)
    total_pot = pot_size_raw + amount_to_call

    return amount_to_call/total_pot


def get_opponent_preflop_action(game_state: dict, opponent_seat: int) -> str:

    opponent_actions = [
        a for a in game_state.get('action_log', []) if a.get('seat') == opponent_seat]

    if not opponent_actions:
        return "unknown"

    if any(a.get('action') in ('raise', 'all_in') for a in opponent_actions):
        return 'raise'

    if any(a.get('action') == 'call' for a in opponent_actions):
        return 'call'

    return 'check_or_fold'

def get_opponent_range(game_state, opponent_dict):
    # * Opponent Position
    # * Pre-flop action
    # * Opponent stack size
    # ? Range lookup against these values
    log(game_state['action_log'])
    
    position = get_position_name(game_state,opponent_dict.get('seat'))
    action = get_opponent_preflop_action(game_state, opponent_dict.get('seat'))
    stack = opponent_dict.get('stack',0)

    log(f'{position,action,stack}')
    

def get_equity(game_state):
    # * My hand
    # * Community cards
    # ? Opponent range
    
    my_hand = game_state.get('your_cards',[])
    community_cards = game_state.get('community_cards',[])

    current_players = [player for player in game_state.get('players',[]) if player.get('is_folded',True) == False and player.get('seat',-1) != game_state.get('seat_to_act')]
    
    for opponent in current_players:
        op_range = get_opponent_range(game_state, opponent)


def handle_flop(game_state:dict) -> dict:
    # * Pot Odds
    # ? Equity
    
    pot_odds = get_pot_odds(game_state)
    equity = get_equity(game_state)



def decide(game_state: dict) -> dict:
    move = {'action':'fold'}
    street = game_state.get('street','')
    try:
        if game_state.get('type') == 'warmup':
            return {"ok": True}

        if street  == 'preflop':
            move = handle_preflop(game_state)

        elif street == 'flop':
            handle_flop(game_state) 

        handle_flop(game_state)

        # log_state(game_state)

        return move

    except Exception:
        err = traceback.format_exc()
        log("!!! BOT CRASHED !!!")
        log(err)
        return {"action": "fold"}
    

