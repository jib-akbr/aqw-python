from core.bot import Bot
from templates.hunt import hunt_item_cmds
from templates.general import un_bank_items
from templates.attack import attack_monster
import commands as cmd
import asyncio

# Initialize variables
item_qty = 10
label_farming = f"Farming for Exalted Crown {item_qty}x"
private_room_number = 9999909
white_list_items = [
        "Dage's Favor",
        "Diamond Token of Dage",
        "Emblem of Dage",
        "Dark Token",
        "Exalted Crown",
        "Legion Seal",
        "Gem of Mastery",
        "Defeated Makai",
        "Legion Token"
        "Legion Round 4 Medal"
      ]

# Initialize bot
b = Bot(
    roomNumber=None, 
    itemsDropWhiteList=white_list_items, 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)
b.set_login_info("u", "u", "alteon")

def get_Hooded_Legion_Cowl():
    item = "Hooded Legion Cowl"
    return [
        cmd.IsInInvCmd(itemName=item),
        cmd.DownIndexCmd(3),
        cmd.JoinMapCmd("underworld", roomNumber=private_room_number),
        cmd.BuyItemCmd(item_name=item, qty=1, shop_id=216)
    ]
    
def get_Dages_Favor(qty: int = 300):
    item = "Dage's Favor"
    return [
        *hunt_item_cmds(
            item_name=item,
            item_qty=qty,
            map_name="underworld",
            room_number=private_room_number,
            cell="r8",
            pad="Left"
        )
    ]
    
# Legion Round 4 Medal 'MUST' be in inventory
def get_Emblem_of_Dage(qty: int = 1):
    item = "Emblem of Dage"
    label_farming = f"Farming for {item} {qty}x"
    label_done = f"DONE farming for {item} {qty}x"
    return [
        cmd.IsInInvCmd("Legion Round 4 Medal", operator="<", itemQty=1),
        cmd.StopBotCmd("Required : Legion Round 4 Medal in inventory"),
        cmd.LabelCmd(label_farming),
        cmd.AcceptQuestCmd(4742),
        cmd.IsInInvCmd(itemName=item, itemQty=qty),
        cmd.ToLabelCmd(label_done),
        *hunt_item_cmds(
            item_name="Legion Seal",
            item_qty=25,
            map_name="shadowblast",
            room_number=private_room_number,
            cell="r10",
            pad="Left",
            monster_name="Doombringer"
        ),
        *hunt_item_cmds(
            item_name="Gem of Mastery",
            item_qty=1,
            map_name="shadowblast",
            room_number=private_room_number,
            cell="r10",
            pad="Left",
            monster_name="Carnage"
        ),
        cmd.TurnInQuestCmd(4742),
        cmd.ToLabelCmd(label_farming),
        cmd.LabelCmd(label_done)
    ]
    
def get_Diamond_Token_of_Dage(qty: int = 30):
    item = "Diamond Token of Dage"
    label_farming_dtd = f"Farming for {item} {qty}x"
    label_done = f"DONE farming for {item} {qty}x"
    return [
        cmd.LabelCmd(label_farming),
        cmd.AcceptQuestCmd(4743),
        cmd.IsInInvCmd(itemName=item, itemQty=qty),
        cmd.ToLabelCmd(label_done),
        cmd.JoinMapCmd("citadel", roomNumber=private_room_number),
        cmd.JumpCmd("m22", "Left"),
        *hunt_item_cmds(
            item_name="Defeated Makai",
            item_qty=25,
            map_name="tercessuinotlim",
            room_number=private_room_number,
            cell="m2",
        ),
        *hunt_item_cmds(
            item_name="Carnax Eye",
            item_qty=1,
            map_name="aqlesson",
            room_number=None,
            cell="Frame9",
            pad="Right"
        ),
        *hunt_item_cmds(
            item_name="Red Dragon's Fang",
            item_qty=1,
            map_name="lair",
            room_number=private_room_number,
            cell="End",
            pad="Left"
        ),
        *hunt_item_cmds(
            item_name="Kathool Tentacle",
            item_qty=1,
            map_name="deepchaos",
            room_number=None,
            cell="Frame4",
            pad="Left"
        ),
        *hunt_item_cmds(
            item_name="Fluffy's Bones",
            item_qty=1,
            map_name="dflesson",
            room_number=None,
            cell="r12",
            pad="Right"
        ),
        *hunt_item_cmds(
            item_name="Blood Titan's Blade",
            item_qty=1,
            map_name="bloodtitan",
            room_number=None,
            cell="Enter",
            pad="Spawn"
        ),
        cmd.TurnInQuestCmd(4743),
        cmd.ToLabelCmd(label_farming),
        cmd.LabelCmd(label_done)
    ]

def get_Dark_Token(qty: int = 100):
    item = "Dark Token"
    label_farming = f"Farming for {item} {qty}x"
    label_done = f"DONE farming for {item} {qty}x"
    return [
        cmd.JoinMapCmd("seraphicwardage", roomNumber=private_room_number),
        cmd.JumpCmd("Enter", "Spawn"),
        cmd.RegisterQuestCmd(6248),
        cmd.RegisterQuestCmd(6249),
        cmd.LabelCmd(label_farming),
        cmd.IsInInvCmd(itemName=item, itemQty=qty),
        cmd.ToLabelCmd(label_done),
        *attack_monster(),
        *attack_monster(),
        *attack_monster(),
        cmd.ToLabelCmd(label_farming),
        cmd.LabelCmd(label_done)
    ]
    
def get_Legion_Token(qty: int = 4000):
    item = "Legion Token"
    label_farming = f"Farming for {item} {qty}x"
    label_done = f"DONE farming for {item} {qty}x"
    
    via_shogun_paragon_pet = []
    via_legion_arena = [
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
    ]
    
    return [
        cmd.LabelCmd(label_farming),
        cmd.IsInInvCmd(itemName=item, itemQty=qty),
        cmd.ToLabelCmd(label_done),
        *via_legion_arena,
        cmd.ToLabelCmd(label_farming),
        cmd.LabelCmd(label_done)
    ]

# Arrange commands
b.add_cmds([
        # *un_bank_items(white_list_items),
        cmd.RegisterQuestCmd(6899),
        cmd.SleepCmd(1000),
        cmd.LabelCmd(label_farming),
        cmd.IsInInvCmd(itemName="Exalted Crown", itemQty=item_qty, operator=">="),
        cmd.StopBotCmd(),
        *get_Legion_Token(),
        *get_Emblem_of_Dage(),
        *get_Diamond_Token_of_Dage(),
        *get_Dages_Favor(),
        *get_Dark_Token(),
        *get_Hooded_Legion_Cowl(),
        cmd.ToLabelCmd(label_farming)
    ])

# Start bot
loop = asyncio.get_event_loop()
loop.run_until_complete(b.start_bot())