from core.bot import Bot
import commands as cmd

# Initialize bot
b = Bot(
    roomNumber=9099, 
    itemsDropWhiteList=["Undead Energy", "Undead Essence", "Bone Dust"], 
    cmdDelay=1000,
    showLog=True, 
    showDebug=False,
    showChat=True)
b.set_login_info("u", "p", "alteon")

# Initialize variables
skill = cmd.UseSkillCmd(0)

# Arrange commands
b.add_cmds([
        cmd.JoinMapCmd("escherion"),
        cmd.JumpCmd("Boss", "Left"),
        cmd.LabelCmd("ATK"),
        skill.createSkill(0, "Staff of Inversion,Escherion"),
        skill.createSkill(1),
        skill.createSkill(2),
        skill.createSkill(0),
        skill.createSkill(3),
        skill.createSkill(4),
        cmd.ToLabelCmd("ATK"),
        cmd.StopBotCmd()
    ])

# Start bot
b.start_bot()