from core.bot import Bot
from templates import afk, attack
import commands as cmd

b = Bot(roomNumber="9099", itemsDropWhiteList=[
  "Rime Token"
  ],showLog=True, showDebug=False, cmdDelay=500)
b.set_login_info("username", "password", "twilly")
atk = attack.generalAttack
b.add_cmds([
  cmd.JoinMapCmd("battlegrounde"),
  cmd.JumpCmd("r2", "Center"),
  cmd.RegisterQuestCmd(3991),
  cmd.RegisterQuestCmd(3992),
  cmd.MessageCmd("Farming...")
] + atk + [
    cmd.IsInInvCmd("Battleground D Opponent Defeated", 10, operator="<", isTemp=True),
    cmd.UpIndexCmd(len(atk)),
    cmd.TurnInQuestCmd(3991),
    cmd.IsInInvCmd("Battleground E Opponent Defeated", 10, operator="<", isTemp=True),
    cmd.UpIndexCmd(len(atk) + 4),
    cmd.TurnInQuestCmd(3992),
    cmd.UpIndexCmd(6),
    cmd.StopBotCmd()
])
b.start_bot()