import asyncio
import json
from datetime import datetime
from core.utils import is_valid_json
from core.commands import Command
from colorama import Fore
from .core_temple import *

target_monsters = "Ascended Midnight"
stop_attack = False
do_taunt = False
log_taunt = True
converges_count = 0
light_gather_count = 0
cleared_count = 0

# SLAVE MAID
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, log_taunt, converges_count, light_gather_count
    
    def reset_counters():
        global do_taunt, stop_attack, converges_count, cleared_count
        converges_count = 0 # reset converges count
        do_taunt = False # reset taunt
        stop_attack = False # reset stop attack
            
    def msg_taunt_handler(message):
        global target_monsters, stop_attack, do_taunt, log_taunt, converges_count, light_gather_count
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                cmd = data["cmd"]
                if cmd == "ct":
                    anims = data.get("anims") # Animations
                    m = data.get("m") # Monster conditions
                    p = data.get("p") # Player conditions
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg", "").lower()
                            if "gather" in msg:
                                light_gather_count += 1
                                if light_gather_count % 2 == 0:
                                    do_taunt = True
                            if  "moon converges" in msg:
                                converges_count += 1
                                if converges_count % 2 == 0:
                                    do_taunt = True
                    if m:
                        for mon_map_id, mon_condition in m.items():
                            monHp = int(mon_condition.get('intHP'))
                            is_alive = monHp > 0
                            if (is_alive == False):
                                print_debug(f"Monster id:{mon_map_id} is dead.")
            except:
                return
    cmd.bot.subscribe(msg_taunt_handler)

    invitation_queue = asyncio.Queue()
    def party_invitation_handler(message):
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                if data["cmd"] == "pi":
                    invitation_queue.put_nowait(data["pid"])
            except:
                return
    cmd.bot.subscribe(party_invitation_handler)
    
    await cmd.equip_item(cmd.getFarmClass())
    await cmd.equip_scroll("Scroll of Enrage")
    
    while (cmd.bot.strMapName != "yulgar"):
        await go_to_master(cmd)
        await cmd.sleep(1000)
    
    print_debug("Waiting party invitation...")
    pid = await invitation_queue.get()
    print_debug(f"Accepting party invitation from PID: {pid}")
    await cmd.send_packet(f"%xt%zm%gp%1%pa%{pid}%")
    await cmd.sleep(1000)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    is_attacking = False
    
    while cmd.isStillConnected():
        reset_counters()
        await go_to_master(cmd)
            
        master = cmd.get_player_in_map(cmd.bot.follow_player)
        while cmd.is_monster_alive() and master.str_frame == cmd.bot.player.CELL:  
            if cmd.bot.player.ISDEAD:
                is_attacking = False
                print_debug("You are dead. Waiting to respawn...")
                await cmd.sleep(1000)
                break

            target_monsters = "Ascended Midnight,Sunset Knight"
            stop_attack = cmd.bot.player.hasAura("Sun's Heat")
                
            if cmd.bot.player.hasAura("Solar Flare"):
                target_monsters = "Blessless Deer"
                
            if not is_attacking:
                print_debug(f"[{cmd.bot.player.CELL}] Attacking monsters...")
                is_attacking = True
            if do_taunt:
                if log_taunt:
                    print_debug(f"[{cmd.bot.player.CELL}] Doing taunt...")
                await cmd.sleep(1000)
                await cmd.use_skill(5, target_monsters=target_monsters)
                await cmd.sleep(500)
                await cmd.use_skill(5, target_monsters=target_monsters)
                do_taunt = False
            else:
                await cmd.use_skill(skill_list[skill_index], target_monsters, buff_only=stop_attack)
                skill_index += 1
                if skill_index >= len(skill_list):
                    skill_index = 0
            await cmd.sleep(100)
        is_attacking = False