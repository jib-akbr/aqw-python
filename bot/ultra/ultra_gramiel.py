from core.bot import Bot
from core.commands import Command
import time, json
from datetime import datetime, timedelta

# SETUP MANUALLY
# LC (Valiance, Wizard Class, Forge Helm, Penitence, 51% Dmg)
# LOO (Arcana's Concerto, Luck Class, Healer Helm, Absolution, 51% Dmg)
# PCM (Luck Mana Vamp, Healer Class, Lucky Helm, Penitence, 51% Dmg)
# SC (Valiance, Wizard Class, Wizard Helm, Penitence, 51% Dmg)

LTaunt = 0
RTaunt = 0
LTauntClass = ""
RTauntClass = ""
force_taunt = False
cmdGlobal: Command = None
taunter_list: list[str] = ["obsidian paladin chronomancer", "stonecrusher", "lightcaster", "lord of order"]
taunter_index: int = 0
taunt_date: datetime = datetime.now()
wait_taunt: bool = False

async def main(cmd: Command):
    cmd.bot.showDebug = True
    cmd.bot.auto_relogin = False
    global LTaunt, RTaunt, LTauntClass, RTauntClass, force_taunt, cmdGlobal, taunter_list, taunter_index, wait_taunt, taunt_date
    cmdGlobal = cmd
    private_room_number = 9909

    cmd.add_drop("Gramiel the Graceful's Insignia")

    await cmd.ensure_accept_quest(10301)
    await cmd.equip_scroll("Scroll of Enrage")
    while cmd.is_not_in_map("ultragramiel"):
        await cmd.join_map("ultragramiel", private_room_number)
        await cmd.sleep(1000)
    await cmd.jump_cell("Enter", "Spawn")


    while not cmd.wait_count_player(4):
        await cmd.sleep(100)
    
    await cmd.use_skill(1)
    await cmd.sleep(1000)
    await cmd.use_skill(2)
    await cmd.sleep(1000)
    await cmd.use_skill(3)
    await cmd.sleep(1000)

    await cmd.jump_cell("r2", "Bottom")

    skill_index = 0
    skill_list = [0,1,2,0,3,4]

    cmd.bot.subscribe(message_handler)

    start_time = time.time()
    print("attacking...")
    equipped_class = cmd.get_equipped_class().item_name.lower()

    if equipped_class == "obsidian paladin chronomancer" or equipped_class == "stonecrusher":
        priority = ["id.2", "id.3"]
    if equipped_class == "lightcaster" or equipped_class == "lord of order":
        priority = ["id.3", "id.2"]

    for prio in priority:
        while cmd.is_monster_alive(prio) and cmd.isStillConnected():
            mons_hp = cmd.get_monster_hp(prio)
            if mons_hp > -1:
                print(f"{prio}: {mons_hp} : {cmd.get_monster_hp_percentage(prio)}%")
            if force_taunt:
                await cmd.sleep(1000)
                await cmd.use_skill(5, prio)
                print(f"{equipped_class} taunt 2")
                force_taunt = False
                continue
            await cmd.use_skill(skill_list[skill_index], prio)
            skill_index += 1
            if skill_index >= len(skill_list):
                skill_index = 0
            await cmd.sleep(100)
    
    force_taunt = False

    if equipped_class == taunter_list[taunter_index]:
        wait_taunt = True
        taunt_date = datetime.now()
    while cmd.is_monster_alive("Gramiel The Graceful") and cmd.isStillConnected():
        mons_hp = cmd.get_monster_hp("Gramiel The Graceful")
        if mons_hp > -1:
            print(f"Gramiel The Graceful: {mons_hp} : {cmd.get_monster_hp_percentage('Gramiel The Graceful')}%")
        if wait_taunt:
            if datetime.now() >= taunt_date:
                force_taunt = True
                wait_taunt = False
        if force_taunt:
            await cmd.sleep(1200)
            await cmd.use_skill(5, "Gramiel The Graceful")
            print(f"{equipped_class} taunt Gramiel The Graceful")
            force_taunt = False
            continue
        await cmd.use_skill(skill_list[skill_index], "Gramiel The Graceful")
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        await cmd.sleep(100)

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print(f"Elapsed time: {minutes} minutes, {seconds} seconds")
    await cmd.turn_in_quest(10301)
    while cmd.is_not_in_map("whitemap"):
        await cmd.join_map("whitemap", private_room_number)
        await cmd.sleep(1000)
    cmd.stopBot("finished Gramiel The Graceful")

def message_handler(message):
    global LTaunt, RTaunt, LTauntClass, RTauntClass, force_taunt, cmdGlobal, taunter_list, taunter_index, wait_taunt, taunt_date
    cmdG: Command = cmdGlobal
    if message:
        if is_valid_json(message):
            data = json.loads(message)
        try:
            data = data["b"]["o"]
        except:
            return
        cmd = data["cmd"]
        if cmd == "ct":
            anims = data.get("anims")
            if anims:
                for anim in anims:
                    msg: str = anim.get("msg")
                    animStr: str = anim.get("animStr")
                    target = anim["tInf"]
                    equipped_class = cmdG.get_equipped_class().item_name.lower()

                    if msg and isinstance(msg, str):
                        if msg.lower() == "The Grace Crystal prepares a defense shattering attack!".lower():
                            if target == "m:3":
                                RTaunt += 1
                                if RTaunt % 2 == 0 and equipped_class == "lord of order":
                                    force_taunt = True
                                elif RTaunt % 2 == 1 and equipped_class == "lightcaster":
                                    force_taunt = True
                            if target == "m:2":
                                LTaunt += 1
                                if LTaunt % 2 == 0 and equipped_class == "obsidian paladin chronomancer":
                                    force_taunt = True
                                elif LTaunt % 2 == 1 and equipped_class == "stonecrusher":
                                    force_taunt = True
                    if msg and isinstance(msg, list):
                        print(msg)
                    
                    if animStr:
                        if animStr == "Point" and target == "m:1":
                            taunter_index += 1
                            if taunter_index >= len(taunter_list):
                                taunter_index = 0
                            
                            if equipped_class == taunter_list[taunter_index]:
                                wait_taunt = True
                                taunt_date = datetime.now() + timedelta(seconds=4)

def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False