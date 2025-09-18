from core.bot import Bot
import commands as cmd

def get_map_items(map_item_id: int, qty: int = 1):
    cmds = []
    for i in range(qty):
        cmds.append(cmd.GetMapItemCmd(map_item_id)),
    return cmds

def accept_quest_bulk(quest_id: int, increament: int):
    cmds = []
    for i in range(increament):
        cmds.append(cmd.AcceptQuestCmd(quest_id + i))
    return cmds

from typing import List

def un_bank_items(items: List[str]):
    cmds = []
    for item in items:
        cmds.append(cmd.IsInBankCmd(item)),
        cmds.append(cmd.BankToInvCmd(item))
    return cmds