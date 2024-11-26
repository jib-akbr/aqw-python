from core.bot import Bot
from abstracts.command import Command

class InvToBankCmd(Command):
    
    def __init__(self, itemName: str):
        self.itemName = itemName
    
    def execute(self, bot: Bot):
        item = bot.player.get_item_inventory(self.itemName)        
        if item:
            packet = f"%xt%zm%bankFromInv%{bot.areaId}%{item['ItemID']}%{int(item['CharItemID'])}%"
            bot.write_message(packet)
            is_exist = False
            for itemBank in bot.player.BANK:
                if itemBank['sName'] == item['sName']:
                    del itemBank
                    bot.player.BANK.append(item)
                    is_exist = True
                    break
            if not is_exist:
                bot.player.BANK.append(item)
            for itemInv in bot.player.INVENTORY:
                if itemInv['sName'] == item['sName']:
                    del itemInv
                    break
        
    def to_string(self):
        return f"Inv to bank : {self.itemName}"