from core.bot import Bot
from abstracts.command import Command
import time

class BuyItemCmd(Command):
    
    def __init__(self, item_name: str, shop_id: int, qty: int = 1):
        self.item_name = item_name
        self.shop_id = shop_id
        self.qty = qty
    
    def execute(self, bot: Bot):            
        shop = None
        for loaded_shop in bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(self.shop_id):
                shop = loaded_shop
                break
        if shop:
            for shop_item in shop.items:
                if shop_item.item_name == self.item_name:
                    packet = f"%xt%zm%buyItem%{bot.areaId}%{shop_item.item_id}%{shop.shop_id}%{shop_item.shop_item_id}%{self.qty}%"
                    bot.write_message(packet)
                    bot.doSleep(500)
                    break
        else:
            packet = f"%xt%zm%loadShop%{bot.areaId}%{self.shop_id}%"
            bot.write_message(packet)
            bot.doSleep(500)
            bot.index -= 1
        
    def to_string(self):
        return f"Buy : {self.item_name}"