from core.bot import Bot
from abstracts.command import Command

class RegisterQuestCmd(Command):
    
    def __init__(self, questId: int):
        self.questId = questId
    
    def execute(self, bot: Bot):
        if self.questId not in bot.registered_auto_quest:
            bot.registered_auto_quest.append(self.questId)
            bot.accept_quest(self.questId)
        
    def to_string(self):
        return f"Register quest : {self.questId}"