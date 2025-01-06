from core.bot import Bot
from templates.hunt import hunt_item_cmds
from templates.general import un_bank_items
import commands as cmd
import asyncio

# Initialize variables
item_qty = 20
label_farming = f"Farming for Revenant's Spellscroll {item_qty}x"
private_room_number = 99999
white_list_items = [
        "Aeacus Empowered",
        "Tethered Soul",
        "Darkened Essence",
        "Dracolich Contract",
        "Revenant's Spellscroll"
      ]

# Initialize bot
b = Bot(
    roomNumber=None, 
    itemsDropWhiteList=white_list_items, 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)
b.set_login_info("u", "p", "alteon")

# Arrange commands
b.add_cmds([
        # *un_bank_items(white_list_items),
        cmd.RegisterQuestCmd(6897),
        cmd.SleepCmd(1000),
        cmd.LabelCmd(label_farming),
        cmd.IsInInvCmd(itemName="Revenant's Spellscroll", itemQty=item_qty, operator=">="),
        cmd.StopBotCmd(),
        *hunt_item_cmds(
            item_name = "Dracolich Contract",
            item_qty = 1000,
            map_name = "necrodungeon",
            room_number = private_room_number,
            cell = "r22",
            pad = "Down",
            monster_name = "id.49,id.50,id.46,id.47"
        ),
        *hunt_item_cmds(
            item_name = "Tethered Soul",
            item_qty = 300,
            map_name = "revenant",
            room_number = None,
            cell = "r2",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Aeacus Empowered",
            item_qty = 50,
            map_name = "judgement",
            room_number = None,
            cell = "r10a",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Darkened Essence",
            item_qty = 500,
            map_name = "shadowrealmpast",
            room_number = None,
            cell = "Enter",
            pad = "Spawn",
            monster_name = "*"
        ),
        cmd.ToLabelCmd(label_farming)
    ])

# Start bot
asyncio.run(b.start_bot())