from core.bot import Bot
from abstracts.command import Command
import time

class SellItemCmd(Command):
    
    def __init__(self, item_name: str, qty: int = 1):
        self.item_name = item_name
        self.qty = qty = qty
    
    def execute(self, bot: Bot):
        for item in bot.player.INVENTORY:
            if item.item_name.lower() == self.item_name.lower():
                packet = f"%xt%zm%sellItem%{bot.areaId}%{item.item_id}%{self.qty}%{item.char_item_id}%"
                bot.write_message(packet)
                time.sleep(0.5)
                break
        
    def to_string(self):
        return f"Sell : {self.item_name}"