from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand

class GetMapItemCmd(BaseCommand):
    
    def __init__(self, map_item_id: int):
        self.map_item_id = map_item_id

    async def execute(self, bot: Bot, cmd: Command):
        bot.write_message(f"%xt%zm%getMapItem%{bot.areaId}%{self.map_item_id}%")
        
    def to_string(self):
        return f"Get map item: {self.map_item_id}"