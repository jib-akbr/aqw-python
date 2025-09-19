from core.bot import Bot
from templates.hunt import hunt_item_cmds
import commands as cmd
import asyncio

# Initialize bot
b = Bot(
    roomNumber=None, 
    itemsDropWhiteList=["Legion Token"], 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)
b.set_login_info("u", "p", "yorumi")

# Initialize variables
private_room_number = 1

# Arrange commands
b.add_cmds([
        cmd.AcceptQuestCmd(6743),
        cmd.SleepCmd(1000),
        *hunt_item_cmds(
            item_name = "Axeros' Brooch",
            item_qty = 1,
            map_name = "legionarena",
            room_number = private_room_number,
            cell = "Boss",
            pad = "Left",
            monster_name = "*"
        ),
        cmd.TurnInQuestCmd(6743),
        cmd.SleepCmd(1000)
    ])

# Start bot
asyncio.run(b.start_bot())