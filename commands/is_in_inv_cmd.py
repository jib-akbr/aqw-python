from core.bot import Bot
from abstracts.command import Command

class IsInInvCmd(Command):
    skip_delay = True
    
    def __init__(self, itemName: str, itemQty: int = 1, operator: str = ">=", isTemp: bool = False):
        self.itemName = itemName
        self.itemQty = itemQty
        self.operator = operator
        self.isTemp = isTemp
        self.inInv = [False, 0]
    
    async def execute(self, bot: Bot):
        self.inInv = bot.player.isInInventory(self.itemName, self.itemQty, self.operator, self.isTemp)
        if(self.inInv[0] == False):
            bot.index += 1
        
    def to_string(self):
        return f"Is in inv : {'[Temp]' * self.isTemp} {self.itemName} {self.inInv[1]} {self.operator} {self.itemQty} "