import asyncio
from datetime import datetime
from typing import List, Union

from colorama import Fore
from core.commands.base import _CommandBase, check_alive
from core.utils import normalize
from model.inventory import ItemInventory, ScrollType
from model.shop import Shop

class ItemCommands(_CommandBase):
    """Inventory, bank, and shop helpers."""

    async def buy_item_cmd(self, item_name: str, shop_id: int, qty: int = 1):
        await self.bot.ensure_leave_from_combat()
        shop = None
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(shop_id):
                shop = loaded_shop
                break
        if shop:
            for shop_item in shop.items:
                if shop_item.item_name == item_name.lower():
                    packet = f"%xt%zm%buyItem%{self.bot.areaId}%{shop_item.item_id}%{shop.shop_id}%{shop_item.shop_item_id}%{qty}%"
                    self.bot.write_message(packet)
                    await asyncio.sleep(0.5)
                    break
        else:
            packet = f"%xt%zm%loadShop%{self.bot.areaId}%{shop_id}%"
            self.bot.write_message(packet)
            await asyncio.sleep(1)
            self.bot.index -= 1

    def is_in_bank(self, itemName: str, itemQty: int = 1, operator: str = ">=") -> bool:
        inBank = self.bot.player.isInBank(itemName, itemQty, operator)
        return inBank[0]

    def is_in_inventory(self, itemName: str, itemQty: int = 1, operator: str = ">=", isTemp: bool = False) -> bool:
        inInv = self.bot.player.isInInventory(itemName, itemQty, operator, isTemp)
        return inInv[0]

    def is_in_inventory_or_bank(self, itemName: str, itemQty: int = 1, operator: str = ">=", isTemp: bool = False) -> bool:
        return self.is_in_bank(itemName, itemQty, operator) or self.is_in_inventory(itemName, itemQty, operator, isTemp)

    def get_quant_item(self, itemName: str) -> int:
        # get item quant from inventory
        item_inventory: ItemInventory = self.bot.player.get_item_inventory(itemName)
        if item_inventory:
            return item_inventory.qty
        return 0

    def farming_logger(self, item_name: str, item_qty: int = 1, is_temp: bool = False) -> None:
        # Determine inventory type and fetch the item
        inventory_type = "temp" if is_temp else "inv"
        get_inventory = (
            self.bot.player.get_item_temp_inventory
            if is_temp else self.bot.player.get_item_inventory
        )
        
        # Fetch the item
        item = get_inventory(item_name)
        inv_item_qty = item.qty if item else 0

        # Prepare log message
        current_time = datetime.now().strftime('%H:%M:%S')
        message = (
            f"{Fore.CYAN}[{current_time}] [{inventory_type}] {item_name} "
            f"{inv_item_qty}/{item_qty}{Fore.RESET}"
        )
        
        # Print log message
        print(message)

    @check_alive
    async def bank_to_inv(self, itemNames: Union[str, List[str]]) -> None:
        itemNames = itemNames if isinstance(itemNames, list) else [itemNames]
        for item in itemNames:
            if not self.is_still_connected():
                return
            item = self.bot.player.get_item_bank(item)        
            if item:
                packet = f"%xt%zm%bankToInv%{self.bot.areaId}%{item.item_id}%{item.char_item_id}%"
                self.bot.write_message(packet)
                is_exist = False
                for itemInv in self.bot.player.INVENTORY:
                    if itemInv.item_name == item.item_name:
                        self.bot.player.INVENTORY.remove(itemInv)
                        self.bot.player.INVENTORY.append(item)
                        is_exist = True
                        break
                if not is_exist:
                    self.bot.player.INVENTORY.append(item)
                for itemBank in self.bot.player.BANK:
                    if itemBank.item_name == item.item_name:
                        self.bot.player.BANK.remove(itemBank)
                        break
                await asyncio.sleep(1)

    @check_alive
    async def inv_to_bank(self, itemNames: Union[str, List[str]]) -> None:
        await self.leave_combat()
        itemNames = itemNames if isinstance(itemNames, list) else [itemNames]
        for item in itemNames:
            if not self.is_still_connected():
                return
            item = self.bot.player.get_item_inventory(item)        
            if item:
                packet = f"%xt%zm%bankFromInv%{self.bot.areaId}%{item.item_id}%{item.char_item_id}%"
                self.bot.write_message(packet)
                is_exist = False
                for itemBank in self.bot.player.BANK:
                    if itemBank.item_name == item.item_name:
                        self.bot.player.BANK.remove(itemBank)
                        self.bot.player.BANK.append(item)
                        is_exist = True
                        break
                if not is_exist:
                    self.bot.player.BANK.append(item)
                for itemInv in self.bot.player.INVENTORY:
                    if itemInv.item_name == item.item_name:
                        self.bot.player.INVENTORY.remove(itemInv)
                        break
                await asyncio.sleep(1)

    @check_alive
    async def equip_item(self, item_name: str) -> None:
        await self.bot.ensure_leave_from_combat()
        
        is_equipped = False
        s_type = None
        for item in self.bot.player.INVENTORY:
            if normalize(item.item_name.lower()) == normalize(item_name.lower()):
                if item.is_equipped:
                    return
                print(f"equipping {item_name}")
                packet = f"%xt%zm%equipItem%{self.bot.areaId}%{item.item_id}%"
                self.bot.write_message(packet)
                is_equipped = True
                s_type = item.s_type
                item.is_equipped = is_equipped
                await asyncio.sleep(1)
                break
        # Update unequip previous item
        if is_equipped and s_type:
            for item in self.bot.player.INVENTORY:
                if item.s_type == s_type and item.is_equipped and not item.item_name == item_name.lower():
                    item.is_equipped = False
                    break

    @check_alive
    async def equip_scroll(self, item_name: str, item_type: ScrollType = ScrollType.SCROLL):
        for item in self.bot.player.INVENTORY:
            if item.item_name.lower() == item_name.lower():
                packet = f"%xt%zm%geia%{self.bot.areaId}%{item_type.value}%{item.s_meta}%{item.item_id}%"
                self.bot.scroll_id = item.item_id
                self.bot.write_message(packet)
                await asyncio.sleep(1)
                break

    @check_alive
    async def equip_item_by_enhancement(self, enh_id: int):
        # TODO: should change the enhance_pattern_id to enhance name
        item: ItemInventory = self.bot.player.get_item_inventory_by_enhance_id(enh_id)
        if item:
            await self.equip_item(item.item_name)

    def add_drop(self, itemName: Union[str, List[str]]) -> None:
        if isinstance(itemName, str):
            itemName = [itemName]

        for item in itemName:
            if item not in self.bot.items_drop_whitelist:
                self.bot.items_drop_whitelist.append(item)

    @check_alive
    async def get_map_item(self, map_item_id: int, qty: int = 1):
        for _ in range(qty):
            self.bot.write_message(f"%xt%zm%getMapItem%{self.bot.areaId}%{map_item_id}%")
            await asyncio.sleep(1)

    @check_alive
    async def load_shop(self, shop_id: int):
        msg = f"%xt%zm%loadShop%{self.bot.areaId}%{shop_id}%"
        self.bot.write_message(msg)
        await self.sleep(1000)

    @check_alive
    def get_loaded_shop(self, shop_id: int) -> Shop:
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(shop_id): 
                return loaded_shop
        return None

    @check_alive
    async def sell_item(self, item_name: str, qty: int = 1):
        # %xt%zm%sellItem%374121%87406%1%950679343%
        item: ItemInventory = self.bot.player.get_item_inventory(item_name)
        if item:
            self.bot.debug(f"Selling {qty}x {item_name}...")
            self.bot.write_message(f"%xt%zm%sellItem%{self.bot.areaId}%{item.item_id}%{qty}%{item.char_item_id}%")
            await self.sleep(500)

    @check_alive
    async def buy_item(self, shop_id: int, item_name: str, qty: int = 1):
        print(f"buying {qty} {item_name}")
        shop: Shop = None
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(shop_id):
                shop = loaded_shop
                break
        if shop:
            for shop_item in shop.items:
                if shop_item.item_name.lower() == item_name.lower():
                    packet = f"%xt%zm%buyItem%{self.bot.areaId}%{shop_item.item_id}%{shop.shop_id}%{shop_item.shop_item_id}%{qty}%"
                    self.bot.write_message(packet)
                    await asyncio.sleep(1)
                    break
        else:
            packet = f"%xt%zm%loadShop%{self.bot.areaId}%{shop_id}%"
            self.bot.write_message(packet)
            await asyncio.sleep(1)
            await self.buy_item(shop_id, item_name, qty)

    @check_alive
    async def ensure_load_shop(self, shop_id: int):
        await self.leave_combat()
        while True:
            for loaded_shop in self.bot.loaded_shop_datas:
                if str(loaded_shop.shop_id) == str(shop_id): 
                    print("loaded_Shop", loaded_shop.shop_id)
                    return
            packet = f"%xt%zm%loadShop%{self.bot.areaId}%{shop_id}%"
            self.bot.write_message(packet)
            await asyncio.sleep(1)
