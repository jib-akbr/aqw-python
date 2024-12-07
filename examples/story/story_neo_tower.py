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

first_map_item_id = 13581
first_quest_id = 9855

def next_map_item():
    global first_map_item_id
    first_map_item_id += 1
    return first_map_item_id

def next_quest_id():
    global first_quest_id
    first_quest_id += 1
    return first_quest_id
    
b.add_cmds([
    cmd.JoinMapCmd("neotower", 9099),
    cmd.SleepCmd(1000),
    cmd.JumpCmd("Enter", "Spawn"),
    
    *accept_quest_bulk(first_quest_id, increament=10),
    
    # 9855 | 24 Hour Graveyard Shift
    *do_story_quest(
        first_quest_id,
        [
            QuestSingleReq("Dawn Vindicator Soldier")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Vindicator Beast")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Vindicator Draconian")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Tower Key",
                qty=1,
                monster="Vindicator Draconian",
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
            QuestSingleReq("Vindicator Assassin")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Vindicator BeastTamer")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Vindicator Beast")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Dawn Vindicator Soldier")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestItemReq(
                item_name="Beast's Grace",
                qty=8,
                monster="Vindicator Beast",
            ),
            QuestItemReq(
                item_name="Soldier's Grace",
                qty=8,
                monster="Dawn Vindicator Soldier",
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq("Vindicator Priest")
        ]
    ),
    cmd.StopBotCmd("DONE STORY - Neo Tower")
])

asyncio.run(b.start_bot())