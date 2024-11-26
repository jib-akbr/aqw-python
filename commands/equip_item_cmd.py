from core.bot import Bot
from abstracts.command import Command
import time

class EquipItemCmd(Command):
    
    def __init__(self, item_name: str):
        self.item_name = item_name
    
    def execute(self, bot: Bot):
        bot.ensure_leave_from_combat()
        
        is_equipped = False
        s_type = None
        for item in bot.player.INVENTORY:
            if item['sName'].lower() == self.item_name.lower():
                packet = f"%xt%zm%equipItem%{bot.areaId}%{item['ItemID']}%"
                bot.write_message(packet)
                is_equipped = True
                s_type = item['sType']
                item['bEquip'] = 1
                time.sleep(0.5)
                break
        # Update unequip previous item
        if is_equipped and s_type:
            for item in bot.player.INVENTORY:
                if item['sType'] == s_type and item['bEquip'] == 1 and not item['sName'].lower() == self.item_name.lower():
                    item['bEquip'] = 0
                    break
        
    def to_string(self):
        return f"Equip item : {self.item_name}"