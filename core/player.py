import requests
from typing import List
from datetime import datetime, timedelta
from .utils import checkOperator
from colorama import Fore
import json
from core.utils import normalize
from model.inventory import ItemInventory, ItemType
from model.aura import Aura
from model.faction import Faction
from model.monster import Monster

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
        self.FACTIONS: list[Faction] = []
        self.CHARID = 0
        self.GOLD = 0
        self.GOLDFARMED = 0
        self.EXPFARMED = 0
        self.ISDEAD = False
        self.MAX_HP = 9999
        self.CURRENT_HP = 9999
        self.MANA = 100
        self.IS_IN_COMBAT: bool = False
        self.X: int = 0
        self.Y: int= 0
        self.AURAS: list[Aura] = []
        self.skills_ref: dict = {}
        self.last_target: Monster = None
        self.is_member: bool = False

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
            self.is_member = response_json["login"]["iUpg"] == 1
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
        if skillNumber > len(self.SKILLS):
            return False
        skills = self.SKILLS[skillNumber]
        if datetime.now() > skills["nextUse"]:
            return True
        return False

    def updateNextUse(self, skillNumber: int, delayms: int = 0) -> None:
        skills = self.SKILLS[skillNumber]
        if delayms == 0:
            cooldown = float(skills["cd"]) * (1 - self.CDREDUCTION)
            self.SKILLS[skillNumber]["nextUse"] = datetime.now() + timedelta(milliseconds=cooldown)
        else:
            self.SKILLS[skillNumber]["nextUse"] = datetime.now() + timedelta(milliseconds=delayms)

    def getCooldown(self, skillNumber: int) -> float:
        skills = self.SKILLS[skillNumber]
        return float(skills["cd"]) * (1 - self.CDREDUCTION)

    def updateTime(self, skillNumber: int, force_update: bool = False):
        skill_detail = self.SKILLS[skillNumber]
        cooldown = float(skill_detail["cd"]) * (1 - self.CDREDUCTION) + 200
        self._update_skill_time(skillNumber, cooldown, force_update)

    def delayAllSkills(self, except_skill: int, delay_ms: float = 1500):
        """this is to delay skill to prevent server warning 'Please slow down'"""
        if except_skill == 0:
            return
        for skill_number in range(len(self.SKILLS)):
            if except_skill != skill_number and skill_number != 0:
                self.updateNextUse(skill_number, delay_ms)
            # elif skill_number == except_skill:
            #     self._update_skill_time(skill_number, float(500))
    
    def _update_skill_time(self, skill_number: int, time_offset_ms: float, force_update: bool = False):
        new_cooldown_time = datetime.now() + timedelta(milliseconds=time_offset_ms)
        if not self.SKILLUSED.get(skill_number) or self.SKILLUSED[skill_number] < new_cooldown_time or force_update:
            self.SKILLUSED[skill_number] = new_cooldown_time
            # print(f"set delay for skill: {skill_number}")

    def get_equipped_item(self, item_type: ItemType):
        for item in self.INVENTORY:
            if item.s_es == item_type.value and item.is_equipped:
                return item
        return None

    def get_item_inventory(self, itemName: str) -> ItemInventory:
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

    def get_item_inventory_by_enhance_id(self, enh_id: int) -> ItemInventory:
        for item in self.INVENTORY:
            if item.enh_id == enh_id:
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
        
    def get_item_bank_by_id(self, itemId):
        for item in self.BANK:
            if item.item_id == str(itemId):
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
            if normalize(item.item_name) == normalize(itemName):
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
        for aura in auras:
            is_new = aura.get('isNew', False)
            name = normalize(aura.get('nam'))
            if is_new:
                self.AURAS.append(Aura(aura))
            else:
                for existing_aura in self.AURAS:
                    if existing_aura.name == name:
                        existing_aura.refresh(aura.get('dur', 0))
    
    def removeAura(self, auraName: str):
        normalized_name = normalize(auraName)
        for aura in self.AURAS[:]:
            if aura.name == normalized_name:
                self.AURAS.remove(aura)
                break
    
    def removeAllAuras(self):
        self.AURAS: list[Aura] = []

    def getAura(self, auraName: str) -> Aura:
        normalized_name = normalize(auraName)
        for aura in self.AURAS:
            if aura.name == normalized_name and not aura.is_expired():
                return aura
        return None
    
    def hasAura(self, auraName: str) -> bool:
        normalized_name = normalize(auraName)
        for aura in self.AURAS:
            if aura.name == normalized_name and not aura.is_expired():
                return True
        return False
    
    def setLastTarget(self, monster: Monster):
        if monster == None:
            self.last_target = None
            return
        self.last_target = monster
    
    def getLastTarget(self) -> Monster:
        return self.last_target
    
    def setIsInCombat(self, player_state: int):
        self.IS_IN_COMBAT = True if player_state == 2 else False
    
    def addFaction(self, faction: Faction) -> None:
        already_exists = False
        for fac in self.FACTIONS:
            if fac.faction_name.lower() == faction.faction_name.lower():
                already_exists = True
                return
        if already_exists == False:
            self.FACTIONS.append(faction)
    
    def addRepToFaction(self, faction_id: int, faction_rep: int) -> None:
        for fac in self.FACTIONS:
            if fac.faction_id == faction_id:
                fac.add_rep(faction_rep)
                return
    
    def getFactionRank(self, faction_name: str) -> int:
        normalized_faction = normalize(faction_name)
        for fac in self.FACTIONS:
            if fac.faction_name == normalized_faction:
                return fac.get_rank()
        return 0
    
    def printAllAura(self):
        for aur in self.AURAS:
            print(aur.name)