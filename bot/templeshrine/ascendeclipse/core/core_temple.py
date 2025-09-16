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

async def prepare_items(cmd: Command):
    minimalScroll = 50
    if cmd.get_quant_item("Scroll of Enrage") < minimalScroll:
        cmd.bot.stop_bot(f"Not enough Scroll of Enrage. Minimum {minimalScroll} required.")
        return
    await cmd.equip_item(cmd.getFarmClass())
    await cmd.equip_scroll("Scroll of Enrage")

async def go_to_master(cmd: Command):        
    if cmd.bot.follow_player:
        if not cmd.is_player_in_cell(cmd.bot.follow_player, cmd.bot.player.CELL):
            print_debug(f"[{cmd.bot.player.CELL}] Going to master's place...")
            while not cmd.is_player_in_cell(cmd.bot.follow_player, cmd.bot.player.CELL):
                await cmd.bot.goto_player(cmd.bot.follow_player)
                if cmd.get_player_in_map(cmd.bot.follow_player):
                    await cmd.sleep(200)
                else:
                    await cmd.sleep(1000)
        await cmd.sleep(100)
    else:
        cmd.stopBot("No master assigned to follow.")

async def use_taunt(cmd: Command, target_monsters: str, show_log=False):
    if show_log or True:
        print_debug(f"[{cmd.bot.player.CELL}] Taunting {target_monsters}...", Fore.BLUE)
    await cmd.sleep(500)
    # await cmd.use_skill(5, target_monsters=target_monsters)
    # await cmd.sleep(500)
    # await cmd.use_skill(5, target_monsters=target_monsters)
    await cmd.wait_use_skill(5, target_monsters=target_monsters)
    
async def skill_delay(cmd: Command):
    await cmd.sleep(100)