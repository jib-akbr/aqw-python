class SlaveConfig:
    def __init__(self, username, password, char_class, bot_path):
        self.username = username
        self.password = password
        self.char_class = char_class
        self.bot_path = bot_path

slaves = [
    SlaveConfig("u", # MASTER
                "p", 
                "Chaos Avenger",
                "bot.templeshrine.midnightsun.core.main"
                ),
    SlaveConfig("u", 
                "p", 
                "StoneCrusher", 
                "bot.templeshrine.midnightsun.core.slave"
                ),
    SlaveConfig("u",
                "p", 
                "ArchPaladin", 
                "bot.templeshrine.midnightsun.core.slave"
                ),
    SlaveConfig("u", 
                "p", 
                "Lord of Order", 
                "bot.templeshrine.midnightsun.core.slave"
                ),
]

server = "safiria"