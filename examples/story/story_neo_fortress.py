from core.bot import Bot
from templates import attack
from templates.general import accept_quest_bulk
from templates.hunt import hunt_item_cmds, hunt_monster_quest_temp_item
from templates.story import do_story_quest, QuestItemReq, QuestMapItemReq, QuestSingleReq
import commands as cmd

b = Bot(
    roomNumber=None, 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)

b.set_login_info("u", "p", "alteon")

first_map_item_id = 11806
first_quest_id = 9281

def next_map_item():
    global first_map_item_id
    first_map_item_id += 1
    return first_map_item_id

def next_quest_id():
    global first_quest_id
    first_quest_id += 1
    return first_quest_id
    
b.add_cmds([
    cmd.JoinMapCmd("neofortress", 9099),
    cmd.SleepCmd(1000),
    cmd.JumpCmd("Enter", "Spawn"),
    
    *accept_quest_bulk(first_quest_id, increament=10),
    
    # 9281 | Watch the Light
    *do_story_quest(
        first_quest_id,
        [
            QuestMapItemReq(
                map_item_id=first_map_item_id, 
                qty=9
            )
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
            QuestSingleReq(monster="Vindicator Hound")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Beast")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Soldier")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=5
            )
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator General")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator Beast")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestSingleReq(monster="Vindicator General")
        ]
    ),
    *do_story_quest(
        next_quest_id(),
        [
            QuestMapItemReq(
                map_item_id=next_map_item(),
                qty=1,
            )
        ]
    ),
    cmd.StopBotCmd("DONE STORY - Neo Fortress")
])

b.start_bot()