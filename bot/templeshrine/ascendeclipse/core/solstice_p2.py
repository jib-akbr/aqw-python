import asyncio
import json
from datetime import datetime
from core.utils import is_valid_json
from core.commands import Command
from colorama import Fore
from .core_temple import *

pid = None
target_monsters = "Ascended Solstice"
stop_attack = False
do_taunt = False
taunt_target = None
log_taunt = True
converges_count = 0

# SLAVE MAID
async def main(cmd: Command):
    global pid, target_monsters, stop_attack, do_taunt, taunt_target, log_taunt, converges_count
    
    def reset_counters():
        global do_taunt, stop_attack, converges_count
        converges_count = 0 # reset converges count
        do_taunt = False # reset taunt
        stop_attack = False # reset stop attack
            
    def msg_handler(message):
        global target_monsters, pid, stop_attack, do_taunt, taunt_target, log_taunt, converges_count
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                cmdData = data["cmd"]
                if cmdData =="pi":
                    pid = data.get("pid")
                if cmdData == "ct":
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
                                    if aura.get("nam") == "Sun's Warmth":
                                        # Start a background task to set do_taunt after 5 seconds
                                        async def delayed_taunt():
                                            global do_taunt, taunt_target
                                            await asyncio.sleep(5)
                                            do_taunt = True
                                            taunt_target = "Sunset Knight"
                                        asyncio.create_task(delayed_taunt())
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg", "").lower()
                            if "sun converges" in msg:
                                converges_count += 1
                                do_taunt = converges_count % 2 == 0
                                if log_taunt:
                                    print_debug(f"Converges count: {converges_count}")
                    if m:
                        for mon_map_id, mon_condition in m.items():
                            monHp = int(mon_condition.get('intHP'))
                            is_alive = monHp > 0
                            if (is_alive == False):
                                print_debug(f"Monster id:{mon_map_id} is dead.")
                                
                            if monHp:
                                mon = cmd.get_monster(f"id.{mon_map_id}")
                                monHpPercent = round(((mon.current_hp/mon.max_hp)*100), 2)
                                # print_debug2(f"id.{mon_map_id} - {mon.mon_name} HP: {monHpPercent}%")
            except:
                return
    cmd.bot.subscribe(msg_handler)
    
    await prepare_items(cmd)
    
    print_debug("Waiting for party invitation...")
    while pid is None:
        await go_to_master(cmd)
        await cmd.sleep(1000)
    print_debug(f"Accepting party invitation from PID: {pid}")
    await cmd.send_packet(f"%xt%zm%gp%1%pa%{pid}%")
    await cmd.sleep(1000)

    skill_list = [0,1,2,3,4]
    skill_index = 0
    is_attacking = False
    
    while cmd.isStillConnected():
        reset_counters()
        await go_to_master(cmd)

        if cmd.bot.player.CELL == "r3a":
            await cmd.rest()
            await cmd.sleep(8000)
            
        # if cmd.bot.player.CELL =="Enter" or cmd.bot.player.CELL =="r1":
        #     await cmd.equip_item("Legion Revenant")
        # else:
        #     await cmd.equip_item("StoneCrusher")
            
        master = cmd.get_player_in_map(cmd.bot.follow_player)
        while cmd.is_monster_alive() and master.str_frame == cmd.bot.player.CELL:
            stop_attack = cmd.bot.player.hasAura("Sun's Heat")

            target_monsters = "Ascended Solstice,Blessless Deer"
            # if cmd.bot.player.hasAura("Solar Flare"):
            #     target_monsters = "Blessless Deer"
            # else:
            #     target_monsters = "Ascended Solstice"
            
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
            await skill_delay(cmd)
        is_attacking = False