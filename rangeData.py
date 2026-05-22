from poker import Range
import json

# 1. Define the isolated flat-calling ranges (FRFI Call)
RAW_FRFI_CALL_DATA = {
    "100bb": {
        "HJ":  { "vs_UTG": "JJ-88, AQs-ATs, KQs, QJs, JTs, T9s, AQo" },
        "CO":  { "vs_UTG": "TT-88, AJs-ATs, KJs+, QJs, JTs, T9s, 98s, AQo",
                 "vs_HJ":  "TT-88, AJs-ATs, KTs+, QJs, JTs, T9s, 98s, AJo, KQo" },
        "BTN": { "vs_UTG": "99-66, AJs-ATs, KTs+, QJs, JTs, T9s, 98s, 87s, AQo",
                 "vs_HJ":  "99-55, AJs-ATs, KTs+, QTs+, JTs, T9s, 98s, 87s, AJo, KQo",
                 "vs_CO":  "99-22, AQs-A2s, K9s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, ATo+, KJo+, QJo" },
        "SB":  { "vs_UTG": "JJ-99, AQs-AJs, KQs",
                 "vs_HJ":  "TT-88, AQs-ATs, KJs+, QJs",
                 "vs_CO":  "99-77, AJs-A9s, KTs+, QTs+, JTs, KQo",
                 "vs_BTN": "88-55, A9s-A2s, K8s+, Q9s+, J9s+, T9s, ATo, KTo+, QJo" },
        "BB":  { "vs_UTG": "99-22, AQs-A2s, K8s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, 65s, ATo+, KTo+, QJo",
                 "vs_HJ":  "99-22, AQs-A2s, K5s+, Q8s+, J8s+, T8s+, 98s, 87s, 76s, 65s, 54s, A9o+, KTo+, QTo+, JTo",
                 "vs_CO":  "99-22, AQs-A2s, K2s+, Q5s+, J7s+, T7s+, 97s+, 87s, 76s, 65s, 54s, A8o+, K9o+, Q9o+, J9o+, T9o",
                 "vs_BTN": "99-22, AJs-A2s, K2s+, Q2s+, J5s+, T6s+, 96s+, 86s+, 75s+, 65s, 54s, A2o+, K8o+, Q8o+, J8o+, T8o+, 98o",
                 "vs_SB":  "99-22, ATs-A2s, K2s+, Q2s+, J2s+, T4s+, 95s+, 85s+, 74s+, 64s+, 53s+, A2o+, K5o+, Q8o+, J8o+, T8o+, 98o" }
    }
    # You must populate the 60bb, 40bb, 30bb, 25bb, 20bb, 15bb, 12bb, 10bb, and 8bb bins here using the same syntax.
}

def build_range_database(source_data):
    master_db = {}
    
    for stack_bin, positions in source_data.items():
        master_db[stack_bin] = {}
        for pos, against in positions.items():
            master_db[stack_bin][pos] = {}
            for op, hand in against.items():
                expanded_hands = Range(hand).hands
                master_db[stack_bin][pos][op] = {str(h): 1 for h in expanded_hands}

    return master_db

# 2. Execute and output to the new isolated file
poker_db = build_range_database(RAW_FRFI_CALL_DATA)

with open('bots/ranger/data/FRFI_CALL.json', 'w') as f:
    json.dump(poker_db, f, indent=4)