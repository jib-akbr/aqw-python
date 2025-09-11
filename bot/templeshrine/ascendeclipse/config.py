class SlaveConfig:
    def __init__(self, username, password, char_class, bot_path):
        self.username = username
        self.password = password
        self.char_class = char_class
        self.bot_path = bot_path

slaves = [
    SlaveConfig("u", # PARTY LEADER, will taunting Suffocated Light
                "p", 
                "Legion Revenant", 
                "bot.templeshrine.ascendeclipse.core.lead_solstice_p1"
                ),
    SlaveConfig("u", 
                "p", 
                "StoneCrusher", 
                "bot.templeshrine.ascendeclipse.core.solstice_p2"
                ),
    SlaveConfig("u", 
                "p", 
                "Lord of Order", 
                "bot.templeshrine.ascendeclipse.core.midnight_p1"
                ),
    SlaveConfig("u",
                "p", 
                "ArchPaladin", 
                "bot.templeshrine.ascendeclipse.core.midnight_p2"
                ),
]

server = "alteon"