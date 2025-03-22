from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item

async def a_melody(cmd: Command, qty: int = 300):
    item_name = "A Melody"
    map_name = "astraviajudge"


    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Brass", "qty": 10, "map_name": map_name, "cell": "r3", "pad": "Left"},
        {"item_name": "Sinew", "qty": 10, "map_name": map_name,"cell": "r2", "pad": "Left"},
        {"item_name": "Knight's Favor", "qty": 1,"map_name": map_name, "cell": "r11", "pad": "Right", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8396)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8396)
    
    await cmd.inv_to_bank(item_name)

async def ancient_remnant(cmd: Command, qty: int = 300):
    item_name = "Ancient Remnant"
    map_name = "firstobservatory"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Creature Samples", "qty": 6, "map_name": map_name, "cell": "r7", "pad": "Right"},
        {"item_name": "Turret Pieces", "qty": 12, "map_name": map_name,"cell": "r6", "pad": "Right"},
        {"item_name": "Alprecha Observed", "qty": 1,"map_name": map_name, "cell": "r10a", "pad": "Left", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8641)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8641)

    await cmd.inv_to_bank(item_name)

async def astravian_medal(cmd: Command, qty: int = 300):
    item_name = "Astravian Medal"
    map_name = "astraviacastle"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Defaced Portrait", "qty": 10, "map_name": map_name, "cell": "r3", "pad": "Right"},
        {"item_name": "Smashed Sculpture", "qty": 4, "map_name": map_name,"cell": "r6", "pad": "Right"},
        {"item_name": "Burned Banana", "qty": 1,"map_name": map_name, "cell": "r11", "pad": "Left", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8257)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8257)
    
    await cmd.inv_to_bank(item_name)

async def bounty_hunter_dubloon(cmd: Command, qty: int = 300):
    item_name = "Bounty Hunter Dubloon"
    map_name = "hbchallenge"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Module 005 Defeated", "qty": 1,"map_name": map_name, "cell": "r6", "pad": "Right", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(9393)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(9393)

    await cmd.inv_to_bank(item_name)

async def darkons_receipts_binky(cmd: Command, qty: int = 222):
    item_name = "Darkon's Receipts"
    map_name = "doomvault"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    if cmd.is_in_bank("Ingredients?"):
        await cmd.bank_to_inv("Ingredients?")
    
    cmd.add_drop(item_name)
    cmd.add_drop("Ingredients?")

    item_to_farm = [
        {"item_name": "Ingredients?", "qty": 22,"map_name": map_name, "cell": "r5", "pad": "Right", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(7325)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(7325)
    
    await cmd.inv_to_bank(item_name)

async def darkons_receipts_tower_of_doom(cmd: Command, qty: int = 222):
    item_name = "Darkon's Receipts"
    map_name = "towerofdoom7"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    if cmd.is_in_bank("Banana"):
        await cmd.bank_to_inv("Banana")
    
    cmd.add_drop(item_name)
    cmd.add_drop("Banana")

    item_to_farm = [
        {"item_name": "Banana", "qty": 22,"map_name": map_name, "cell": "r5", "pad": "Right", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(7324)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(7324)
    
    await cmd.inv_to_bank(item_name)

async def las_gratitude(cmd: Command, qty: int = 300):
    item_name = "La's Gratitude"
    map_name = "astravia"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    await cmd.register_quest(8001)

    await hunt_item(
        cmd,
        item_name=item_name,
        item_qty=qty,
        map_name=map_name,
        cell="r10",
        pad="Right",
        farming_logger=True
    )

    await cmd.inv_to_bank(item_name)

async def mourning_flower(cmd: Command, qty: int = 1000):
    item_name = "Mourning Flower"
    map_name = "genesisgarden"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)
    cmd.add_drop("Jus Divium Scale")

    item_to_farm = [
        {"item_name": "Beast Subject", "qty": 7, "map_name": map_name, "cell": "r6", "pad": "Right"},
        {"item_name": "Humanoid Subject", "qty": 7, "map_name": map_name,"cell": "r9", "pad": "Right"},
        {"item_name": "Replacement Parts", "qty": 7,"map_name": map_name, "cell": "r11", "pad": "Left"},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8688)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8688)
    
    await cmd.inv_to_bank(item_name)

async def sukis_prestige(cmd: Command, qty: int = 300):
    item_name = "Suki's Prestige"
    map_name = "astraviapast"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Regulus' Rematch Won", "qty": 1, "map_name": map_name, "cell": "r6", "pad": "Right", "is_solo": True},
        {"item_name": "Titania's Rematch Won", "qty": 1, "map_name": map_name,"cell": "r7", "pad": "Right", "is_solo": True},
        {"item_name": "Aurola's Rematch Won", "qty": 1, "map_name": map_name,"cell": "r8", "pad": "Right", "is_solo": True},
        {"item_name": "Soldiers Trained", "qty": 8,"map_name": map_name, "cell": "r4", "pad": "Left"},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8602)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8602)

    await cmd.inv_to_bank(item_name)

async def unfinished_musical_score(cmd: Command, qty: int = 300):
    item_name = "Unfinished Musical Score"
    map_name = "theworld"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    solo_class = cmd.getSoloClass()
    if solo_class:
        await cmd.equip_item(solo_class)
    
    await hunt_item(
        cmd,
        item_name=item_name,
        item_qty=qty,
        map_name=map_name,
        cell="r9",
        pad="Left",
        farming_logger=True
    )

    await cmd.inv_to_bank(item_name)

async def bandits_correspondence(cmd: Command, qty: int = 3000):
    item_name = "Bandit's Correspondence"
    map_name = "eridanipast"

    if cmd.is_in_bank(item_name):
        await cmd.bank_to_inv(item_name)
    
    cmd.farming_logger(item_name, qty)

    if cmd.is_in_inventory(item_name, qty, ">="):
        await cmd.inv_to_bank(item_name)
        return
    
    if cmd.is_not_in_map(map_name):
        await cmd.join_map(map_name)
    
    cmd.add_drop(item_name)

    item_to_farm = [
        {"item_name": "Bandit Contraband", "qty": 12, "map_name": map_name, "cell": "r2", "pad": "Left"},
        {"item_name": "Dogs Confiscated", "qty": 12, "map_name": map_name,"cell": "r3", "pad": "Left"},
        {"item_name": "Seraphic Sparred", "qty": 1,"map_name": map_name, "cell": "r10", "pad": "Left", "is_solo": True},
    ]

    while cmd.isStillConnected():
        if cmd.is_in_inventory(item_name, qty, ">="):
            break
        
        await cmd.ensure_accept_quest(8531)

        await farm_mats(cmd, item_to_farm)

        await cmd.ensure_turn_in_quest(8531)
    
    await cmd.inv_to_bank(item_name)


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
        await hunt_item(
            cmd = cmd,
            item_name = item["item_name"],
            item_qty = item["qty"],
            cell = item["cell"],
            pad = item["pad"],
            map_name = item["map_name"],
            farming_logger=True,
            is_temp=True
        )