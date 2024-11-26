from core.bot import Bot
from abstracts.command import Command
import time

class EquipScrollCmd(Command):
    
    #item_type: scroll, elixir, potion
    def __init__(self, item_name: str, item_type: str = "scroll"):
        self.item_name = item_name
        self.item_type = item_type
    
    def execute(self, bot: Bot):
        bot.ensure_leave_from_combat()
            
        for item in bot.player.INVENTORY:
            if item["sName"].lower() == self.item_name.lower():
                packet = f"%xt%zm%geia%%{bot.areaId}%{self.item_type}%{item['sMeta']}%{item['ItemID']}%"
                bot.write_message(packet)
                time.sleep(0.5)
                break
        
    def to_string(self):
        return f"Equip scroll : {self.item_name}"