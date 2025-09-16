import asyncio
import json
from datetime import datetime
from core.utils import is_valid_json
from core.commands import Command
from colorama import Fore

pid = None

# SLAVE MAID
async def main(cmd: Command):
    def print_debug(message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}{message}{Fore.RESET}")
    
    async def go_to_master():
        if cmd.bot.follow_player and cmd.bot.followed_player_cell != cmd.bot.player.CELL:
            await cmd.bot.goto_player(cmd.bot.follow_player)
            await cmd.sleep(1000)

    def msg_handler(message):
        global pid
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                cmdData = data["cmd"]
                if cmdData =="pi":
                    pid = data.get("pid")
            except:
                return
    cmd.bot.subscribe(msg_handler)
    
    await cmd.equip_item(cmd.getFarmClass())
    
    print_debug("Waiting for party invitation...")
    while pid is None:
        await go_to_master()
        await cmd.sleep(1000)
    print_debug(f"Accepting party invitation from PID: {pid}")
    await cmd.send_packet(f"%xt%zm%gp%1%pa%{pid}%")
    await cmd.sleep(1000)

    skill_list = [0,1,2,1,2,0,3,4,3,4]
    skill_index = 0
    is_attacking = False
    while cmd.isStillConnected():
        print_debug("Going to master's place...")
        await go_to_master()
        await cmd.sleep(1000)
        while cmd.is_monster_alive():
            if not is_attacking:
                print_debug(f"[{cmd.bot.player.CELL}] Attacking monsters...")
                is_attacking = True
            await cmd.use_skill(skill_list[skill_index])
            skill_index += 1
            if skill_index >= len(skill_list):
                skill_index = 0
            await cmd.sleep(200)
        is_attacking = False