from core.bot import Bot
import commands as cmd

def hunt_item_cmds(
        item_name: str, 
        item_qty: int, 
        map_name: str, 
        cell: str, 
        pad: str, 
        room_number: int = None, 
        monster_name: str = "*"
    ):
    label_done = f"Hunt for {item_name} [{item_qty}x] is done"
    lebel_farming = f"Farming for {item_name} [{item_qty}x]"
    return [
        # Check is item in bank
        cmd.IsInBankCmd(item_name),
        cmd.BankToInvCmd(item_name),
        
        # Check is item qty already fullfiled
        cmd.IsInInvCmd(item_name, item_qty, operator=">="),
        cmd.ToLabelCmd(label_done),
        
        # Farming items
        cmd.JoinMapCmd(map_name, room_number),
        cmd.JumpCmd(cell, pad),
        cmd.LabelCmd(lebel_farming),
        cmd.IsInInvCmd(item_name, item_qty, operator=">="),
        cmd.ToLabelCmd(label_done),
        *attack(monster_name),
        cmd.ToLabelCmd(lebel_farming),
        
        cmd.LabelCmd(label_done),
        cmd.SleepCmd(1000)
    ]
    
def attack(monster_name = "*"):
    return [
        cmd.UseSkillCmd(0, monster_name),
        cmd.UseSkillCmd(1, monster_name),
        cmd.UseSkillCmd(2, monster_name),
        cmd.UseSkillCmd(0, monster_name),
        cmd.UseSkillCmd(3, monster_name),
        cmd.UseSkillCmd(4, monster_name),
    ]

def attack_len():
    return len(attack())