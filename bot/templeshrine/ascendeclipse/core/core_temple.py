import asyncio
from collections import deque
from datetime import datetime
from colorama import Fore
import colorama

from core.commands import Command

colorama.init()

MOVE_UP = "\033[F"
ERASE_LINE = "\033[K"
logs = deque(maxlen=5)

def print_debug2(message: str, color=Fore.YELLOW):
    if logs:
        print(MOVE_UP * (len(logs)), end="")
        print(ERASE_LINE * (len(logs) + 1), end="")
    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {color}{message}{Fore.RESET}")
    print("\n".join(logs))

def print_debug(message, color=Fore.YELLOW):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {color}{message}{Fore.RESET}")

async def go_to_master(cmd: Command):        
    if cmd.bot.follow_player:
        if not cmd.is_player_in_cell(cmd.bot.follow_player, cmd.bot.player.CELL):
            print_debug(f"[{cmd.bot.player.CELL}] Going to master's place...")
            while not cmd.is_player_in_cell(cmd.bot.follow_player, cmd.bot.player.CELL):
                await cmd.sleep(1000)
                await cmd.bot.ensure_leave_from_combat()
                await cmd.bot.goto_player(cmd.bot.follow_player)
        await cmd.sleep(100)
    else:
        cmd.stopBot("No master assigned to follow.")