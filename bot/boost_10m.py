from core.bot import Bot
from core.command import Command
from templates.hunt import hunt_item

async def main(cmd: Command):
    private_room_number = 999999

    item_list = ["GOLD Boost! (10 min)", "CLASS Boost! (10 min)", "REPUTATION Boost! (10 min)"]

    cmd.add_drop(item_list)
    cmd.add_drop("Nimblestem")
    cmd.add_drop("Trollola Nectar")
    cmd.add_drop("Moglinberries")
    await cmd.bank_to_inv(item_list)
    await cmd.equip_item("ArchPaladin")

    while cmd.is_still_connected():

        await cmd.ensure_accept_quest(6208)

        await hunt_item(
            cmd,
            item_name="Nimblestem",
            item_qty=1,
            map_name="cloister",
            monster_name= "Acornent",
            most_monster=True,
            farming_logger=True,
            room_number=private_room_number
        )
        await hunt_item(
            cmd,
            item_name="Trollola Nectar",
            item_qty=2,
            map_name="bloodtusk",
            cell="r4",
            pad="Center",
            monster_name="Trollola Plant",
            farming_logger=True,
            room_number=private_room_number
        )
        await hunt_item(
            cmd,
            item_name="Moglinberries",
            item_qty=3,
            map_name="nibbleon",
            monster_name="Dark Makai",
            most_monster=True,
            farming_logger=True,
            room_number=private_room_number
        )
        
        await cmd.ensure_turn_in_quest(6208)

        for item in item_list:
            cmd.farming_logger(item, 9999)