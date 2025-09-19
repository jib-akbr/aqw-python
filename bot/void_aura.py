from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item

async def main(cmd: Command):
    private_room_number = 12345
    max = 5
    item_qty = 20*max

    await cmd.join_map("whitemap")

    await cmd.bank_to_inv([
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
    ])
    
    # await cmd.equip_item("Legion Revenant")

    # Define the list of dictionaries
    hunt_tasks = [
        {
            "item_name": "Astral Ephemerite Essence",
            "item_qty": item_qty,
            "map_name": "timespace",
            "room_number": private_room_number,
            "cell": "Frame1",
            "pad": "Spawn",
            "monster_name": "*",
        },
        {
            "item_name": "Belrot the Fiend Essence",
            "item_qty": item_qty,
            "map_name": "citadel",
            "room_number": private_room_number,
            "cell": "m13",
            "pad": "Left",
            "monster_name": "*",
        },
        {
            "item_name": "Black Knight Essence",
            "item_qty": item_qty,
            "map_name": "greenguardwest",
            "room_number": private_room_number,
            "cell": "BKWest15",
            "pad": "Left",
            "monster_name": "*",
        },
        {
            "item_name": "Tiger Leech Essence",
            "item_qty": item_qty,
            "map_name": "mudluk",
            "room_number": private_room_number,
            "cell": "Boss",
            "pad": "Down",
            "monster_name": "*",
        },
        {
            "item_name": "Carnax Essence",
            "item_qty": item_qty,
            "map_name": "aqlesson",
            "room_number": private_room_number,
            "cell": "Frame9",
            "pad": "Right",
            "monster_name": "*",
        },
        {
            "item_name": "Chaos Vordred Essence",
            "item_qty": item_qty,
            "map_name": "necrocavern",
            "room_number": private_room_number,
            "cell": "r16",
            "pad": "Down",
            "monster_name": "",
        },
        {
            "item_name": "Dai Tengu Essence",
            "item_qty": item_qty,
            "map_name": "hachiko",
            "room_number": private_room_number,
            "cell": "Roof",
            "pad": "Left",
            "monster_name": "*",
        },
        {
            "item_name": "Unending Avatar Essence",
            "item_qty": item_qty,
            "map_name": "timevoid",
            "room_number": private_room_number,
            "cell": "Frame8",
            "pad": "Left",
            "monster_name": "*",
        },
        {
            "item_name": "Void Dragon Essence",
            "item_qty": item_qty,
            "map_name": "dragonchallenge",
            "room_number": private_room_number,
            "cell": "r4",
            "pad": "Left",
            "monster_name": "*",
        },
        {
            "item_name": "Creature Creation Essence",
            "item_qty": item_qty,
            "map_name": "maul",
            "room_number": private_room_number,
            "cell": "r3",
            "pad": "Down",
            "monster_name": "*",
        },
    ]

    while cmd.is_in_inventory("Void Aura", 7500, "<") and cmd.is_still_connected():
        await cmd.ensure_accept_quest(4432)

        if cmd.can_turnin_quest(4432):
            await cmd.ensure_turn_in_quest(4432)
            await cmd.ensure_accept_quest(4432)
    
        cmd.farming_logger("Void Aura", 7500)
        
        for task in hunt_tasks:
            if not cmd.is_still_connected():
                return
            await hunt_item(
                cmd,
                item_name=task["item_name"],
                item_qty=task["item_qty"],
                map_name=task["map_name"],
                room_number=task["room_number"],
                cell=task["cell"],
                pad=task["pad"],
                monster_name=task["monster_name"],
                farming_logger=True,
                skill_list=[3,0,2,0,3,0,2,0,3,0,4,1],
            )

        await cmd.ensure_turn_in_quest(4432,amount=max)

whitelist = [
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

if __name__ == "__main__":
    import asyncio
    bot = Bot(itemsDropWhiteList=whitelist,
              cmdDelay=600,
              showDebug=True,
              autoRelogin=True,
              isScriptable=True)  
    run = Command(bot) 
    login = input("Login (username,pass): ").split(",")
    
    bot.set_login_info(login[0], login[1],"Safiria")  # Set login info

    asyncio.run(bot.start_bot(main))  # Run the main coroutine

