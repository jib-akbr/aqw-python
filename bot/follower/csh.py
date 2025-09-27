from core.bot import Bot
from core.command import Command
from templates.hunt import hunt_item

async def main(cmd: Command):

    # await cmd.join_map("whitemap")

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

    # await cmd.equip_item("Legion Revenant")
    await cmd.register_quest(4432)

    skill_list = [3,0,3,0,2,0,3,0,3,0,4,1]
    skill_index = 0
    while cmd.is_still_connected():
        if cmd.bot.follow_player != "" and cmd.bot.followed_player_cell != cmd.bot.player.CELL:
            await cmd.bot.goto_player(cmd.bot.follow_player)
            await cmd.sleep(1000)
            continue 
        await cmd.wait_use_skill(skill_list[skill_index])
        skill_index += 1
        if skill_index >= len(skill_list):
            skill_index = 0
        await cmd.sleep(100)

if __name__ == "__main__":
    import asyncio
    login = input("Login (username,pass): ").split(",")
    # follow = input("player to follow: ")
    follow = "onodera_san"
    bot = Bot(cmdDelay=600,
              showDebug=True,
              autoRelogin=True,
              followPlayer=follow,
              isScriptable=True,
              restartOnAFK=True)  
    # run = Command(bot) 
    
    bot.set_login_info(login[0], login[1],"Safiria")  # Set login info

    asyncio.run(bot.start_bot(main))  # Run the main coroutine
