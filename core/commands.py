import asyncio
from typing import List, Union
import time
from functools import wraps
from inspect import iscoroutinefunction
from datetime import datetime, timedelta
from colorama import Fore
from model.inventory import ItemType, ItemInventory, ScrollType
from model.shop import Shop
import json

def check_alive(func):
    @wraps(func)
    def sync_wrapper(self, *args, **kwargs):
        if self.isPlayerAlive():
            return func(self, *args, **kwargs)
        start_time = time.time()
        timeout = 11  # Maximum time to wait (in seconds)

        while self.isStillConnected():
            if self.isPlayerAlive():
                break
            if time.time() - start_time > timeout:
                self.stopBot()
                return
            time.sleep(1)  # Avoid busy-waiting
        if not self.isStillConnected():
            print("STOPPPPPPPP")
            return
        return func(self, *args, **kwargs)

    @wraps(func)
    async def async_wrapper(self, *args, **kwargs):
        if self.isPlayerAlive():
            return await func(self, *args, **kwargs)
        start_time = time.time()
        timeout = 11  # Maximum time to wait (in seconds)

        while self.isStillConnected():
            if self.isPlayerAlive():
                break
            if time.time() - start_time > timeout:
                self.stopBot()
                return
            await asyncio.sleep(1)  # Non-blocking wait
        if not self.isStillConnected():
            print("STOPPPPPPPP")
            return
        return await func(self, *args, **kwargs)
    # Check if the function is async and use the appropriate wrapper
    return async_wrapper if iscoroutinefunction(func) else sync_wrapper

