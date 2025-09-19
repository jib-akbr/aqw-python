from core.player import Player
from model.inventory import ItemInventory, ItemType
from model import PlayerArea
from typing import Optional

from core.commands.base import _CommandBase

class PlayerCommands(_CommandBase):
    """Player state inspection helpers."""
    
    def get_player(self) -> Player:
        """Return the bot's active player instance."""
        return self.bot.player

    def is_player_alive(self) -> bool:
        """Return True when the local player is not dead."""
        return not self.bot.player.ISDEAD

    def is_still_connected(self) -> bool:
        """Check whether the client connection is still active."""
        return self.bot.is_client_connected

    def get_farm_class(self) -> Optional[str]:
        """Return the configured farming class name, or None when unset."""
        return None if self.bot.farmClass == "" else self.bot.farmClass

    def get_solo_class(self) -> Optional[str]:
        """Return the configured solo class name, or None when unset."""
        return None if self.bot.soloClass == "" else self.bot.soloClass

    def get_equipped_class(self) -> Optional[ItemInventory]:
        """Return the currently equipped class inventory item, or None."""
        equipped_class = self.bot.player.get_equipped_item(ItemType.CLASS)
        return equipped_class if equipped_class else None

    def wait_count_player(self, player_count: int) -> bool:
        """Check if the current map has at least the requested player count."""
        return len(self.bot.user_ids) >= player_count

    def wait_count_player_in_cell(self, cell: str, player_count: int) -> bool:
        """Check if a cell hosts at least the requested number of players."""
        count = 0
        cell = cell.lower()
        for player in self.bot.player_in_area:
            print(player.str_username, player.str_frame, cell)
            if player.str_frame.lower() == cell:
                count += 1
        
        if self.bot.player.CELL.lower() == cell:
            count += 1
        return count >= player_count

    def get_player_in_map(self, name: str) -> Optional[PlayerArea]:
        """Return the area record for a player in the current map, if present."""
        for player in self.bot.player_in_area:
            if player.str_username.lower() == name.lower():
                return player
        return None

    def is_player_in_cell(self, name: str, cell: str) -> bool:
        """Return True when a named player is currently in the given cell."""
        player = self.get_player_in_map(name)
        if player and player.str_frame and player.str_frame.lower() == cell.lower():
            return True
        return False

    def get_player_cell(self) -> str:
        """Return the local player's current cell name."""
        return self.bot.player.getPlayerCell()[0]

    def get_player_pad(self) -> str:
        """Return the local player's current pad identifier."""
        return self.bot.player.getPlayerCell()[1]

    def get_player_position_xy(self) -> list[int]:
        """Return the local player's map coordinates as an [x, y] list."""
        return self.bot.player.getPlayerPositionXY()
