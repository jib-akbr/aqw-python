import json
from typing import TYPE_CHECKING

from core.commands.quest_commands import QuestCommands
from core.commands.item_commands import ItemCommands
from core.commands.map_commands import MapCommands
from core.commands.combat_commands import CombatCommands
from core.commands.player_commands import PlayerCommands
from core.commands.utility_commands import UtilityCommands

if TYPE_CHECKING:
    from core.bot import Bot


class Command(QuestCommands, ItemCommands, MapCommands, CombatCommands, PlayerCommands, UtilityCommands):
    """Facade that exposes quest, item, map, combat, player, and utility helpers."""

    def __init__(self, bot: "Bot", init_handler: bool = False) -> None:
        self.bot = bot

        self.quest_to_check: int = None
        self.is_green_quest_var: bool = None
        self.is_completed_before_var: bool = None
        self.skill_reload_time: int = 0

        if init_handler:
            self.bot.subscribe(self._message_handler)

    def _message_handler(self, message: str) -> None:
        """Handle server messages to update quest status flags."""
        if not message:
            return
        if self.is_valid_json(message):
            data = json.loads(message)
        else:
            return
        try:
            data = data["b"]["o"]
        except Exception:
            return
        cmd = data.get("cmd")
        if cmd != "ccqr":
            return
        quest_id = data.get('QuestID')
        ccqr_msg = data.get('msg', '')
        if data.get('bSuccess', 0) == 1:
            return
        if quest_id is None or int(quest_id) != self.quest_to_check:
            return
        if "Missing Turn In Item" in ccqr_msg:
            self.is_green_quest_var = True
        if "Missing Quest Progress" in ccqr_msg:
            self.is_green_quest_var = False
        if "One Time Quest Only" in ccqr_msg:
            self.is_green_quest_var = False
            self.is_completed_before_var = True
