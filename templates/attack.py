import commands as cmd

skillCmd = cmd.UseSkillCmd()
atkExample = [
    cmd.JoinMapCmd("arcangrove"),
    cmd.JumpCmd("Left", "Right"),
    skillCmd.createSkill(0, "Gorillaphant"), # commands below using this 'monsterName'
    skillCmd.createSkill(3),
    skillCmd.createSkill(1),
    skillCmd.createSkill(0),
    skillCmd.createSkill(2),
    skillCmd.createSkill(4),
    skillCmd.createSkill(0, "Seed Spitter"), # commands below using this 'monsterName'
    skillCmd.createSkill(3),
    skillCmd.createSkill(1),
    skillCmd.createSkill(0),
    skillCmd.createSkill(2),
    skillCmd.createSkill(4),
    cmd.ToIndexCmd(2)
]

generalAttack = [
    skillCmd.createSkill(0),
    skillCmd.createSkill(1),
    skillCmd.createSkill(2),
    skillCmd.createSkill(0),
    skillCmd.createSkill(3),
    skillCmd.createSkill(4),
]

csh = [
    cmd.UseSkillCmd(3,"*"),
    cmd.UseSkillCmd(0,"*"),
    cmd.auraCmd("Rounds Empty"),
    cmd.UpIndexCmd(3),
    cmd.UseSkillCmd(4,"*",wait=True),
    cmd.UseSkillCmd(1,"*",wait=True),
]

def attack_monster(monster_name: str = "*"):
    return [
        skillCmd.createSkill(0, monster_name),
        skillCmd.createSkill(1),
        skillCmd.createSkill(2),
        skillCmd.createSkill(0),
        skillCmd.createSkill(3),
        skillCmd.createSkill(4),
    ]