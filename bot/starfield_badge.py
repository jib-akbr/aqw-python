from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)
    item_qty = 1_000_000

    await cmd.bank_to_inv("Stars Destroyed")

    cmd.add_drop("Stars Destroyed")

    await cmd.join_map("starfield")

    if bot.farmClass:
        await cmd.equip_item(bot.farmClass)

    await cmd.ensure_accept_quest(9818)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    while cmd.is_in_inventory("Stars Destroyed", item_qty, "<") and cmd.isStillConnected():
        await cmd.use_skill(skill_list[skill_index])
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
