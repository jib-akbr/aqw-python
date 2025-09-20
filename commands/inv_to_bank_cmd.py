from typing import List, Union
from core.bot import Bot
from core.command import Command
from abstracts.base_command import BaseCommand

class InvToBankCmd(BaseCommand):
    skip_delay = True
    
    def __init__(self, itemNames: Union[str, List[str]]):
        self.itemNames = itemNames
    
    async def execute(self, bot: Bot, cmd: Command):
        cmd.inv_to_bank(self.itemNames)
        
    def to_string(self):
        if len(self.itemNames) == 1:
            return f"Inv to bank: {self.itemNames[0]}"
        else:
            return f"Inv to bank: {', '.join(self.itemNames)}"