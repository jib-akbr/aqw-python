from core.bot import Bot
from abstracts.command import Command
import time

class BankToInvCmd(Command):
    
    def __init__(self, itemName: str):
        self.itemName = itemName
            
    def execute(self, bot: Bot):
        item = bot.player.get_item_bank(self.itemName)        
        if item:
            packet = f"%xt%zm%bankToInv%{bot.areaId}%{item['ItemID']}%{int(item['CharItemID'])}%"
            bot.write_message(packet)
            is_exist = False
            for itemInv in bot.player.INVENTORY:
                if itemInv['sName'] == item['sName']:
                    del itemInv
                    bot.player.INVENTORY.append(item)
                    is_exist = True
                    break
            if not is_exist:
                bot.player.INVENTORY.append(item)
            for itemBank in bot.player.BANK:
                if itemBank['sName'] == item['sName']:
                    del itemBank
                    break
            time.sleep(1)
        
    def to_string(self):
        return f"Bank to inv : {self.itemName}"