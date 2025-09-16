class SlaveConfig:
    def __init__(self, username, password, char_class, bot_path):
        self.username = username
        self.password = password
        self.char_class = char_class
        self.bot_path = bot_path

slaves = [
    SlaveConfig("u", # MASTER
                "p", 
                "Verus DoomKnight",
                "bot.templeshrine.solsticemoon.core.main"
                ),
    SlaveConfig("u", 
                "p", 
                "Legion Revenant", 
                "bot.templeshrine.solsticemoon.core.slave"
                ),
    SlaveConfig("u",
                "p", 
                "ArchPaladin", 
                "bot.templeshrine.solsticemoon.core.slave"
                ),
    SlaveConfig("u", 
                "p", 
                "Lord of Order", 
                "bot.templeshrine.solsticemoon.core.slave"
                ),
]

server = "safiria"