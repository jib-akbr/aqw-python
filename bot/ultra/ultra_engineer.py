from core.bot import Bot
from core.commands import Command

async def main(cmd: Command):
    private_room_number = 1231

    if cmd.bot.soloClass:
        await cmd.equip_item(cmd.bot.soloClass)
        await cmd.equip_item_by_enhancement(enh_pattern_id=29) # 29 for penitence
        await cmd.equip_item_by_enhancement(enh_pattern_id=10) # 10 for valiance
    
    await cmd.ensure_accept_quest(8154)
    await cmd.join_map("ultraengineer", private_room_number)
    await cmd.jump_cell("r2", "Left")

    while not cmd.wait_count_player(4):
        await cmd.sleep(100)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    while cmd.is_monster_alive("Ultra Engineer") and cmd.is_still_connected():
        if cmd.hp_below_percentage(60):
            equipped_class = cmd.get_equipped_class()
            if equipped_class:
                class_name = equipped_class.item_name.lower()
                if class_name == "archpaladin" or class_name == "lord of order":
                    await cmd.use_skill(2)
                elif class_name == "legion revenant":
                    await cmd.use_skill(3)
        await cmd.use_skill(skill_list[skill_index], "Defense Drone,Attack Drone,Ultra Engineer")
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        await cmd.sleep(100)
    
    await cmd.join_map("battleon", private_room_number)
    await cmd.turn_in_quest(8154)

    print("finished ultra engineer")
    await cmd.sleep(100000)