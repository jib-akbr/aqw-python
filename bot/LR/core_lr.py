from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item

async def revenant_spellscroll(cmd: Command, qty: int = 20):
    item_name = "Revenant's Spellscroll"

    list_items = [
        "Aeacus Empowered",
        "Tethered Soul",
        "Darkened Essence",
        "Dracolich Contract",
        "Revenant's Spellscroll"
    ]

    await cmd.bank_to_inv(list_items)
    cmd.add_drop(list_items)

    cmd.farming_logger(item_name, qty)

    item_to_farm = [
        {"item_name": "Aeacus Empowered", "qty": 50, "map_name": "judgement", "cell": "r10a", "pad": "Left", "is_solo": True},
        {"item_name": "Tethered Soul", "qty": 300, "map_name": "revenant","cell": "r2", "pad": "Left", "is_solo" : False},
        {"item_name": "Darkened Essence", "qty": 500,"map_name": "shadowrealmpast", "cell": "Enter", "pad": "Spawn", "is_solo": False},
        {"item_name": "Dracolich Contract", "qty": 1000,"map_name": "necrodungeon", "cell": "r22", "pad": "Down", "is_solo": False},
    ]


    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break

        await cmd.ensure_accept_quest(6897)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(6897)

    await cmd.inv_to_bank(list_items)

async def conquest_wreath(cmd: Command, qty: int = 6):
    item_name = "Conquest Wreath"

    list_items = [
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

    await cmd.bank_to_inv(list_items)
    cmd.add_drop(list_items)

    cmd.farming_logger(item_name, qty)

    item_to_farm = [
        {"item_name": "Ancient Cohort Conquered", "qty": 400, "map_name": "mummies", "cell": "Enter", "pad": "Spawn", "is_solo": False},
        {"item_name": "Grim Cohort Conquered", "qty": 400, "map_name": "doomvault", "cell": "r1", "pad": "Right", "is_solo": False},
        {"item_name": "Pirate Cohort Conquered", "qty": 400, "map_name": "wrath", "cell": "r5", "pad": "Left", "is_solo": False},
        {"item_name": "Battleon Cohort Conquered", "qty": 400, "map_name": "doomwar", "cell": "r6", "pad": "Left", "is_solo": False},
        {"item_name": "Mirror Cohort Conquered", "qty": 400, "map_name": "overworld", "cell": "Enter", "pad": "Spawn", "is_solo": False},
        {"item_name": "Darkblood Cohort Conquered", "qty": 400, "map_name": "deathpits", "cell": "r1", "pad": "Left", "is_solo": False},
        {"item_name": "Vampire Cohort Conquered", "qty": 400, "map_name": "maxius", "cell": "r2", "pad": "Left", "is_solo": False},
        {"item_name": "Spirit Cohort Conquered", "qty": 400, "map_name": "curseshore", "cell": "Enter", "pad": "Spawn", "is_solo": False},
        {"item_name": "Dragon Cohort Conquered", "qty": 400, "map_name": "dragonbone", "cell": "Enter", "pad": "Spawn", "is_solo": False},
        {"item_name": "Doomwood Cohort Conquered", "qty": 400, "map_name": "doomwood", "cell": "r6", "pad": "Right", "is_solo": False},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break

        await cmd.ensure_accept_quest(6898)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(6898)
    
    await cmd.inv_to_bank(list_items)

async def conquest_wreath(cmd: Command, qty: int = 10):
    # not finished yet
    item_name = "Exalted Crown"

    list_items = [
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

    await cmd.bank_to_inv(list_items)
    cmd.add_drop(list_items)

    cmd.farming_logger(item_name, qty)

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break

        await cmd.ensure_accept_quest(6899)

        await cmd.ensure_turn_in_quest(6899)

async def get_hooded_legion_cowl(cmd: Command):
    item = "Hooded Legion Cowl"
    await cmd.bank_to_inv(item)

    if cmd.is_in_inventory(item):
        return
    
    await cmd.join_map("underworld")
    await cmd.ensure_load_shop(216)
    await cmd.buy_item(1951, item, 1)

async def get_dages_favor(cmd: Command, qty: int = 300):
    await hunt_item(
            cmd = cmd,
            item_name = "Dage's Favor",
            item_qty = qty,
            cell = "r8",
            pad = "Left",
            map_name = "underworld",
            farming_logger=True,
            is_temp=False
        )


async def farm_mats(cmd: Command, item_to_farm: list[dict]):
    for item in item_to_farm:
        if not cmd.isStillConnected():
            return
        is_solo = item.get("is_solo", False)
        if is_solo:
            solo_class = cmd.getSoloClass()
            if solo_class:
                await cmd.equip_item(solo_class)
        else:
            farm_class = cmd.getFarmClass()
            if farm_class:
                await cmd.equip_item(farm_class)
        if item["map_name"] == "revenant":
            await cmd.join_map("revenant", 999999)
        await hunt_item(
            cmd = cmd,
            item_name = item["item_name"],
            item_qty = item["qty"],
            cell = item["cell"],
            pad = item["pad"],
            map_name = item["map_name"],
            farming_logger=True,
            is_temp=False
        )