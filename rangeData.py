from poker import Range
import json

BOT_DIR = 'bots/mybot/data'


RAW_SHORTHAND_DATA = {
    "100bb": {
        "UTG": "77+, ATs+, KTs+, QTs+, JTs, AJo+, KQo",
        "HJ":  "55+, A2s+, KTs+, QTs+, JTs+, T9s, ATo+, KQo",
        "CO":  "22+, A2s+, K8s+, Q9s+, J9s+, T9s, 98s, 87s, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 86s+, 76s, 65s, 54s, A2o+, K8o+, Q9o+, J9o+, T9o",
        "SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 84s+, 74s+, 63s+, 53s+, 43s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o"
    },
    "60bb": {
        "UTG": "88+, AJs+, KJs+, QJs, AQo+",
        "HJ":  "66+, A2s+, KTs+, QTs+, JTs, AJo+, KQo",
        "CO":  "33+, A2s+, K8s+, Q9s+, J9s+, T9s, 87s, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K3s+, Q6s+, J7s+, T7s+, 97s+, 87s, 76s, A2o+, K9o+, Q9o+, J9o+, T9o",
        "SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 75s+, 65s, A2o+, K6o+, Q8o+, J8o+, T8o+"
    },
    "40bb": {
        "UTG": "88+, ATs+, KJs+, QJs, AQo+",
        "HJ":  "77+, ATs+, KTs+, QTs+, JTs, AJo+, KQo",
        "CO":  "44+, A2s+, K9s+, Q9s+, J9s+, T9s, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K4s+, Q7s+, J8s+, T8s+, 98s, A2o+, K9o+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T6s+, 96s+, 86s+, 76s, A2o+, K7o+, Q9o+, J9o+, T9o"
    },
    "30bb": {
        "UTG": "99+, ATs+, KJs+, AQo+",
        "HJ":  "77+, ATs+, KTs+, QJs, AJo+, KQo",
        "CO":  "55+, A2s+, KTs+, QTs+, JTs, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A4o+, KTo+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q4s+, J6s+, T7s+, 97s+, 87s, A2o+, K8o+, Q9o+, J9o+, T9o"
    },
    "25bb": {
        "UTG": "99+, AJs+, KQs, AQo+",
        "HJ":  "88+, ATs+, KJs+, AJo+, KQo",
        "CO":  "55+, A2s+, KTs+, QTs+, JTs, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K6s+, Q8s+, J8s+, T8s+, A5o+, KTo+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 98s, A2o+, K9o+, Q9o+, J9o+, T9o"
    },
    "20bb": {
        "UTG": "99+, ATs+, KJs+, AJo+",
        "HJ":  "77+, ATs+, KTs+, QJs, ATo+, KQo",
        "CO":  "55+, A2s+, K9s+, QTs+, JTs, ATo+, KTo+, QJo",
        "BTN": "22+, A2s+, K7s+, Q9s+, J9s+, T9s, A7o+, KTo+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q6s+, J8s+, T8s+, 98s, A2o+, KTo+, QTo+, JTo"
    },
    "15bb": {
        "UTG": "77+, ATs+, KQs, ATo+, KQo",
        "HJ":  "66+, A8s+, KJs+, QJs, ATo+, KJo+",
        "CO":  "44+, A2s+, KTs+, QTs+, JTs, A9o+, KTo+, QJo",
        "BTN": "22+, A2s+, K8s+, Q9s+, J9s+, T9s, A5o+, KTo+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q7s+, J8s+, T8s+, 98s, A2o+, KTo+, QTo+, JTo"
    },
    "12bb": {
        "UTG": "77+, A8s+, KQs, ATo+, KQo",
        "HJ":  "55+, A5s+, KTs+, QJs, ATo+, KJo+",
        "CO":  "22+, A2s+, K9s+, QTs+, JTs, A8o+, KTo+, QTo+",
        "BTN": "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A3o+, KTo+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 97s+, 87s, A2o+, K8o+, Q9o+, J9o+, T9o"
    },
    "10bb": {
        "UTG": "55+, A5s+, KJs+, ATo+, KQo",
        "HJ":  "44+, A2s+, KTs+, QTs+, A9o+, KTo+, QJo",
        "CO":  "22+, A2s+, K8s+, Q9s+, J9s+, A7o+, KTo+, QTo+, JTo",
        "BTN": "22+, A2s+, K4s+, Q8s+, J8s+, T8s+, 98s, A2o+, K9o+, QTo+, JTo",
        "SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o"
    },
    "8bb": {
        "UTG": "44+, A2s+, KTs+, QJs, A8o+, KTo+, QJo",
        "HJ":  "22+, A2s+, K8s+, QTs+, JTs, A7o+, KTo+, QTo+, JTo",
        "CO":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, A5o+, K9o+, QTo+, JTo",
        "BTN": "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 98s, A2o+, K8o+, Q9o+, J9o+, T9o",
        "SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T2s+, 92s+, 84s+, 74s+, 64s+, 54s, A2o+, K2o+, Q4o+, J7o+, T7o+, 97o+"
    }
}


def build_range_database(source_data):
    master_db = {}
    
    for stack_bin, positions in source_data.items():
        master_db[stack_bin] = {}
        for pos, shorthand in positions.items():
            # Range() parses the shorthand; .hands returns the 169 unique hand objects
            expanded_hands = Range(shorthand).hands
            
            # Map each hand to 1 (Action: Raise/Push)
            # Using str(hand) converts it to 'AKs', '76o', '22', etc.
            master_db[stack_bin][pos] = {str(h): 1 for h in expanded_hands}
            
    return master_db

poker_db = build_range_database(RAW_SHORTHAND_DATA)

with open('bots/mybot/data/RFI.json', 'w') as f:
    json.dump(poker_db, f, indent=4)
