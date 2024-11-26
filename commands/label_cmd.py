from core.bot import Bot
from abstracts.command import Command

class LabelCmd(Command):
    skip_delay = True
    
    def __init__(self, label: str):
        self.label = label.upper()
    
    def execute(self, bot: Bot):
        pass
        
    def to_string(self):
        return f"[{self.label}]"