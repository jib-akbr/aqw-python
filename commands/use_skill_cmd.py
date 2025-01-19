from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand
from core.commands import Command
from model import Monster
import asyncio

class UseSkillCmd(BaseCommand):
    
    skip_delay = True
    
    def __init__(self, index: int = 0, target_monsters: str = "*", hunt: bool = False, scroll_id: int = 0):
        self.index = index
        self.target_monsters = target_monsters
        self.hunt = hunt
        self.scroll_id = scroll_id
    
    def createSkill(self, index: int, target_monsters: str = "*"):
        self.index = index
        if target_monsters != "*":
            self.target_monsters = target_monsters
        return UseSkillCmd(index, self.target_monsters)
    
    async def execute(self, bot: Bot, cmd: Command):
        await cmd.use_skill(self.index, self.target_monsters, self.hunt, self.scroll_id)
        
    def to_string(self):
        # return f"UseSkill : {self.index}"
        return None