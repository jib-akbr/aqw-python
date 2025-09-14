import time
import json
from datetime import datetime
from core.commands import Command
from core.utils import is_valid_json
from colorama import Fore
from .core_temple import *
    
target_monsters = "Ascended Solstice,Suffocated Light"
stop_attack = False
do_taunt = False
taunt_target = None
timeleapse = 0
log_taunt = True

deerHp = 100 # in percentage
cleared_count = 0
converges_count = 0
light_gather_count = 0
sun_warmth_count = 0
moonlight_gaze_count = 0

# PARTY LEADER
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, taunt_target, timeleapse, log_taunt, cleared_count, converges_count, light_gather_count, sun_warmth_count, moonlight_gaze_count, deerHp
        
    async def enter_dungeon():
        global timeleapse
        timeleapse = time.monotonic() 
        await cmd.send_packet("%xt%zm%dungeonQueue%25127%ascendeclipse%")
        while cmd.is_not_in_map("ascendeclipse"):
            print_debug("Waiting for dungeon queue...")
            await cmd.sleep(500)
        
    async def to_next_cell():
        global do_taunt, stop_attack, timeleapse, deerHp, cleared_count, converges_count, light_gather_count, sun_warmth_count, moonlight_gaze_count
        do_taunt = False # reset taunt
        stop_attack = False # reset stop attack
        converges_count = 0 # reset converges count
        light_gather_count = 0 # reset light gather count
        sun_warmth_count = 0 # reset Sun's Warmth count
        moonlight_gaze_count = 0 # reset Moonlight Gaze count
        deerHp = 100 # reset deer HP

        # check all slaves are ready
        if cmd.bot.player.CELL != "Enter":
            cmd.jump_cell("Enter", "Spawn")
            for slave in cmd.bot.slaves_player:
                player = cmd.get_player_in_map(slave)
                if player:
                    hpPercent = round(((player.int_hp/player.int_hp_max)*100), 2) if player.int_hp_max != 0 else 0
                    print_debug(f"Checking {slave} - Cell: {player.str_frame}, State: {player.int_state}, HP: {player.int_hp}")
                    while player.str_frame != cmd.bot.player.CELL or player.int_state == 0:
                            await cmd.sleep(100)
                            player = cmd.get_player_in_map(slave)
                    await cmd.sleep(500)
        
        print_debug(f"Moving to next cell...")
        cmd.bot.respawn_cell_pad = None
        await cmd.sleep(2000)
        if cmd.bot.player.CELL == "Enter":
            if not cmd.get_monster("Blessless Deer").is_alive and not cmd.get_monster("Fallen Star").is_alive:
                await cmd.jump_cell("r1", "Left")
        elif cmd.bot.player.CELL == "r1":
            if not cmd.get_monster("Suffocated Light").is_alive and not cmd.get_monster("Imprisoned Fairy").is_alive:
                await cmd.jump_cell("r2", "Left")
        elif cmd.bot.player.CELL == "r2":
            if not cmd.get_monster("Sunset Knight").is_alive and not cmd.get_monster("Moon Haze").is_alive:
                cmd.bot.respawn_cell_pad = ["Enter", "Spawn"]
                await cmd.jump_cell("r3", "Left")
        elif cmd.bot.player.CELL == "r3":
            if not cmd.get_monster("Ascended Midnight").is_alive and not cmd.get_monster("Ascended Solstice").is_alive:
                await cmd.jump_cell("r3a", "Left")
        elif cmd.bot.player.CELL == "r3a":
            elapsed_seconds = time.monotonic() - timeleapse
            minutes = int(elapsed_seconds // 60)
            seconds = int(elapsed_seconds % 60)
            cleared_count += 1
            await cmd.send_chat(f"Total time taken: {minutes} minutes and {seconds} seconds.")
            await cmd.sleep(1000)
            await cmd.send_chat(f"Dungeon cleared {cleared_count} times.")

            print_debug(f"Resting for 10 secs...")
            await cmd.rest()
            await cmd.sleep(10000)

            print_debug(f"Entering new queue...")
            await cmd.join_map("yulgar", roomNumber=999999)
            await cmd.sleep(4000)
            await enter_dungeon()
        
    def msg_taunt_handler(message):
        global do_taunt, taunt_target, deerHp, converges_count, light_gather_count, sun_warmth_count, moonlight_gaze_count
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
                        for a_item in a:
                            for aura in a_item.get("auras", []):
                                if cmd.bot.user_id in a_item.get("tInf", ""):
                                    if aura.get("nam") == "Sun's Heat":
                                        print_debug("Sun's Heat") 
                                    if aura.get("nam") == "Moonlight Stun":
                                        print_debug("Moonlight Stun")
                                    # if aura.get("nam") == "Sun's Warmth":
                                    #     sun_warmth_count += 1
                                    #     if sun_warmth_count % 2 != 0:
                                    #         do_taunt = True
                                    #         taunt_target = f"Sunset Knight,{sun_warmth_count}"
                                    # if aura.get("nam") == "Moonlight Gaze":
                                    #     moonlight_gaze_count += 1
                                    #     if moonlight_gaze_count % 2 == 0:
                                    #         do_taunt = True
                                    #         taunt_target = "Moon Haze"
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg", "").lower()
                            if "gather" in msg:
                                light_gather_count += 1
                                do_taunt = light_gather_count % 2 != 0
                            if  "sun converges" in msg.lower():
                                converges_count += 1
                                do_taunt = converges_count % 2 != 0
                    if m:
                        for mon_map_id, mon_condition in m.items():
                            monHp = int(mon_condition.get('intHP'))
                            # if monHp:
                            #     mon = cmd.get_monster(f"id.{mon_map_id}")
                            #     monHpPercent = round(((mon.current_hp/mon.max_hp)*100), 2)
                            #     print_debug2(f"id.{mon_map_id} - {mon.mon_name} HP: {monHpPercent}%")
                            is_alive = monHp > 0
                            if (is_alive == False):
                                print_debug(f"Monster id:{mon_map_id} is dead.")
            except:
                return
    cmd.bot.subscribe(msg_taunt_handler)
    
    # Initial setup
    await cmd.join_map("yulgar", roomNumber=999999)
    await cmd.sleep(4000)
    await prepare_items(cmd)
    
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
            if cmd.bot.player.ISDEAD:
                is_attacking = False
                print_debug("You are dead. Waiting to respawn...", Fore.RED)
                await cmd.sleep(1000)
                break

            stop_attack = cmd.bot.player.hasAura("Sun's Heat")

            if cmd.bot.player.hasAura("Solar Flare"):
                target_monsters = "Blessless Deer"
            else:
                target_monsters = "Ascended Solstice"

            if not is_attacking:
                print_debug(f"[{cmd.bot.player.CELL}] Attacking monsters...")
                is_attacking = True
            if do_taunt:
                if taunt_target is None:
                    await use_taunt(cmd, target_monsters=target_monsters, show_log=log_taunt)
                else:
                    await use_taunt(cmd, target_monsters=taunt_target, show_log=log_taunt)
                    taunt_target = None
                do_taunt = False
            else:
                await cmd.use_skill(skill_list[skill_index], target_monsters, buff_only=stop_attack)
                skill_index += 1
                if skill_index >= len(skill_list):
                    skill_index = 0
            await cmd.sleep(200)
        is_attacking = False
        await to_next_cell()