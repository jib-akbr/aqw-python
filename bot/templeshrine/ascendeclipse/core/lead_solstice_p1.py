import time
import json
from datetime import datetime
from core.commands import Command
from core.utils import is_valid_json
from colorama import Fore
from .core_temple import *
    
target_monsters = "Ascended Solstice,Blessless Deer,Suffocated Light"
stop_attack = False
do_taunt = False
timeleapse = 0
log_taunt = True
cleared_count = 0
converges_count = 0
light_gather_count = 0

# PARTY LEADER
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, timeleapse, log_taunt, cleared_count, converges_count, light_gather_count
        
    async def enter_dungeon():
        global timeleapse
        timeleapse = time.monotonic() 
        await cmd.send_packet("%xt%zm%dungeonQueue%25127%ascendeclipse%")
        while cmd.is_not_in_map("ascendeclipse"):
            print_debug("Waiting for dungeon queue...")
            await cmd.sleep(500)
        
    async def to_next_cell():
        global do_taunt, stop_attack, timeleapse, cleared_count, converges_count, light_gather_count
        do_taunt = False # reset taunt
        stop_attack = False # reset stop attack
        converges_count = 0 # reset converges count
        light_gather_count = 0 # reset light gather count
        deerHp = 100 # in percentage
        
        print_debug(f"Moving to next cell...")
        await cmd.sleep(2000)
        if cmd.bot.player.CELL == "Enter":
            await cmd.jump_cell("r1", "Left")
        elif cmd.bot.player.CELL == "r1":
            await cmd.jump_cell("r2", "Left")
        elif cmd.bot.player.CELL == "r2":
            await cmd.jump_cell("r3", "Left")
        elif cmd.bot.player.CELL == "r3":
            await cmd.jump_cell("r4", "Left")
        elif cmd.bot.player.CELL == "r4":
            elapsed_seconds = time.monotonic() - timeleapse
            minutes = int(elapsed_seconds // 60)
            seconds = int(elapsed_seconds % 60)
            cleared_count += 1
            print_debug(f"Dungeon cleared {cleared_count} times.")
            print_debug(f"Total time taken: {minutes} minutes and {seconds} seconds.")
            print_debug(f"Entering new queue...")
            await enter_dungeon()
        
    def msg_taunt_handler(message):
        global stop_attack, do_taunt, log_taunt, converges_count, light_gather_count
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                dataCmd = data["cmd"]
                if dataCmd == "ct":
                    anims = data.get("anims") # Animations
                    m = data.get("m") # Monster conditions
                    p = data.get("p") # Player conditions
                    a = data.get("a") # Auras
                    if a:
                        for auras in a:
                            if auras.get("auras"):
                                if auras.get("auras")[0].get("nam") == "Lunar Prance":
                                    deerHp = deerHp - 10
                                    print_debug(f"Blessless Deer HP : < {deerHp}%")
                                    break
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg")
                            if msg:
                                if "gather" in msg.lower():
                                    light_gather_count += 1
                                    if light_gather_count % 2 != 0:
                                        do_taunt = True
                                if  "sun converges" in msg.lower():
                                    converges_count += 1
                                    if converges_count % 2 != 0:
                                        do_taunt = True
                    if m:
                        for mon_map_id, mon_condition in m.items():
                            monHp = int(mon_condition.get('intHP'))
                            if monHp:
                                mon = cmd.get_monster(f"id.{mon_map_id}")
                                monHpPercent = round(((mon.current_hp/mon.max_hp)*100), 2)
                                print_debug(f"id.{mon_map_id} - {mon.mon_name} HP: {monHpPercent}%")
                            is_alive = monHp > 0
                            if (is_alive == False):
                                print_debug(f"Monster id:{mon_map_id} is dead.")
            except:
                return
    cmd.bot.subscribe(msg_taunt_handler)
    
    # Initial setup
    await cmd.join_map("yulgar", roomNumber=999999)
    await cmd.sleep(4000)
    await cmd.equip_item(cmd.getFarmClass())
    await cmd.equip_scroll("Scroll of Enrage")
    
    # WAit for all slaves to be online
    print_debug(f"Waiting for all slaves to be online...")
    while not cmd.wait_count_player(4):
        await cmd.sleep(100)
    
    # send party invitation to all slaves
    for slave in cmd.bot.slaves_player:
        await cmd.send_packet(f"%xt%zm%gp%1%pi%{slave}%")
        await cmd.sleep(500)

    # Wait for all slaves to join the party, then enter the dungeon
    await cmd.sleep(4000)
    await enter_dungeon()

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    is_attacking = False
    
    while cmd.isStillConnected():
        print_debug("Idle...")
            
        while cmd.is_monster_alive():    
            target_monsters = "Ascended Solstice,Blessless Deer,Suffocated Light"
            
            if cmd.bot.player.hasAura("Sun's Heat"):
                target_monsters = "Moon Haze"

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
        await to_next_cell()