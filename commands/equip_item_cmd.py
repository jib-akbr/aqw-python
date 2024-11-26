from core.bot import Bot
from abstracts.command import Command

class EquipItemCmd(Command):
    
    def __init__(self, itemName: str):
        self.itemName = itemName
    
    def execute(self, bot: Bot):
        item = bot.player.get_item_inventory(itemName= self.itemName)      
        if item:
            packet = f"%xt%zm%equipItem%{bot.areaId}%{item['ItemID']}%"
            bot.write_message(packet)
            bot.player.EQUIPPED[item["sType"]] = item
            bot.doSleep(1000)
        
    def to_string(self):
        return f"Equip item : {self.itemName}"