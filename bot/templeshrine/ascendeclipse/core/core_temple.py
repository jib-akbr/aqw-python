import asyncio
from collections import deque
from datetime import datetime
from colorama import Fore
import colorama

colorama.init()

MOVE_UP = "\033[F"
ERASE_LINE = "\033[K"
logs = deque(maxlen=5)

def add_log(message: str):
    if logs:
        print(MOVE_UP * (len(logs)), end="")
        print(ERASE_LINE * (len(logs) + 1), end="")
    logs.append(message)
    print("\n".join(logs))

def print_debug(message, color=Fore.YELLOW):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {color}{message}{Fore.RESET}")