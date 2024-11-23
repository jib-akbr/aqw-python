from core.bot import Bot
from templates import afk, attack
import commands as cmd

b = Bot(roomNumber="9099",showLog=True, showDebug=False)
b.set_login_info("u", "p", "alteon")
atk = attack.generalAttack
b.add_cmds([
  cmd.JoinMapCmd("arcangrove"),
  cmd.JumpCmd("Back", "Right"),
  cmd.RegisterQuestCmd(800),
  cmd.RegisterQuestCmd(798),
  cmd.RegisterQuestCmd(797),
  cmd.RegisterQuestCmd(794),
  cmd.MessageCmd("Farming..."),
  cmd.LabelCmd("atk"),
] + atk + [
    cmd.ToLabelCmd("atk")
])
b.start_bot()