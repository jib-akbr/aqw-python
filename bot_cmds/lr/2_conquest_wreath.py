from core.bot import Bot
from templates.hunt import hunt_item_cmds
from templates.general import un_bank_items
import commands as cmd
import asyncio

# Initialize variables
item_qty = 6
label_farming = f"Farming for Conquest Wreath {item_qty}x"
private_room_number = 99999
white_list_items = [
        "Grim Cohort Conquered",
        "Ancient Cohort Conquered",
        "Pirate Cohort Conquered",
        "Battleon Cohort Conquered",
        "Mirror Cohort Conquered",
        "Darkblood Cohort Conquered",
        "Vampire Cohort Conquered",
        "Spirit Cohort Conquered",
        "Dragon Cohort Conquered",
        "Doomwood Cohort Conquered",
        "Conquest Wreath"
      ]
quest_item_qty = 400

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
        *un_bank_items(white_list_items),
        cmd.RegisterQuestCmd(6898),
        cmd.SleepCmd(1000),
        cmd.LabelCmd(label_farming),
        cmd.IsInInvCmd(itemName="Conquest Wreath", itemQty=item_qty, operator=">="),
        cmd.StopBotCmd(),
        *hunt_item_cmds(
            item_name = "Grim Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "doomvault",
            room_number = private_room_number,
            cell = "r3",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Ancient Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "mummies",
            room_number = private_room_number,
            cell = "r2",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Pirate Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "wrath",
            room_number = private_room_number,
            cell = "r7",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Battleon Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "doomwar",
            room_number = private_room_number,
            cell = "r6",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Mirror Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "overworld",
            room_number = private_room_number,
            cell = "Enter",
            pad = "Spawn",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Vampire Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "maxius",
            room_number = private_room_number,
            cell = "r2",
            pad = "Left",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Dragon Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "dragonbone",
            room_number = private_room_number,
            cell = "Enter",
            pad = "Spawn",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Doomwood Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "doomwood",
            room_number = private_room_number,
            cell = "r6",
            pad = "Right",
            monster_name = "*"
        ),
        *hunt_item_cmds(
            item_name = "Spirit Cohort Conquered",
            item_qty = quest_item_qty,
            map_name = "curseshore",
            room_number = private_room_number,
            cell = "r2",
            pad = "Left",
            monster_name = "*"
        ),
        cmd.ToLabelCmd(label_farming)
    ])

# Start bot
asyncio.run(b.start_bot())