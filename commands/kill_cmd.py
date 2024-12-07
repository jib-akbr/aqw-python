from core.bot import Bot
from abstracts.command import Command
from commands import UseSkillCmd

class KillCmd(Command):
    
    def __init__(self, monsterName: []):
        self.monsterName = monsterName
    
    async def execute(self, bot: Bot):
        pass
        
    def to_string(self):
        return f"Kill : {self.monsterName}"