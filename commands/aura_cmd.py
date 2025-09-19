from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand

class auraCmd(BaseCommand):
    
    def __init__(self, aura_name: str):
        self.aura_name = aura_name
        self.aura = False
    
    async def execute(self, bot: Bot, cmd: Command):
        if bot.player.hasAura(auraName=self.aura_name):
            bot.index += 1
            self.aura = True
            return
        self.aura = False
        
    def to_string(self):
        return f"{self.aura_name} : {self.aura}"