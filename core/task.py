from core.bot import Bot
from core.commands import Command
from templates.hunt import hunt_item
from dataclasses import dataclass

@dataclass(frozen=True)
class FarmTask:
    item_name: str
    qty: int
    map_name: str
    cell: str
    pad: str
    is_solo: bool = False
    
async def do_farm_tasks(cmd: Command, tasks: list[FarmTask]):
    for task in tasks:
        if not cmd.isStillConnected():
            return

        if task.is_solo:
            class_to_equip = cmd.getSoloClass()
        else:
            class_to_equip = cmd.getFarmClass()

        if class_to_equip:
            await cmd.equip_item(class_to_equip)

        await hunt_item(
            cmd=cmd,
            item_name=task.item_name,
            item_qty=task.qty,
            cell=task.cell,
            pad=task.pad,
            map_name=task.map_name,
            farming_logger=True,
            is_temp=True
        )
