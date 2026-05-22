import os
import sys
import json

BOT_NAME = "ranger"
BOT_AVATAR = "robot_1"


class Logger:
    def __init__(self) -> None:
        self.bot_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_dir = os.path.join(self.bot_dir,'debug.log')
        self._init_log()

    def log(self,message):
        msg = str(message)
        try:
            with open(self.log_dir, "a") as f:
                f.write(msg + "\n")
        except Exception:
            pass

    def _init_log(self):
        try:
            with open(self.log_dir, "w") as f:
                f.write("<-- MATCH START -->\n")
        except Exception:
            pass

class RangeController:
    def __init__(self) -> None:
        self.bot_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.bot_dir,'data')

        self.preflop_ranges = {}

        self.load_range_data()

    def load_range_data(self):
        self._load_preflop_ranges()

    def _load_preflop_ranges(self):
        # * RFI
        # ? FRFI Call ranges
        # ? FRFI Raise ranges
        # ? 3Bet ranges
        # ? 3Bet+ ranges

        if os.path.exists(self.data_dir):
            preflop_folder = os.path.join(self.data_dir,'preflop')
            for fn in os.listdir(preflop_folder):
                if fn.endswith('.json'):
                    LOGGER.log(f'Loaded {fn}')
                    scenario = fn.split('.')[0]
                    path = os.path.join(preflop_folder,fn)
                    try:
                        if os.path.getsize(path) > 0:
                            with open(path) as f:
                                self.preflop_ranges[scenario] = json.load(f)
                        else:
                            LOGGER.log(f"WARNING: Skipping empty data file: {fn}")
                    except Exception as e:
                        LOGGER.log(f"ERROR: Could not load {fn}: {e}")

LOGGER = Logger()
RANGE_CONTROLLER = RangeController()


def decide(game_state: dict) -> dict:
    return {"action": "fold"}

