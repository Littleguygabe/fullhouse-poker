from poker import Range
import json

BOT_DIR = 'bots/mybot/data'


RAW_SHORTHAND_DATA = {
    "100bb": {
        "HJ":  { "vs_UTG": "88+, ATs+, KQs, QJs, JTs, T9s, AQo+" },
        "CO":  { "vs_UTG": "77+, ATs+, KJs+, QJs, JTs, T9s, 98s, AQo+",
                 "vs_HJ":  "77+, A9s+, KTs+, QJs, JTs, T9s, 98s, AJo+, KQo" },
        "BTN": { "vs_UTG": "66+, ATs+, KTs+, QJs, JTs, T9s, 98s, 87s, AQo+",
                 "vs_HJ":  "55+, A9s+, KTs+, QTs+, JTs, T9s, 98s, 87s, AJo+, KQo",
                 "vs_CO":  "22+, A2s+, K9s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, ATo+, KJo+, QJo" },
        "SB":  { "vs_UTG": "99+, AJs+, KQs, AKo",
                 "vs_HJ":  "88+, ATs+, KJs+, QJs, AQo+",
                 "vs_CO":  "77+, A9s+, KTs+, QTs+, JTs, AJo+, KQo",
                 "vs_BTN": "55+, A2s+, K8s+, Q9s+, J9s+, T9s, ATo+, KTo+, QJo" },
        "BB":  { "vs_UTG": "22+, A2s+, K8s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, 65s, ATo+, KTo+, QJo",
                 "vs_HJ":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, 87s, 76s, 65s, 54s, A9o+, KTo+, QTo+, JTo",
                 "vs_CO":  "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, 76s, 65s, 54s, A8o+, K9o+, Q9o+, J9o+, T9o",
                 "vs_BTN": "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 75s+, 65s, 54s, A2o+, K8o+, Q8o+, J8o+, T8o+, 98o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 74s+, 64s+, 53s+, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "60bb": {
        "HJ":  { "vs_UTG": "88+, AJs+, KQs, QJs, JTs, AQo+" },
        "CO":  { "vs_UTG": "88+, ATs+, KJs+, QJs, JTs, T9s, AQo+",
                 "vs_HJ":  "77+, ATs+, KTs+, QJs, JTs, T9s, AJo+, KQo" },
        "BTN": { "vs_UTG": "77+, ATs+, KTs+, QJs, JTs, T9s, 98s, AQo+",
                 "vs_HJ":  "66+, A9s+, KTs+, QTs+, JTs, T9s, 98s, AJo+, KQo",
                 "vs_CO":  "44+, A2s+, K9s+, Q9s+, J9s+, T9s, 98s, ATo+, KJo+, QJo" },
        "SB":  { "vs_UTG": "99+, AQs+, AKo",
                 "vs_HJ":  "88+, AJs+, KQs, AQo+",
                 "vs_CO":  "77+, ATs+, KJs+, QJs, AJo+, KQo",
                 "vs_BTN": "55+, A9s+, KTs+, QTs+, JTs, ATo+, KTo+, QJo" },
        "BB":  { "vs_UTG": "33+, A2s+, K8s+, Q9s+, J9s+, T9s, 98s, 87s, ATo+, KTo+, QJo",
                 "vs_HJ":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, 87s, 76s, A9o+, KTo+, QTo+, JTo",
                 "vs_CO":  "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, 76s, A8o+, K9o+, Q9o+, J9o+, T9o",
                 "vs_BTN": "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 76s, 65s, A2o+, K8o+, Q8o+, J8o+, T8o+, 98o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 75s+, 64s+, 54s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "40bb": {
        "HJ":  { "vs_UTG": "99+, AJs+, KQs, AQo+" },
        "CO":  { "vs_UTG": "88+, ATs+, KJs+, QJs, AQo+",
                 "vs_HJ":  "77+, ATs+, KTs+, QJs, JTs, AJo+, KQo" },
        "BTN": { "vs_UTG": "77+, ATs+, KJs+, QJs, JTs, T9s, AQo+",
                 "vs_HJ":  "66+, A9s+, KTs+, QTs+, JTs, T9s, 98s, AJo+, KQo",
                 "vs_CO":  "44+, A2s+, K9s+, Q9s+, J9s+, T9s, 98s, 87s, ATo+, KJo+, QJo" },
        "SB":  { "vs_UTG": "TT+, AQs+, AKo",
                 "vs_HJ":  "99+, AJs+, KQs, AQo+",
                 "vs_CO":  "77+, ATs+, KJs+, QJs, AJo+, KQo",
                 "vs_BTN": "55+, A8s+, KTs+, QTs+, JTs, ATo+, KTo+, QJo" },
        "BB":  { "vs_UTG": "44+, A2s+, K8s+, Q9s+, J9s+, T9s, 98s, ATo+, KTo+, QJo",
                 "vs_HJ":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, 87s, A9o+, KTo+, QTo+, JTo",
                 "vs_CO":  "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, 76s, A8o+, K9o+, Q9o+, J9o+, T9o",
                 "vs_BTN": "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 76s, A2o+, K8o+, Q8o+, J8o+, T8o+, 98o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 75s+, 65s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "30bb": {
        "HJ":  { "vs_UTG": "99+, AJs+, KQs, AQo+" },
        "CO":  { "vs_UTG": "88+, ATs+, KJs+, QJs, AQo+",
                 "vs_HJ":  "88+, ATs+, KTs+, QJs, AJo+, KQo" },
        "BTN": { "vs_UTG": "88+, ATs+, KJs+, QJs, JTs, AQo+",
                 "vs_HJ":  "77+, ATs+, KTs+, QTs+, JTs, AJo+, KQo",
                 "vs_CO":  "55+, A5s+, K9s+, Q9s+, J9s+, T9s, ATo+, KTo+, QJo" },
        "SB":  { "vs_UTG": "TT+, AQs+, AKo",
                 "vs_HJ":  "99+, AJs+, KQs, AQo+",
                 "vs_CO":  "88+, ATs+, KJs+, AJo+, KQo",
                 "vs_BTN": "66+, A8s+, KTs+, QTs+, JTs, ATo+, KQo" },
        "BB":  { "vs_UTG": "55+, A2s+, K9s+, QTs+, JTs, T9s, ATo+, KJo+",
                 "vs_HJ":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A9o+, KTo+, QJo",
                 "vs_CO":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, 87s, A9o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, 76s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 95s+, 85s+, 75s+, 65s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "25bb": {
        "HJ":  { "vs_UTG": "TT+, AQs+, AKo" },
        "CO":  { "vs_UTG": "99+, AJs+, KQs, AQo+",
                 "vs_HJ":  "88+, ATs+, KJs+, AJo+, KQo" },
        "BTN": { "vs_UTG": "88+, ATs+, KJs+, QJs, AQo+",
                 "vs_HJ":  "77+, A9s+, KTs+, QTs+, JTs, AJo+, KQo",
                 "vs_CO":  "55+, A5s+, K9s+, Q9s+, J9s+, T9s, ATo+, KTo+, QJo" },
        "SB":  { "vs_UTG": "JJ+, AKs, AKo",
                 "vs_HJ":  "TT+, AQs+, AKo",
                 "vs_CO":  "88+, AJs+, KQs, AQo+",
                 "vs_BTN": "66+, ATs+, KTs+, QTs+, JTs, ATo+, KQo" },
        "BB":  { "vs_UTG": "55+, A2s+, K9s+, QTs+, JTs, ATo+, KJo+",
                 "vs_HJ":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A9o+, KTo+, QJo",
                 "vs_CO":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A5o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "20bb": {
        "HJ":  { "vs_UTG": "TT+, AQs+, AKo" },
        "CO":  { "vs_UTG": "99+, AJs+, KQs, AQo+",
                 "vs_HJ":  "88+, ATs+, KJs+, AJo+, KQo" },
        "BTN": { "vs_UTG": "88+, ATs+, KJs+, QJs, AQo+",
                 "vs_HJ":  "77+, A9s+, KTs+, QTs+, JTs, AJo+, KQo",
                 "vs_CO":  "55+, A5s+, K9s+, Q9s+, J9s+, T9s, ATo+, KTo+, QJo" },
        "SB":  { "vs_UTG": "JJ+, AKs, AKo",
                 "vs_HJ":  "TT+, AQs+, AKo",
                 "vs_CO":  "88+, AJs+, KQs, AQo+",
                 "vs_BTN": "66+, ATs+, KTs+, QTs+, JTs, ATo+, KQo" },
        "BB":  { "vs_UTG": "55+, A5s+, K9s+, QTs+, JTs, ATo+, KJo+",
                 "vs_HJ":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A9o+, KTo+, QJo",
                 "vs_CO":  "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A5o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "15bb": {
        "HJ":  { "vs_UTG": "TT+, AQs+, AKo" },
        "CO":  { "vs_UTG": "99+, AJs+, KQs, AQo+",
                 "vs_HJ":  "88+, ATs+, KJs+, AQo+" },
        "BTN": { "vs_UTG": "88+, ATs+, KQs, AQo+",
                 "vs_HJ":  "77+, A9s+, KJs+, AJo+, KQo",
                 "vs_CO":  "66+, A5s+, KTs+, QJs, ATo+, KQo" },
        "SB":  { "vs_UTG": "JJ+, AKs, AKo",
                 "vs_HJ":  "TT+, AQs+, AKo",
                 "vs_CO":  "88+, AJs+, KQs, AQo+",
                 "vs_BTN": "66+, ATs+, KJs+, ATo+, KQo" },
        "BB":  { "vs_UTG": "66+, A8s+, KTs+, QJs, ATo+, KJo+",
                 "vs_HJ":  "55+, A5s+, K9s+, QTs+, JTs, A9o+, KTo+, QJo",
                 "vs_CO":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A5o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "12bb": {
        "HJ":  { "vs_UTG": "TT+, AQs+, AKo" },
        "CO":  { "vs_UTG": "99+, AJs+, AKo",
                 "vs_HJ":  "88+, ATs+, KQs, AQo+" },
        "BTN": { "vs_UTG": "88+, ATs+, KQs, AQo+",
                 "vs_HJ":  "77+, A9s+, KJs+, AJo+, KQo",
                 "vs_CO":  "66+, A5s+, KTs+, QJs, ATo+, KQo" },
        "SB":  { "vs_UTG": "JJ+, AKs, AKo",
                 "vs_HJ":  "TT+, AQs+, AKo",
                 "vs_CO":  "88+, AJs+, KQs, AQo+",
                 "vs_BTN": "66+, ATs+, KJs+, ATo+, KQo" },
        "BB":  { "vs_UTG": "66+, A8s+, KTs+, QJs, ATo+, KJo+",
                 "vs_HJ":  "55+, A5s+, K9s+, QTs+, JTs, A9o+, KTo+, QJo",
                 "vs_CO":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A5o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "10bb": {
        "HJ":  { "vs_UTG": "TT+, AQs+, AKo" },
        "CO":  { "vs_UTG": "99+, AJs+, AKo",
                 "vs_HJ":  "88+, ATs+, KQs, AQo+" },
        "BTN": { "vs_UTG": "88+, ATs+, KQs, AQo+",
                 "vs_HJ":  "77+, A9s+, KJs+, AJo+, KQo",
                 "vs_CO":  "66+, A5s+, KTs+, QJs, ATo+, KQo" },
        "SB":  { "vs_UTG": "JJ+, AKs, AKo",
                 "vs_HJ":  "TT+, AQs+, AKo",
                 "vs_CO":  "88+, AJs+, KQs, AQo+",
                 "vs_BTN": "66+, ATs+, KJs+, ATo+, KQo" },
        "BB":  { "vs_UTG": "66+, A8s+, KTs+, QJs, ATo+, KJo+",
                 "vs_HJ":  "55+, A5s+, K9s+, QTs+, JTs, A9o+, KTo+, QJo",
                 "vs_CO":  "44+, A2s+, K8s+, Q9s+, J9s+, T9s, A5o+, K9o+, QTo+, JTo",
                 "vs_BTN": "22+, A2s+, K5s+, Q8s+, J8s+, T8s+, 98s, A2o+, K8o+, Q9o+, J9o+, T9o",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    },
    "8bb": {
        "HJ":  { "vs_UTG": "JJ+, AKs, AKo" },
        "CO":  { "vs_UTG": "TT+, AQs+, AKo",
                 "vs_HJ":  "99+, AJs+, AKo" },
        "BTN": { "vs_UTG": "99+, AJs+, AKo",
                 "vs_HJ":  "88+, ATs+, KQs, AQo+",
                 "vs_CO":  "77+, A9s+, KJs+, AJo+, KQo" },
        "SB":  { "vs_UTG": "QQ+, AKs",
                 "vs_HJ":  "JJ+, AKs, AKo",
                 "vs_CO":  "TT+, AQs+, AKo",
                 "vs_BTN": "88+, AJs+, KQs, AQo+" },
        "BB":  { "vs_UTG": "77+, A9s+, KJs+, ATo+, KQo",
                 "vs_HJ":  "66+, A8s+, KTs+, QJs, ATo+, KJo+",
                 "vs_CO":  "55+, A5s+, K9s+, QTs+, JTs, A9o+, KTo+, QJo",
                 "vs_BTN": "22+, A2s+, K8s+, Q9s+, J9s+, T9s, A5o+, K9o+, QTo+, JTo",
                 "vs_SB":  "22+, A2s+, K2s+, Q2s+, J4s+, T5s+, 96s+, 86s+, 76s, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    }
}
def build_range_database(source_data):
    master_db = {}
    
    for stack_bin, positions in source_data.items():
        master_db[stack_bin] = {}
        for pos, against in positions.items():
            # Range() parses the shorthand; .hands returns the 169 unique hand objects
            master_db[stack_bin][pos] = {}
            
            # Map each hand to 1 (Action: Raise/Push)
            # Using str(hand) converts it to 'AKs', '76o', '22', etc.

            for op, hand in against.items():
                print(stack_bin, pos, op)
                expanded_hands = Range(hand).hands
                master_db[stack_bin][pos][op] = {str(h): 1 for h in expanded_hands}


    return master_db

poker_db = build_range_database(RAW_SHORTHAND_DATA)

with open('bots/mybot/data/FRFI.json', 'w') as f:
    json.dump(poker_db, f, indent=4)
