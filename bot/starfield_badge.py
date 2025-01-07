from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)
    item_qty = 1_000_000
    item_name = "Stars Destroyed"

    await cmd.bank_to_inv(item_name)

    cmd.add_drop(item_name)

    await cmd.join_map("starfield")

    await cmd.jump_cell("r3", "Spawn")

    if bot.farmClass:
        await cmd.equip_item(bot.farmClass)

    await cmd.ensure_accept_quest(9818)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    counter = 0
    while cmd.is_in_inventory(item_name, item_qty, "<") and cmd.isStillConnected():
        if counter >= 50:
            cmd.farming_logger(item_name, item_qty)
            counter = 0
        await cmd.use_skill(skill_list[skill_index])
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        counter += 1
