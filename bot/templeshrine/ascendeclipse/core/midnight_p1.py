import asyncio
import json
from datetime import datetime
from core.utils import is_valid_json
from core.commands import Command
from colorama import Fore

target_monsters = "Ascended Midnight"
stop_attack = False
do_taunt = True
log_taunt = False
converges_count = 0

# SLAVE MAID
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, log_taunt, converges_count
    
    def print_debug(message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}{message}{Fore.RESET}")
    
    async def go_to_master():
        global do_taunt, stop_attack, converges_count
        converges_count = 0 # reset converges count
        do_taunt = False # reset taunt
        stop_attack = False # reset stop attack
        
        if cmd.bot.follow_player:
            cmd.bot.jump_cell(cmd.bot.player.CELL, cmd.bot.player.PAD)
            await cmd.bot.ensure_leave_from_combat()
            await cmd.bot.goto_player(cmd.bot.follow_player)
            
    def msg_taunt_handler(message):
        global target_monsters, stop_attack, do_taunt, log_taunt, converges_count
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
                            msg = anim.get("msg")
                            if msg:
                                if  "moon converges" in msg.lower():
                                    converges_count += 1
                                    if converges_count % 2 != 0:
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
        await go_to_master()
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
        if cmd.bot.followed_player_cell != cmd.bot.player.CELL:
            print_debug(f"[{cmd.bot.player.CELL}] Going to master's place...")
            await go_to_master()
            await cmd.sleep(500)
            
        while cmd.is_monster_alive():
            target_monsters = "Ascended Midnight"
            stop_attack = cmd.bot.player.hasAura("Sun's Heat")
            
            while cmd.bot.player.ISDEAD:
                print_debug(f"[{cmd.bot.player.CELL}] player death...")
                is_attacking = False
                await cmd.sleep(500)
                
            if cmd.bot.player.hasAura("Sun's Heat"):
                target_monsters = "Moon Haze"
                
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
                await cmd.sleep(1000)
                do_taunt = False
            else:
                await cmd.use_skill(skill_list[skill_index], target_monsters, buff_only=stop_attack)
                skill_index += 1
                if skill_index >= len(skill_list):
                    skill_index = 0
            await cmd.sleep(100)
        is_attacking = False