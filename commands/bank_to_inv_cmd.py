from typing import List, Union
from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand

class BankToInvCmd(BaseCommand):
    
    def __init__(self, itemNames: Union[str, List[str]]):
        self.itemNames = itemNames

    async def execute(self, bot: Bot, cmd: Command):
        await cmd.bank_to_inv(self.itemNames)
        
    def to_string(self):
        if len(self.itemNames) == 1:
            return f"Bank to inv: {self.itemNames[0]}"
        else:
            return f"Bank to inv: {', '.join(self.itemNames)}"