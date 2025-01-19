from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand
import asyncio

class BuyItemCmd(BaseCommand):
    
    def __init__(self, item_name: str, shop_id: int, qty: int = 1):
        self.item_name = item_name
        self.shop_id = shop_id
        self.qty = qty
    
    async def execute(self, bot: Bot, cmd: Command):  
        await bot.ensure_leave_from_combat()
                  
        shop = None
        for loaded_shop in bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(self.shop_id):
                shop = loaded_shop
                break
        if shop:
            for shop_item in shop.items:
                if shop_item.item_name == self.item_name.lower():
                    packet = f"%xt%zm%buyItem%{bot.areaId}%{shop_item.item_id}%{shop.shop_id}%{shop_item.shop_item_id}%{self.qty}%"
                    bot.write_message(packet)
                    await asyncio.sleep(0.5)
                    break
        else:
            packet = f"%xt%zm%loadShop%{bot.areaId}%{self.shop_id}%"
            bot.write_message(packet)
            await asyncio.sleep(1)
            bot.index -= 1
        
    def to_string(self):
        return f"Buy : {self.item_name}"