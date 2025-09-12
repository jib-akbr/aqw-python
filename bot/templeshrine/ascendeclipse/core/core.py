from datetime import datetime
from colorama import Fore

def print_debug(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}{message}{Fore.RESET}")