class Command:
    def __init__(self, bot, init_handler = False):
        from core.bot import Bot
        self.bot: Bot = bot

        self.quest_to_check: int = None
        self.is_green_quest_var: bool = None
        
        if init_handler:
            self.bot.subscribe(self.message_handler)

    def isPlayerAlive(self) -> bool:
        return not self.bot.player.ISDEAD

    def isStillConnected(self) -> bool:
        return self.bot.is_client_connected
    
    def shouldFollowPlayer(self) -> bool:
        return self.bot.follow_player and self.bot.followed_player_cell != self.bot.player.CELL

    def getFarmClass(self) -> str:
        return None if self.bot.farmClass == "" else self.bot.farmClass
    
    def getSoloClass(self) -> str:
        return None if self.bot.soloClass == "" else self.bot.soloClass

    def stopBot(self, msg: str = ""):
        print(Fore.RED + msg + Fore.RESET)
        print(Fore.RED + "stop bot: " + self.bot.player.USER + Fore.RESET)
        self.bot.stop_bot()
    
    @check_alive
    async def goto_player(self, player_name: str):
        await self.bot.ensure_leave_from_combat(always=True)
        self.bot.write_message(f"%xt%zm%cmd%1%goto%{player_name}%")
        await self.sleep(1000)
    
    @check_alive
    async def leave_combat(self, safeLeave: bool = True) -> bool:
        await self.bot.ensure_leave_from_combat(always=True)
        if safeLeave:
            await self.jump_cell("Enter", "Spawn")
    
    @check_alive
    async def ensure_accept_quest(self, quest_id: int) -> None:
        while self.quest_not_in_progress(quest_id) and self.isStillConnected():
            await self.accept_quest(quest_id)
            await self.sleep(1000)
            if quest_id in self.bot.failed_get_quest_datas:
                return
        print("quest accepted:", quest_id)
    
    @check_alive
    async def ensure_turn_in_quest(self, quest_id: int, item_id = -1) -> None:
        while self.quest_in_progress(quest_id) and self.isStillConnected():
            await self.turn_in_quest(quest_id, item_id)
            await self.sleep(1000)
            if quest_id in self.bot.failed_get_quest_datas:
                return
        print("quest turned in:", quest_id, item_id)
        
    @check_alive
    async def join_house(self, houseName: str, safeLeave: bool = True):
        self.stop_aggro()
        if self.bot.strMapName.lower() == houseName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)
        msg = f"%xt%zm%house%1%{houseName}%"
        self.bot.write_message(msg)

    @check_alive
    async def join_map(self, mapName: str, roomNumber: int = None, safeLeave: bool = True) -> None:
        self.stop_aggro()
        if self.bot.strMapName.lower() == mapName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)

        if roomNumber != None:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{roomNumber}%"
        elif self.bot.roomNumber != None:
            roomNumber = self.bot.roomNumber
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{self.bot.roomNumber}%"
        else:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}%"
        self.bot.write_message(msg)
    
    def is_not_in_map(self, mapName: str) -> bool:
        return mapName.lower() != self.bot.strMapName.lower()

    @check_alive
    async def jump_cell(self, cell: str, pad: str) -> None:
        if self.bot.player.CELL.lower() != cell.lower() or self.bot.player.PAD.lower() != pad.lower():
            self.bot.jump_cell(cell, pad)
            #print(f"jump cell: {cell} {pad}")
            await asyncio.sleep(1)
    
    def is_not_in_cell(self, cell: str) -> bool:
        return self.bot.player.CELL.lower() != cell.lower()
    
    @check_alive
    async def jump_to_monster(self, monsterName: str, byMostMonster: bool = True, byAliveMonster: bool = False) -> None:
        for monster in self.bot.monsters:
            if monster.mon_name.lower() == monsterName.lower() \
                    and monster.is_alive \
                    and self.bot.player.CELL == monster.frame:
                return

        # Hunt monster in other cell
        if byMostMonster or byAliveMonster:
            cell = self.bot.find_best_cell(monsterName, byMostMonster, byAliveMonster)
            if cell:
                if cell == self.bot.player.CELL:
                    return
                self.bot.jump_cell(cell, "Left")
                await asyncio.sleep(1)
                return
        for monster in self.bot.monsters:
            if monster.mon_name.lower() == monsterName.lower() \
                    and monster.is_alive \
                    and self.bot.player.CELL != monster.frame:
                # TODO need to handle the rigth pad
                self.bot.jump_cell(monster.frame, "Left")
                await asyncio.sleep(1)
                return
        
    @check_alive
    async def use_skill(self,  index: int = 0, target_monsters: str = "*", hunt: bool = False, scroll_id: int = 0) -> None:
        if not self.bot.player.canUseSkill(int(index)) or not self.bot.check_is_skill_safe(int(index)):
            return

        skill = self.bot.player.SKILLS[int(index)]
        self.bot.skillAnim = skill["anim"]
        self.bot.skillNumber = index
        max_target = int(skill.get("tgtMax", 1))

        if skill["tgt"] == "h": 
            priority_monsters_id = []
            if hunt and len(target_monsters.split(",")) == 1 and target_monsters != "*":
                await self.jump_to_monster(target_monsters, byAliveMonster=True)
            cell_monsters_id = [mon.mon_map_id for mon in self.bot.monsters if mon.frame == self.bot.player.CELL and mon.is_alive]
            cell_monsters = [mon for mon in self.bot.monsters if mon.frame == self.bot.player.CELL and mon.is_alive]
            final_ids = []
            if target_monsters != "*":
                # Mapping priority_monsters_id
                target_ids = []
                target_names = []
                for target_monster in target_monsters.split(','):
                    if target_monster.startswith('id.'):
                        target_ids.append(target_monster.split('.')[1])
                    else:
                        target_names.append(target_monster.lower())

                # Mapping priority_monsters_id
                for mon in self.bot.monsters:
                    if mon.frame != self.bot.player.CELL or not mon.is_alive:
                        continue

                    # Check by ID
                    if mon.mon_map_id in target_ids:
                        priority_monsters_id.append(mon.mon_map_id)
                        continue

                    # Check by name
                    if mon.mon_name.lower() in target_names:
                        priority_monsters_id.append(mon.mon_map_id)
                # Check if the first index is one of the priority targets
                if len(priority_monsters_id) > 0:
                    if not cell_monsters_id[0] in priority_monsters_id:
                        cell_monsters_id.pop(0)
                        cell_monsters_id.insert(0, priority_monsters_id[0])
                # Remove duplicate monster id and keep the order
                seen = set()
                for monster_id in cell_monsters_id:
                    if monster_id not in seen:
                        final_ids.append(monster_id)
                        seen.add(monster_id)
            else:
                cell_monsters.sort(key=lambda m: m.current_hp)
                final_ids = [mon.mon_map_id for mon in cell_monsters]
            if index == 5:
                self.bot.use_scroll(final_ids, max_target)
            if len(final_ids) > 0:
                self.bot.use_skill_to_monster("a" if self.bot.skillNumber == 0 else self.bot.skillNumber, final_ids, max_target)
        elif skill["tgt"] == "f":
            self.bot.use_skill_to_player(self.bot.skillNumber, max_target)
        # self.bot.canuseskill = False
        # self.bot.player.delayAllSkills(except_skill=index, delay_ms=1200)

        await self.sleep(200)
        self.bot.player.updateNextUse(index)
        self.bot.player.SKILLS[int(index)]["canUseSkill"] = False
        if index != 0:
            self.bot.player.delayAllSkills(except_skill=index, delay_ms=600)

    
    @check_alive
    def do_pwd(self, monster_id: str):
        # %xt%zm%gar%1%3%p6>m:1%wvz%
        self.bot.write_message(f"%xt%zm%gar%1%3%p6>m:{monster_id}%wvz%")

    @check_alive
    async def sleep(self,  milliseconds: int) -> None:
        await asyncio.sleep(milliseconds/1000)

    @check_alive
    async def accept_quest(self, quest_id: int) -> None:
        self.bot.accept_quest(quest_id)
        await asyncio.sleep(1)

    def quest_not_in_progress(self, quest_id: int) -> bool:
        loaded_quest_ids = [loaded_quest["QuestID"] for loaded_quest in self.bot.loaded_quest_datas]
        return str(quest_id) not in str(loaded_quest_ids)
    
    def quest_in_progress(self, quest_id: int) -> bool:
        loaded_quest_ids = [loaded_quest["QuestID"] for loaded_quest in self.bot.loaded_quest_datas]
        return str(quest_id) in str(loaded_quest_ids)

    def can_turnin_quest(self, questId: int) -> bool:
        return self.bot.can_turn_in_quest(questId)
    
    @check_alive
    async def turn_in_quest(self, quest_id: int, item_id: int = -1) -> None:
        self.quest_to_check = quest_id
        await self.bot.ensure_leave_from_combat()
        self.bot.turn_in_quest(quest_id, item_id)
        await asyncio.sleep(1)
        
    async def buy_item_cmd(self, item_name: str, shop_id: int, qty: int = 1):
        await self.bot.ensure_leave_from_combat()
        shop = None
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(self.shop_id):
                shop = loaded_shop
                break
        if shop:
            for shop_item in shop.items:
                if shop_item.item_name == self.item_name.lower():
                    packet = f"%xt%zm%buyItem%{self.bot.areaId}%{shop_item.item_id}%{shop.shop_id}%{shop_item.shop_item_id}%{self.qty}%"
                    self.bot.write_message(packet)
                    await asyncio.sleep(0.5)
                    break
        else:
            packet = f"%xt%zm%loadShop%{self.bot.areaId}%{self.shop_id}%"
            self.bot.write_message(packet)
            await asyncio.sleep(1)
            self.bot.index -= 1
            
    async def sell_item(self, item_name: str, qty: int = 1):
        for item in self.bot.player.INVENTORY:
            if item.item_name.lower() == self.item_name.lower():
                packet = f"%xt%zm%sellItem%{self.bot.areaId}%{item.item_id}%{self.qty}%{item.char_item_id}%"
                self.bot.write_message(packet)
                asyncio.sleep(0.5)
                break

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
            if not self.isStillConnected():
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
            if not self.isStillConnected():
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
            if item.item_name == item_name.lower():
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
    async def equip_item_by_enhancement(self, enh_pattern_id: int):
        # TODO: should change the enhance_pattern_id to enhance name
        item = self.bot.player.get_item_inventory_by_enhance_id(enh_pattern_id)
        if item:
            await self.equip_item(item.item_name)

    def add_drop(self, itemName: Union[str, List[str]]) -> None:
        if isinstance(itemName, str):
            itemName = [itemName]

        for item in itemName:
            if item not in self.bot.items_drop_whitelist:
                self.bot.items_drop_whitelist.append(item)

    def is_monster_alive(self, monster: str = "*") -> bool:
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.is_alive and mon.frame == self.bot.player.CELL:
                if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                    return True
                elif monster == "*":
                    return True
        return False
    
    @check_alive
    def get_monster_hp(self, monster: str) -> int:
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                return mon.current_hp
            elif monster == "*":
                return mon.current_hp
        # this mean not get the desired monster
        return -1

    def get_monster_hp_percentage(self, monster: str) -> int:
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                return round(((mon.current_hp/mon.max_hp)*100), 2)
            elif monster == "*":
                return round(((mon.current_hp/mon.max_hp)*100), 2)
        # this mean not get the desired monster
        return -1

    @check_alive
    async def get_map_item(self, map_item_id: int, qty: int = 1):
        for _ in range(qty):
            self.bot.write_message(f"%xt%zm%getMapItem%{self.bot.areaId}%{map_item_id}%")
            await asyncio.sleep(1)

    @check_alive
    async def accept_quest_bulk(self, quest_id: int, increament: int, ensure:bool = False):
        for i in range(increament):
            if ensure:
                await self.ensure_accept_quest(quest_id + i)
            elif not ensure:
                await self.accept_quest(quest_id + i)


    @check_alive
    async def register_quest(self, questId: int):
        if questId not in self.bot.registered_auto_quest_ids:
            self.bot.registered_auto_quest_ids.append(questId)
            await self.ensure_accept_quest(questId)

    def wait_count_player(self, player_count: int):
        return len(self.bot.user_ids) >= player_count
    
    def get_player_cell(self) -> list[str]:
        return self.bot.player.getPlayerCell()
    
    def get_player_position_xy(self) -> list[int]:
        return self.bot.player.getPlayerPositionXY()
    
    @check_alive
    async def walk_to(self, X: int, Y: int, speed: int = 8):
        await self.bot.walk_to(X, Y, speed)
        await self.sleep(200)

    def start_aggro_by_cell(self, cells: list[str], delay_ms : int = 500):
        mons_id: list[str] = []
        for monster in self.bot.monsters:
            if monster.frame in cells:
                mons_id.append(str(monster.mon_map_id))

        if len(mons_id) == 0:
            return
        
        self.start_aggro(mons_id, delay_ms)

    def start_aggro(self, mons_id: list[str], delay_ms: int = 500):
        self.stop_aggro()
        self.bot.is_aggro_handler_task_running = True
        self.bot.aggro_mons_id = mons_id
        self.bot.aggro_delay_ms = delay_ms
        self.bot.run_aggro_hadler_task()

    def stop_aggro(self):
        self.bot.is_aggro_handler_task_running = False
        self.bot.aggro_mons_id = []

    @check_alive
    async def load_shop(self, shop_id: int):
        msg = f"%xt%zm%loadShop%{self.bot.areaId}%{shop_id}%"
        self.bot.write_message(msg)
        await self.sleep(1000)

    def get_loaded_shop(self, shop_id: int):
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(shop_id):
                return loaded_shop
        return None
    
    @check_alive
    def hp_below_percentage(self, percent: int):
        return ((self.bot.player.CURRENT_HP / self.bot.player.MAX_HP) * 100) < percent
    
    def get_equipped_class(self):
        equipped_class = self.bot.player.get_equipped_item(ItemType.CLASS)
        return equipped_class if equipped_class else None
    
    @check_alive
    async def sell_item(self, item_name: str):
        # %xt%zm%sellItem%374121%87406%1%950679343%
        item: ItemInventory = self.bot.player.get_item_inventory(item_name)
        if item:
            self.bot.write_message(f"%xt%zm%sellItem%{self.bot.areaId}%{item.item_id}%1%{item.char_item_id}%")
            await self.sleep(1000)

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
    
    @check_alive
    def get_loaded_shop(self, shop_id: int) -> Shop:
        for loaded_shop in self.bot.loaded_shop_datas:
            if str(loaded_shop.shop_id) == str(shop_id): 
                return loaded_shop
        return None
    
    @check_alive
    async def is_green_quest(self, quest_id: int) -> bool:
        await self.turn_in_quest(quest_id)
        while(self.isStillConnected()):
            if self.is_green_quest_var is not None:
                output = self.is_green_quest_var
                # print(f"{quest_id} is {self.is_green_quest_var}")
                self.is_green_quest_var = None
                return output
            else:
                await self.sleep(100)
        return False

    def message_handler(self, message):
        if message:
            if self.is_valid_json(message):
                data = json.loads(message)
            try:
                data = data["b"]["o"]
            except:
                return
            cmd = data["cmd"]
            # print("XX", data)
            # print("userid", self.bot.user_id)
            # print()
            if cmd == "ccqr":
                quest_id = data.get('QuestID', None)
                s_name = data.get('sName', None)
                faction_id = data.get('rewardObj', {}).get('FactionID', None)
                i_rep = data.get('rewardObj', {}).get('iRep', 0)
                is_success = data.get('bSuccess', 0)
                ccqr_msg = data.get('msg', '')
                if is_success == 1:
                    pass
                else:
                    if int(quest_id) == self.quest_to_check:
                        if "Missing Turn In Item" in ccqr_msg:
                            self.is_green_quest_var = True
                        if "Missing Quest Progress" in ccqr_msg:
                            self.is_green_quest_var = False
                        if "One Time Quest Only" in ccqr_msg:
                            self.is_green_quest_var = False

    def is_valid_json(self, s):
        try:
            json.loads(s)
            return True
        except json.JSONDecodeError:
            return False