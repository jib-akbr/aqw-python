from core.bot import Bot
from core.commands import Command
import asyncio
from templates.hunt import hunt_item, attack_script

async def main(bot: Bot):
    cmd = Command(bot)
    private_room_number = 1231

    if bot.farmClass:
        await cmd.equip_item(bot.farmClass)
        await cmd.equip_item_by_enhancement(enh_pattern_id=29) # 29 for penitence
        await cmd.equip_item_by_enhancement(enh_pattern_id=10) # 10 for valiance
    
    await cmd.ensure_accept_quest(8154)
    await cmd.join_map("ultraengineer", private_room_number)
    await cmd.jump_cell("r2", "Left")

    while not cmd.wait_count_player(4):
        await asyncio.sleep(0.1)

    while cmd.is_monster_alive("Ultra Engineer") and cmd.isStillConnected():
        await attack_script(cmd, "Defense Drone,Attack Drone,Ultra Engineer")
    
    await cmd.join_map("battleon", private_room_number)

    print("finished ultra engineer")
    await cmd.sleep(100000)