from core.bot import Bot
from abstracts.command import Command
from colorama import Fore 

class AcceptQuestCmd(Command):
    
    def __init__(self, quest_id: int):
        self.quest_id = quest_id
    
    def execute(self, bot: Bot):
        bot.accept_quest(self.quest_id)
        
    def to_string(self):
        return f"Accept quest : {self.quest_id}"