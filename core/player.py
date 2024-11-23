import requests
from datetime import datetime, timedelta
from .utils import checkOperator

class Player:
    USER = ""
    PASS = ""
    TOKEN = ""
    SERVERS = []
    SKILLS = []
    SKILLUSED = {}
    CELL = ""
    PAD = ""
    CDREDUCTION = 0
    LOGINUSERID = 0
    INVENTORY = []
    TEMPINVENTORY = []
    BANK = []
    FACTIONS = []
    CHARID = 0
    GOLD = 0
    GOLDFARMED = 0
    EXPFARMED = 0
    ISDEAD = False

    listTypeEquip = ["Pet", "Cape", "Class", "Misc", "Armor", "Helm"]
    EQUIPPED = {}

    def __init__(self, user, pwd):
        self.USER = user
        self.PASS = pwd

    def getInfo(self) -> dict:
        url = "https://game.aq.com/game/api/login/now?"

        data = {
            "user": self.USER,
            "option": 1,
            "pass": self.PASS
        }

        print(f'Login {self.USER}...')
        response = requests.post(url, json=data)
        response_json = response.json()
        self.SERVERS = response_json["servers"]
        self.TOKEN = response_json["login"]["sToken"]
        self.LOGINUSERID = response_json["login"]["userid"]
        return response_json

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
        self.BANK = response.json()
    
    def getServerInfo(self, serverName) -> list[str, int]:
        for server in self.SERVERS:
            if server["sName"].lower() == serverName.lower():
                return [server["sIP"], server["iPort"]]
        return ["", 0]
    
    def canUseSkill(self, skillNumber) -> bool:
        skill = self.SKILLUSED.get(skillNumber)
        skillDetail = self.SKILLS[skillNumber]
        if skill:
            if datetime.now() > skill:
                return True
            else:
                return False
        return True

    def updateTime(self, skillNumber):
        skillDetail = self.SKILLS[skillNumber]
        self.SKILLUSED[skillNumber] = datetime.now() + timedelta(milliseconds=float(skillDetail["cd"]) * (1 - self.CDREDUCTION))

    def get_item_inventory(self, itemName: str):
        for item in self.INVENTORY:
            if item['sName'].lower() == itemName.lower():
                return item
        return None
    
    def get_item_temp_inventory(self, itemName: str):
        for item in self.TEMPINVENTORY:
            if item['sName'].lower() == itemName.lower():
                return item
        return None
    
    def get_item_inventory(self, itemId):
        for item in self.INVENTORY:
            if str(item['ItemID']) == str(itemId):
                return item
        return None
    
    def get_item_temp_inventory(self, itemId):
        for item in self.TEMPINVENTORY:
            if str(item['ItemID']) == str(itemId):
                return item
        return None
    
    def get_item_bank(self, itemName: str):
        for item in self.BANK:
            if item['sName'].lower() == itemName.lower():
                return item
        return None

    def isInBank(self, itemName: str, qty: int = 1, operator: str = ">=") -> bool:
        for item in self.BANK:
            if item["sName"].lower() == itemName.lower():
                if checkOperator(item["iQty"], qty, operator):
                    self.BANK_CHAR_ITEM_ID = int(item["CharItemID"])
                    self.BANK_ITEM_ID = int(item["ItemID"])
                    self.BANK_ITEM_NAME = itemName
                    return True
        return False
    
    def isInInventory(self, itemName: str, qty: int = 1, operator: str = ">=", isTemp: bool = False) -> bool:
        inv = self.INVENTORY
        invItemQty = 0
        if isTemp:
            inv = self.TEMPINVENTORY
        for item in inv:
            if item["sName"].lower() == itemName.lower():
                invItemQty = item["iQty"]
                break
        print(f"actual: {itemName} [{invItemQty}]")
        return checkOperator(invItemQty, qty, operator)