import asyncio
import json
from datetime import datetime
from core.utils import is_valid_json
from core.commands import Command
from colorama import Fore

target_monsters = "Ascended Midnight"
stop_attack = False
do_taunt = False
log_taunt = False
converges_count = 0

# SLAVE MAID
async def main(cmd: Command):
    global target_monsters, stop_attack, do_taunt, log_taunt, converges_count
    
    def print_debug(message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {Fore.YELLOW}{message}{Fore.RESET}")
    
    async def go_to_master():
        if cmd.bot.follow_player and cmd.bot.followed_player_cell != cmd.bot.player.CELL:
            await cmd.bot.goto_player(cmd.bot.follow_player)
            await cmd.sleep(1000)
            
    def msg_taunt_handler(message):
        global target_monsters, stop_attack, do_taunt, log_taunt, converges_count
        if message:
            if is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
                cmd = data["cmd"]
                a = data.get("a") # Auras
                if a:
                    for auras in a:
                        cInf = auras.get("cInf")
                        if auras.get("auras"):
                            for aura in auras.get("auras"):
                                if aura.get("nam") == "Solar Flare":
                                    print_debug(f"{cInf} Aura: {aura.get('msgOn')}")
                                    if aura.get("isNew") == True:
                                        target_monsters = "Blessless Deer,Ascended Midnight"
                                        
                                if aura.get("nam") == "Moonveil":
                                    print_debug(f"{cInf} Aura: {aura.get('msgOn')}")
                                    if aura.get("isNew") == True:
                                        target_monsters = "Ascended Midnight"
                                        
                                if aura.get("nam") == "Sun's Heat":
                                    if aura.get("isNew") == True:
                                        stop_attack = True
                        if auras.get("aura"):
                            aura = auras.get("aura")
                            if aura.get("nam") == "Sun's Heat":
                                if auras.get("cmd") == "aura-":
                                    stop_attack = False
                if cmd == "ct":
                    anims = data.get("anims") # Animations
                    m = data.get("m") # Monster conditions
                    p = data.get("p") # Player conditions
                    if anims:
                        for anim in anims:
                            msg = anim.get("msg")
                            if msg:
                                if log_taunt:
                                    print_debug(f"Received message: {msg}")
                                if  "moon converges" in msg.lower():
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
    
    await go_to_master()
    
    print_debug("Waiting party invitation...")
    pid = await invitation_queue.get()
    print_debug(f"Accepting party invitation from PID: {pid}")
    await cmd.send_packet(f"%xt%zm%gp%1%pa%{pid}%")
    await cmd.sleep(1000)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    is_attacking = False
    
    while cmd.isStillConnected():
        print_debug("Going to master's place...")
        await go_to_master()
        await cmd.sleep(1000)
        while cmd.is_monster_alive():
            while stop_attack:
                await cmd.sleep(500)
            while stop_attack:
                print_debug(f"[{cmd.bot.player.CELL}] Stopping attack...")
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