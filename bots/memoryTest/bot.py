import os
import sys
from typing import *

BOT_NAME = "MyBot"
BOT_AVATAR = "robot_1"

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

try:
    with open(LOG_FILE, "w") as f:
        f.write("--- MATCH START ---\n")
except Exception:
    pass



class MemoryTester:
    def __init__(self) -> None:
        self.count = 1

    def iterate(self):
        log(self.count)
        self.count+=1

global_memory = MemoryTester()

def decide(game_state:dict):

    global_memory.iterate()
    return {'action':'fold'}