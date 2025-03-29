import json
from core.bot import Bot
from core.commands import Command
from colorama import Fore
import time

speaker_counter = 0
taunter_class = None
zone_class = ""
what_zone = ""
force_taunt = False
force_skill = False
skill_to_force = 1
in_zone = False

force_heal = False
skill_to_heal = -1
equipped_class = ""

async def main(cmd: Command):
    global speaker_counter, taunter_class, zone_class, what_zone, force_taunt, force_skill, skill_to_force, in_zone, force_heal, skill_to_heal, equipped_class

    # fill weapon, helm, cape with item name
    equipment = {
        "legion revenant": {
            "class": "Legion Revenant",  # Arcana
            "weapon": "",  # Wizard
            "helm": "",  # Wizard
            "cape": ""  # Penitence
        },
        "archpaladin": {
            "class": "ArchPaladin",  # Lace
            "weapon": "",  # Luck
            "helm": "",  # Luck
            "cape": ""  # Penitence
        },
        "lord of order": {
            "class": "Lord of Order",  # Valiance
            "weapon": "",  # Luck
            "helm": "",  # Luck
            "cape": ""  # Penitence
        },
        "verus doomknight": {
            "class": "Verus DoomKnight",  # Dauntless
            "weapon": "",  # Luck
            "helm": "",  # Anima
            "cape": ""  # Penitence
        }
    }
    
    # will equip item base on the class you set for soloClass
    await equip_items(cmd, cmd.bot.soloClass, equipment)
    
    private_room_number = 9909
    
    await cmd.equip_scroll("Scroll of Enrage")

    await cmd.accept_quest(9173)
    await cmd.join_map("ultraspeaker", private_room_number)

    while not cmd.wait_count_player(4):
        await cmd.sleep(100)
    
    await cmd.use_skill(1)
    await cmd.sleep(1000)
    await cmd.use_skill(2)
    await cmd.sleep(1000)
    await cmd.use_skill(3)
    await cmd.sleep(1000)
    await cmd.jump_cell("Boss", "Left")

    # skill_list = [0,2,0,3,4] if bot.soloClass.lower() == "legion revenant" else [0,1,2,0,3,4]
    if cmd.bot.soloClass.lower() == "legion revenant":
        skill_list = [0,2,0,3,4]
    if cmd.bot.soloClass.lower() == "archpaladin":
        skill_list = [0,1,2,0,3,4]
    if cmd.bot.soloClass.lower() == "lord of order":
        skill_list = [0,1,2,0,3,4]
    if cmd.bot.soloClass.lower() == "verus doomknight":
        skill_list = [0,1,2,0,3,4]
    skill_index = 0

    # asyncio.create_task(message_handler(cmd.bot=cmd.bot))
    cmd.bot.subscribe(message_handler)
    equipped_class = cmd.get_equipped_class().item_name.lower()

    counter = 0

    start_time = time.time()

    while cmd.is_monster_alive("The First Speaker") and cmd.isStillConnected():
        mons_hp = cmd.get_monster_hp("The First Speaker")
        counter += 1
        if mons_hp > 9_990_000:
            speaker_counter = 0
        if mons_hp > -1 and counter >= 50:
            print("The First Speaker:", mons_hp)
            counter = 0
        try:
            equipped_class = equipped_class.item_name.lower()
        except:
            equipped_class = equipped_class.lower()
        # print("my hp:", cmd.bot.player.CURRENT_HP,"/", cmd.bot.player.MAX_HP, equipped_class)

        if taunter_class:
            if not force_taunt and equipped_class == taunter_class.lower():
                force_taunt = True
                continue
        
        if force_taunt:
            if not cmd.bot.player.canUseSkill(5):
                await cmd.sleep(100)
                continue
            print(equipped_class, "taunt")
            force_taunt = False
            taunter_class = None
            # await cmd.sleep(500)
            await cmd.use_skill(5, scroll_id=12917)

        if force_heal:
            force_heal = False
            await cmd.sleep(500)
            if skill_to_heal != -1:
                await cmd.use_skill(skill_to_heal)
                skill_to_heal = -1
        
        if force_skill and equipped_class == "legion revenant":
            await cmd.use_skill(1, "The First Speaker")
            force_skill = False
        
        if zone_class:
            if zone_class.lower() == equipped_class:
                if what_zone == "IN":
                    in_zone = True
                elif what_zone == "OUT":
                    in_zone = False
                zone_class = None
         
        if in_zone:
            if cmd.bot.player.getPlayerPositionXY()[0] != 203:
                print(Fore.BLUE + "I SOHULD IN ZONE" + Fore.WHITE)
                await cmd.walk_to(203, 301)
        elif in_zone == False:
            if cmd.bot.player.getPlayerPositionXY()[0] != 100:
                print(Fore.BLUE + "I SOHULD OUT ZONE" + Fore.WHITE)
                await cmd.walk_to(100, 321)

        # if cmd.bot.player.getPlayerPositionXY()[0] != 100:
        #     await cmd.walk_to(100, 321)
        
        if cmd.hp_below_percentage(60):
            equipped_class = cmd.get_equipped_class()
            if equipped_class:
                class_name = equipped_class.item_name.lower()
                if class_name == "archpaladin" or class_name == "lord of order":
                    await cmd.use_skill(2)
                elif class_name == "legion revenant":
                    await cmd.use_skill(3)

        # await cmd.use_skill(5, scroll_id=12917)
        await cmd.use_skill(skill_list[skill_index], "The First Speaker")
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        await cmd.sleep(100)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    # Convert to minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print(f"Elapsed time: {minutes} minutes, {seconds} seconds")
    
    await cmd.join_map("battleon", private_room_number)
    await cmd.turn_in_quest(9173)

    print("finished ultra speaker")
    await cmd.sleep(100000)

