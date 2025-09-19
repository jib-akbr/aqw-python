from core.bot import Bot
from templates.attack import generalAttack
import commands as cmd
import asyncio

# Initialize bot
b = Bot(
    roomNumber=9099, 
    itemsDropWhiteList=[
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
    ], 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True,
    followPlayer="followed_player_name")
b.set_login_info("u", "p", "alteon")

# Arrange commands
b.add_cmds([
        cmd.RegisterQuestCmd(4432),
        cmd.LabelCmd("ATK"),
        *generalAttack,
        cmd.ToLabelCmd("ATK"),
        cmd.StopBotCmd()
    ])

# Start bot
asyncio.run(b.start_bot())