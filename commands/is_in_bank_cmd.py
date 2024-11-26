from core.bot import Bot
from abstracts.command import Command

class IsInBankCmd(Command):
    skip_delay = True
    
    def __init__(self, itemName: str, itemQty: int = 1, operator: str = ">="):
        self.itemName = itemName
        self.itemQty = itemQty
        self.operator = operator
    
    def execute(self, bot: Bot):
        inBank = bot.player.isInBank(self.itemName, self.itemQty, self.operator)
        if(inBank == False):
            bot.index += 1
        
    def to_string(self):
        return f"Is in bank : {self.itemName} {self.operator} {self.itemQty} "