async def equip_items(cmd: Command, class_name: str, equipment: dict):
    class_name = class_name.lower()
    
    if class_name in equipment:
        items = equipment[class_name]
        await cmd.equip_item(items["class"])
        await cmd.equip_item(items["weapon"])
        await cmd.equip_item(items["helm"])
        await cmd.equip_item(items["cape"])

def message_handler(message):
    global speaker_counter, taunter_class, zone_class, what_zone, force_skill, skill_to_force, force_heal, skill_to_heal,equipped_class
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
            p = data.get("p")
            if p:
                for player in p.keys():
                    ply = p.get(player)
                    if ply:
                        hp = ply.get("intHP")
                        if hp:
                            if hp <= 2000:
                                try:
                                    equipped_class = equipped_class.item_name.lower()
                                except:
                                    equipped_class = equipped_class.lower()
                                if equipped_class:
                                    class_name = equipped_class
                                    if class_name == "archpaladin" or class_name == "lord of order":
                                        skill_to_heal = 2
                                        force_heal = True
                                    elif class_name == "legion revenant":
                                        skill_to_heal = 3
                                        force_heal = True
            if anims:
                for anim in anims:
                    msg = anim.get("msg")
                    if msg:
                        # print(msg)
                        if "truth" in msg or "listen" in msg:
                            whoTaunt, whoZone, whatZone, delay = malgorHandler()
                            # print(speaker_counter)
                            speaker_counter += 1
                            taunter_class = whoTaunt
                            zone_class = whoZone
                            what_zone = whatZone
        elif cmd == "event":
            print(Fore.GREEN + data["args"]["zoneSet"] + Fore.WHITE)
            if data["args"]["zoneSet"] == "A":
                force_skill = True
                skill_to_force = 1

def malgorHandler():
    global speaker_counter
    if speaker_counter == 0:
        return ("Legion Revenant", None, None, 0)
    elif speaker_counter == 1:
        return ("Lord Of Order", "Verus DoomKnight", "IN", 0)
    elif speaker_counter == 2:
        return ("ArchPaladin", "Verus DoomKnight", "OUT", 0)
    elif speaker_counter == 3 or speaker_counter == 7:
        return ("Lord Of Order", None, None, 500)
    elif speaker_counter == 4:
        return (None, "Legion Revenant", "IN", 0)
    elif speaker_counter == 5:
        return ("Legion Revenant", "Legion Revenant", "OUT", 500)
    elif speaker_counter == 8:
        return (None, "ArchPaladin", "IN", 0)
    elif speaker_counter == 9:
        return ("ArchPaladin", "ArchPaladin", "OUT", 0)
    elif speaker_counter == 10:
        return ("Legion Revenant", None, None, 500)
    elif speaker_counter == 11:
        return (None, "Lord Of Order", "IN", 0)
    elif speaker_counter == 12:
        return ("Lord Of Order", "Lord Of Order", "OUT", 500)
    elif speaker_counter == 14:
        return ("Legion Revenant", None, None, 0)
    elif speaker_counter == 15:
        speaker_counter = 1  # Resetting speaker_counter to 1
        return ("Lord Of Order", "Verus DoomKnight", "IN", 500)
    
    return (None, None, None, 0)

def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False