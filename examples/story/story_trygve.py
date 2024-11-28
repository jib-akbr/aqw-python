from core.bot import Bot
from templates import attack
from templates.hunt import hunt_item_cmds, hunt_monster_quest_temp_item
from templates.story import do_story_quest, QuestItemReq, QuestMapItemReq, QuestSingleReq
from templates.general import accept_quest_bulk
import commands as cmd

b = Bot(
    roomNumber=None, 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)

b.set_login_info("u", "p", "alteon")

first_map_item_id = 9036
first_quest_id = 8289

def next_map_item():
    global first_map_item_id
    first_map_item_id += 1
    return first_map_item_id

def next_quest_id():
    global first_quest_id
    first_quest_id += 1
    return first_quest_id
    
b.add_cmds([
    cmd.JoinMapCmd("trygve", 9099),
    cmd.SleepCmd(1000),
    cmd.JumpCmd("Enter", "Spawn"),
    
    *accept_quest_bulk(first_quest_id, increament=10),
    
    *do_story_quest(
        first_quest_id,
        [
            QuestSingleReq(monster="Vindicator Recruit"),
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Blood Eagle Feather",
                qty=9,
                monster="Blood Eagle",
            ),
            QuestMapItemReq(
                map_item_id=first_map_item_id,
                qty=1
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Armor Chunk",
                qty=9,
                monster="Vindicator Recruit",
            ),
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=1
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Patch of Boar Hide",
                qty=8,
                monster="Rune Boar",
            ),
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=1
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Soldiers Pacified",
                qty=9,
                monster="Vindicator Recruit",
            ),
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=3
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=8
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Boar Bone",
                qty=9,
                monster="Rune Boar",
            ),
            QuestItemReq(
                item_name="Eagle Talon",
                qty=9,
                monster="Blood Eagle",
            ),
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Recruit")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Creature Bones",
                qty=7,
                monster="Blood Eagle",
            ),
            QuestItemReq(
                item_name="Vindicator Defeated",
                qty=7,
                monster="Vindicator Recruit",
            ),
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Gramiel")
        ]
    ),
    cmd.StopBotCmd("DONE STORY - Trgve")
])

b.start_bot()