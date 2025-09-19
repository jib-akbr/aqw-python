from core.bot import Bot
import commands as cmd
import asyncio

users = [
	{
		'user': 'username',
		'pass': 'password'
	},
	{
		'user': 'username',
		'pass': 'password'
	}
]

for user in users:
		b = Bot(roomNumber="9099", showLog = True, showDebug=False, cmdDelay = 500)
		b.set_login_info(user['user'], user['pass'], "alteon")
		b.add_cmds([
				cmd.IsInInvCmd("Gear of Doom", 3, operator="<"),
				cmd.StopBotCmd(msg="Not enough Gear of Doom."),
				cmd.AcceptQuestCmd(3076),
				cmd.TurnInQuestCmd(3076),
				cmd.SleepCmd(1000),
				cmd.StopBotCmd(msg="Bot Finished.")
		])
		asyncio.run(b.start_bot())