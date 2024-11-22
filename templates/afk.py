import commands as cmd

idhq = [
        cmd.SleepCmd(2000),
        cmd.JoinHouseCmd("idhq"),
        cmd.SleepCmd(1000),
        cmd.JumpCmd("r1a", "Left"),
        cmd.WalkCmd(x=844,y=631),
        cmd.SleepCmd(60000),
        cmd.UpIndexCmd(1),
        # cmd.StopBotCmd()
    ]