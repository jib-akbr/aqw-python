from core.bot import Bot
from abstracts.command import Command
from colorama import Fore 

class TurnInQuestCmd(Command):
    
    def __init__(self, quest_id: int):
        self.quest_id = quest_id
    
    def execute(self, bot: Bot):
        bot.turn_in_quest(self.quest_id)
        
    def to_string(self):
        return f"Turn in quest : {self.quest_id}"