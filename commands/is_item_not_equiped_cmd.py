from core.bot import Bot
from abstracts.command import Command

class IsItemNotEquipedCmd(Command):
    
    def __init__(self, item_name: str):
        self.item_name = item_name
    
    def execute(self, bot: Bot):
        item = bot.player.get_item_inventory(self.item_name)
        if not item or int(item['bEquip']) == 1:
            bot.index += 1
        
    def to_string(self):
        return f"Is item equiped : {self.item_name}"