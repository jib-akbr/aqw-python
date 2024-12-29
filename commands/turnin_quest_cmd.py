from core.bot import Bot
from abstracts.command import Command
from colorama import Fore 

class TurnInQuestCmd(Command):
    
    def __init__(self, quest_id: int, item_id: int = -1):
        self.quest_id = quest_id
        self.item_id = item_id
    
    async def execute(self, bot: Bot):
        bot.turn_in_quest(self.quest_id, self.item_id)
        
    def to_string(self):
        return f"Turn in quest : {self.quest_id}^{self.item_id}"