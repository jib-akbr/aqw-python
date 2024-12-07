from core.bot import Bot
from abstracts.command import Command

class InvToBankCmd(Command):
    skip_delay = True
    
    def __init__(self, itemName: str):
        self.itemName = itemName
    
    async def execute(self, bot: Bot):
        item = bot.player.get_item_inventory(itemName=self.itemName)        
        if item:
            packet = f"%xt%zm%bankFromInv%{bot.areaId}%{item.item_id}%{item.char_item_id}%"
            bot.write_message(packet)
            is_exist = False
            for itemBank in bot.player.BANK:
                if itemBank.item_name == item.item_name:
                    bot.player.BANK.remove(itemBank)
                    bot.player.BANK.append(item)
                    is_exist = True
                    break
            if not is_exist:
                bot.player.BANK.append(item)
            for itemInv in bot.player.INVENTORY:
                if itemInv.item_name == item.item_name:
                    bot.player.INVENTORY.remove(itemInv)
                    break
        
    def to_string(self):
        return f"Inv to bank : {self.itemName}"