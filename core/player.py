import requests
from typing import List
from datetime import datetime, timedelta
from .utils import checkOperator
from colorama import Fore
import json
from core.utils import normalize
from model.inventory import ItemInventory, ItemType

class Player:    
    # Player intState
    # 0 = dead
    # 1 = alive, not in combat
    # 2 = alive, in combat

    def __init__(self, user, pwd):
        self.USER = user
        self.PASS = pwd
        self.TOKEN = ""
        self.SERVERS = []
        self.SKILLS = []
        self.SKILLUSED = {}
        self.CELL = ""
        self.PAD = ""
        self.CDREDUCTION = 0
        self.LOGINUSERID = 0
        self.INVENTORY: List[ItemInventory] = []
        self.TEMPINVENTORY: List[ItemInventory] = []
        self.BANK: List[ItemInventory] = []
        self.FACTIONS = []
        self.CHARID = 0
        self.GOLD = 0
        self.GOLDFARMED = 0
        self.EXPFARMED = 0
        self.ISDEAD = False
        self.MAX_HP = 9999
        self.CURRENT_HP = 9999
        self.IS_IN_COMBAT = False
        self.X: int = 0
        self.Y: int= 0
        self.AURAS = []

    def getInfo(self):
        url = "https://game.aq.com/game/api/login/now?"

        data = {
            "user": self.USER,
            "option": 1,
            "pass": self.PASS
        }

        print(f'Login {self.USER}...')
        response = requests.post(url, json=data)
        response_json = response.json()
        # print(json.dumps(response_json))
        if response_json.get("login", None):
            self.SERVERS = response_json["servers"]
            self.TOKEN = response_json["login"]["sToken"]
            self.LOGINUSERID = response_json["login"]["userid"]
            return response
        if response_json.get("bSuccess", 0) == 0:
            print(f"Login {self.USER} failed... {Fore.RED + response_json['sMsg'] + Fore.RESET}")
            return None
        return None

    def loadBank(self):
        url = "https://game.aq.com/game/api/char/bank?v=0.35129284486174583"

        data = {
            "layout": {
                "cat": "all"
            }
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'ccid': self.CHARID,
            'token': self.TOKEN,
            'artixmode': 'launcher',
            'X-Requested-With': 'ShockwaveFlash/32.0.0.371'
        }

        response = requests.request("POST", url, headers=headers, data=data)
        for item in response.json():
            self.BANK.append(ItemInventory(item))
    
    def getServerInfo(self, serverName):
        for server in self.SERVERS:
            if server["sName"].lower() == serverName.lower():
                return [server["sIP"], server["iPort"]]
        return ["", 0]
    
    def canUseSkill(self, skillNumber):
        skill = self.SKILLUSED.get(skillNumber)
        skillDetail = self.SKILLS[skillNumber]
        if skill:
            if datetime.now() > skill:
                return True
            else:
                return False
        return True

    def updateTime(self, skillNumber: int):
        skill_detail = self.SKILLS[skillNumber]
        cooldown = float(skill_detail["cd"]) * (1 - self.CDREDUCTION)
        self._update_skill_time(skillNumber, cooldown, force_update= True)

    def delayAllSkills(self, except_skill: int, delay_ms: float = 1000):
        """this is to delay skill to prevent server warning 'Please slow down'"""
        for skill_number in range(len(self.SKILLS)):
            if except_skill != skill_number:
                self._update_skill_time(skill_number, float(delay_ms))
    
    def _update_skill_time(self, skill_number: int, time_offset_ms: float, force_update: bool = False):
        new_cooldown_time = datetime.now() + timedelta(milliseconds=time_offset_ms)
        if not self.SKILLUSED.get(skill_number) or self.SKILLUSED[skill_number] < new_cooldown_time or force_update:
            self.SKILLUSED[skill_number] = new_cooldown_time

    def get_equipped_item(self, item_type: ItemType):
        for item in self.INVENTORY:
            if item.s_es == item_type.value and item.is_equipped:
                return item
        return None

    def get_item_inventory(self, itemName: str):
        for item in self.INVENTORY:
            if item.item_name == normalize(itemName):
                return item
        return None
    
    def get_item_temp_inventory(self, itemName: str):
        for item in self.TEMPINVENTORY:
            if item.item_name == normalize(itemName):
                return item
        return None
    
    def get_item_inventory_by_id(self, itemId):
        for item in self.INVENTORY:
            if item.item_id == str(itemId):
                return item
        return None
    
    def get_item_temp_inventory_by_id(self, itemId):
        for item in self.TEMPINVENTORY:
            if item.item_id == str(itemId):
                return item
        return None
    
    def get_item_bank(self, itemName: str):
        for item in self.BANK:
            if item.item_name == normalize(itemName):
                return item
        return None

    def isInBank(self, itemName: str, qty: int = 1, operator: str = ">="):
        inv = self.BANK
        invItemQty = 0
        for item in inv:
            if item.item_name == normalize(itemName):
                invItemQty = item.qty
                break
        return [checkOperator(invItemQty, qty, operator), invItemQty]
    
    def isInInventory(self, itemName: str, qty: int = 1, operator: str = ">=", isTemp: bool = False):
        inv = self.INVENTORY
        invItemQty = 0
        if isTemp:
            inv = self.TEMPINVENTORY
        for item in inv:
            if item.item_name == normalize(itemName):
                invItemQty = item.qty
                break
        return [checkOperator(invItemQty, qty, operator), invItemQty]
    
    def getPlayerPositionXY(self) -> list[int]:
        return [self.X, self.Y]
    
    def setPlayerPositionXY(self, X: int, Y: int):
        self.X = X
        self.Y = Y

    def getPlayerCell(self) -> list[str]:
        return [self.CELL, self.PAD]

    def addAura(self, auras:list):
        timestamp = datetime.now()
        for aura in auras:
            duration = aura.get('dur', 0)
            expiration_time = timestamp + timedelta(seconds=duration)
            aura_details ={
                'name': aura.get('nam'),
                'type': aura.get('t'),
                'duration': duration,
                'source_spell': aura.get('spellOn', None),
                'icon': aura.get('icon'),
                'applied_time': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'expires_at': expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            is_new = aura.get('isNew', False)
            if is_new:
                self.AURAS.append(aura_details)
            else:
                for existing_aura in self.AURAS:
                    if existing_aura['name'] == aura_details['name']:
                        existing_aura['applied_time'] = aura_details['applied_time']
                        existing_aura['expires_at'] = aura_details['expires_at']
                        break
            # print(f"{is_new} Aura: {aura_details['name']}, Type: {aura_details['type']}, Duration: {aura_details['duration']} seconds, "
            #     f"Source Spell: {aura_details['source_spell']}, Icon: {aura_details['icon']}, "
            #     f"Applied: {aura_details['applied_time']}, Expires: {aura_details['expires_at']}")
            # print()
    
    def removeAura(self, auraName: str):
        for aura in self.AURAS[:]:
            if aura['name'] == auraName:
                self.AURAS.remove(aura)
                # print(f"aura removed: {auraName}")
                break