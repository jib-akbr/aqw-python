from core.bot import Bot
from abstracts.command import Command

class UseSkillCmd(Command):
    
    def __init__(self, index: int = 0, monsterName: str = "*"):
        self.index = index
        self.monsterName = monsterName
    
    def createSkill(self, index: int, monsterName: str = None):
        self.index = index
        if monsterName != None:
            self.monsterName = monsterName
        return UseSkillCmd(index, self.monsterName)
    
    def execute(self, bot: Bot):
        if not bot.player.canUseSkill(int(self.index)) and not bot.canuseskill:
            bot.debug(f"Skill {self.index} not ready yet")
            return

        skill = bot.player.SKILLS[int(self.index)]
        
        bot.skillAnim = skill["anim"]
        bot.skillNumber = self.index

        max_target = int(skill.get("tgtMax", 1))

        if skill["tgt"] == "h": 
            monIds = []
            monIds = monIds + [mons["MonMapID"] for mons in bot.monsters if mons["strFrame"] == bot.player.CELL]
            if self.monsterName != "*":
                for mons in bot.monsters:
                    if mons["name"].lower() == self.monsterName.lower() and mons["strFrame"] == bot.player.CELL:
                        monIds.remove(mons["MonMapID"])
                        monIds.insert(0, mons["MonMapID"])
            bot.use_skill_to_monster("a" if bot.skillNumber == 0 else bot.skillNumber, monIds, max_target)
        elif skill["tgt"] == "f":
            bot.use_skill_to_player(bot.skillNumber, max_target)
        bot.canuseskill = False
        
    def to_string(self):
        # return f"UseSkill : {self.index}"
        return None