from core.bot import Bot
from abstracts.command import Command
import asyncio

class EquipScrollCmd(Command):
    
    #item_type: scroll, elixir, potion
    def __init__(self, item_name: str, item_type: str = "scroll"):
        self.item_name = item_name
        self.item_type = item_type
    
    async def execute(self, bot: Bot):
        await bot.ensure_leave_from_combat()
            
        for item in bot.player.INVENTORY:
            if item.item_name.lower() == self.item_name.lower():
                packet = f"%xt%zm%geia%%{bot.areaId}%{self.item_type}%{item.s_meta}%{item.item_id}%"
                bot.write_message(packet)
                asyncio.sleep(0.5)
                break
        
    def to_string(self):
        return f"Equip scroll : {self.item_name}"