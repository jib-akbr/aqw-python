from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item

async def main(cmd: Command):

    await cmd.join_map("whitemap")

    item_list = [
        "Astral Ephemerite Essence",
        "Belrot the Fiend Essence",
        "Black Knight Essence",
        "Tiger Leech Essence",
        "Carnax Essence",
        "Chaos Vordred Essence",
        "Dai Tengu Essence",
        "Unending Avatar Essence",
        "Void Dragon Essence",
        "Creature Creation Essence",
        "Void Aura"
    ]

    await cmd.bank_to_inv(item_list)   

    cmd.add_drop(item_list) 

    await cmd.equip_item("Legion Revenant")
    await cmd.register_quest(4432)

    skill_list = [0,1,2,0,3,4]
    skill_index = 0
    while cmd.isStillConnected():
        if cmd.bot.follow_player != "" and cmd.bot.followed_player_cell != cmd.bot.player.CELL:
            await cmd.bot.goto_player(cmd.bot.follow_player)
            await cmd.sleep(1000)
            continue 
        await cmd.use_skill(skill_list[skill_index])
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        await cmd.sleep(100)