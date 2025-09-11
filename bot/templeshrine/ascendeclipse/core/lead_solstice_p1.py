import time
import json
from datetime import datetime
from core.commands import Command
from core.utils import is_valid_json
from colorama import Fore

target_monsters = "Ascended Solstice,Blessless Deer,Suffocated Light"
stop_attack = False
do_taunt = False
timeleapse = 0
log_taunt = False
cleared_count = 0
converges_count = 0

# PARTY LEADER
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, timeleapse, log_taunt, cleared_count, converges_count
    
    def print_debug(message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}{message}{Fore.RESET}")
        
    async def enter_dungeon():
        global timeleapse
        timeleapse = time.monotonic() 
        await cmd.send_packet("%xt%zm%dungeonQueue%25127%ascendeclipse%")
        while cmd.is_not_in_map("ascendeclipse"):
            print_debug("Waiting for dungeon queue...")
            await cmd.sleep(200)
        
    async def to_next_cell():
        global stop_attack, timeleapse, cleared_count, converges_count
        stop_attack = False # reset stop attack
        converges_count = 0 # reset converges count
        print_debug(f"Moving to next cell...")
        await cmd.sleep(2000)
        if cmd.bot.player.CELL == "Enter":
            await cmd.jump_cell("r1", "Left")
        elif cmd.bot.player.CELL == "r1":
            await cmd.jump_cell("r2", "Left")
        elif cmd.bot.player.CELL == "r2":
            await cmd.jump_cell("r3", "Left")
        elif cmd.bot.player.CELL == "r3":
            elapsed_seconds = time.monotonic() - timeleapse
            minutes = int(elapsed_seconds // 60)
            seconds = int(elapsed_seconds % 60)
            cleared_count += 1
            print_debug(f"Dungeon cleared {cleared_count} times.")
            print_debug(f"Total time taken: {minutes} minutes and {seconds} seconds.")
            print_debug(f"Entering new queue...")
            await enter_dungeon()
        
    def msg_taunt_handler(message):
        global target_monsters, stop_attack, do_taunt, log_taunt, converges_count
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
                            cInf = auras.get("tInf")
                            if auras.get("auras"):
                                for aura in auras.get("auras"):
                                    if aura.get("nam") == "Solar Flare":
                                        print_debug(f"{cInf} Aura: {aura.get('msgOn')}")
                                        if aura.get("isNew") == True:
                                            target_monsters = "Blessless Deer,Ascended Solstice"
                                            
                                    if aura.get("nam") == "Moonveil":
                                        print_debug(f"{cInf} Aura: {aura.get('msgOn')}")
                                        if aura.get("isNew") == True:
                                            target_monsters = "Ascended Solstice,Suffocated Light"
                                            
                                    if aura.get("nam") == "Sun's Heat":
                                        if aura.get("isNew") == True:
                                            stop_attack = True
                                            print_debug(f"stop_attack: {stop_attack}")
                            if auras.get("aura"):
                                aura = auras.get("aura")
                                if aura.get("nam") == "Sun's Heat":
                                    if auras.get("cmd") == "aura-":
                                        stop_attack = False
                                        print_debug(f"stop_attack: {stop_attack}")
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg")
                            if msg:
                                if log_taunt:
                                    print_debug(f"Received message: {msg}")
                                if "gather" in msg.lower():
                                    do_taunt = True
                                if  "sun converges" in msg.lower():
                                    converges_count += 1
                                    if converges_count % 2 != 0:
                                        do_taunt = True
                    if m:
                        for mon_map_id, mon_condition in m.items():
                            is_alive = int(mon_condition.get("intHP")) > 0
                            if (is_alive == False):
                                print(f"Monster id:{mon_map_id} is dead.")
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
            while stop_attack:
                # should do spam buff and heal here
                await cmd.sleep(500)
            if not is_attacking:
                print_debug(f"[{cmd.bot.player.CELL}] Attacking monsters...")
                is_attacking = True
            if do_taunt:
                if log_taunt:
                    print_debug(f"[{cmd.bot.player.CELL}] Doing taunt...")
                await cmd.sleep(1000)
                await cmd.use_skill(5, target_monsters=target_monsters)
                await cmd.sleep(1000)
                do_taunt = False
            else:
                await cmd.use_skill(skill_list[skill_index], target_monsters)
                skill_index += 1
                if skill_index >= len(skill_list):
                    skill_index = 0
            await cmd.sleep(100)
        is_attacking = False
        await to_next_cell()