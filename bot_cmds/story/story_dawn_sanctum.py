from core.bot import Bot
from templates import attack
from templates.hunt import hunt_item_cmds, hunt_monster_quest_temp_item
from templates.story import do_story_quest, QuestItemReq, QuestMapItemReq, QuestSingleReq
from templates.general import accept_quest_bulk
import commands as cmd
import asyncio

b = Bot(
    roomNumber=None, 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)

b.set_login_info("u", "p", "alteon")

first_map_item_id = 13853
first_quest_id = 9977

def next_map_item():
    global first_map_item_id
    first_map_item_id += 1
    return first_map_item_id

def next_quest_id():
    global first_quest_id
    first_quest_id += 1
    return first_quest_id
    
b.add_cmds([
    cmd.JoinMapCmd("dawnsanctum", 9099),
    cmd.SleepCmd(1000),
    cmd.JumpCmd("Enter", "Spawn"),
    
    *accept_quest_bulk(first_quest_id, increament=10),
    
    *do_story_quest(
        first_quest_id,
        [
            QuestSingleReq("Vindicator Soldier"),
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Hollowborn Soldier")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Recruit's Brand",
                qty=5,
                monster="Vindicator Recruit",
            ),
            QuestMapItemReq(
                map_item_id= first_map_item_id,
                qty=1
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Hound")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Hollowborn Collar",
                qty=6,
                monster="Hollowborn Hound",
            ),
            QuestMapItemReq(
                map_item_id= next_map_item(),
                qty=1
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Draconian")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Hollowborn Draconian")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Vindicator Talon",
                qty=6,
                monster="Vindicator Draconian",
            ),
            QuestItemReq(
                item_name="Hollowborn Talon",
                qty=6,
                monster="Hollowborn Draconian",
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Grandmaster Gramiel")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Celestial Gramiel")
        ]
    ),
    cmd.StopBotCmd("DONE STORY - Dawn Sanctum")
])

asyncio.run(b.start_bot())