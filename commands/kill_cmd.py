from core.bot import Bot
from abstracts.command import Command
from commands import UseSkillCmd

class KillCmd(Command):
    
    def __init__(self, monsterName: []):
        self.monsterName = monsterName
    
    def execute(self, bot: Bot):
        isMonsterAlive = True
        while isMonsterAlive:
            UseSkillCmd(0)
            UseSkillCmd(1)
            UseSkillCmd(2)
            UseSkillCmd(0)
            UseSkillCmd(3)
            UseSkillCmd(4)
        
    def to_string(self):
        return f"Kill : {self.monsterName}"