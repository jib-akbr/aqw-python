from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item

async def main(bot: Bot):
    cmd = Command(bot)
    private_room_number = 999999
    item_qty = 20

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
    
    await cmd.equip_item("Legion Revenant")

    while cmd.is_in_inventory("Void Aura", 7500, "<") and bot.is_client_connected:
        cmd.farming_logger("Void Aura", 7500)
        await cmd.ensure_accept_quest(4432)

        if cmd.can_turnin_quest(4432):
            await cmd.ensure_turn_in_quest(4432)
            await cmd.ensure_accept_quest(4432)
    
        await hunt_item(
                cmd,
                item_name = "Astral Ephemerite Essence",
                item_qty = item_qty,
                map_name = "timespace",
                room_number = private_room_number,
                cell = "Frame1",
                pad = "Spawn",
                monster_name = "*",
                farming_logger=True
            )
        
        await hunt_item(
                cmd,
                item_name = "Belrot the Fiend Essence",
                item_qty = item_qty,
                map_name = "citadel",
                room_number = private_room_number,
                cell = "m13",
                pad = "Left",
                monster_name = "*",
                farming_logger=True
            )
        
        await hunt_item(
                cmd,
                item_name = "Black Knight Essence",
                item_qty = item_qty,
                map_name = "greenguardwest",
                room_number = None,
                cell = "BKWest15",
                pad = "Left",
                monster_name = "*",
                farming_logger=True
            )

        await hunt_item(
                cmd,
                item_name = "Tiger Leech Essence",
                item_qty = item_qty,
                map_name = "mudluk",
                room_number = private_room_number,
                cell = "Boss",
                pad = "Down",
                monster_name = "*",
                farming_logger=True
            )
        
        await hunt_item(
                cmd,
                item_name = "Carnax Essence",
                item_qty = item_qty,
                map_name = "aqlesson",
                room_number = private_room_number,
                cell = "Frame9",
                pad = "Right",
                monster_name = "*",
                farming_logger=True
            )
        await hunt_item(
            cmd,
            item_name = "Chaos Vordred Essence",
            item_qty = item_qty,
            map_name = "necrocavern",
            room_number = private_room_number,
            cell = "r16",
            pad = "Down",
            monster_name = "",
            farming_logger=True
        )
        
        await hunt_item(
            cmd,
            item_name = "Dai Tengu Essence",
            item_qty = item_qty,
            map_name = "hachiko",
            room_number = private_room_number,
            cell = "Roof",
            pad = "Left",
            monster_name = "*",
            farming_logger=True
        )
        
        await hunt_item(
            cmd,
            item_name = "Unending Avatar Essence",
            item_qty = item_qty,
            map_name = "timevoid",
            room_number = private_room_number,
            cell = "Frame8",
            pad = "Left",
            monster_name = "*",
            farming_logger=True
        )
        
        await hunt_item(
            cmd,
            item_name = "Void Dragon Essence",
            item_qty = item_qty,
            map_name = "dragonchallenge",
            room_number = private_room_number,
            cell = "r4",
            pad = "Left",
            monster_name = "*",
            farming_logger=True
        )
        
        await hunt_item(
            cmd,
            item_name = "Creature Creation Essence",
            item_qty = item_qty,
            map_name = "maul",
            room_number = private_room_number,
            cell = "r3",
            pad = "Down",
            monster_name = "*",
            farming_logger=True
        )

        await cmd.ensure_turn_in_quest(4432)

