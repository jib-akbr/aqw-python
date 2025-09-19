from core.player import Player
from model.inventory import ItemType
from model import PlayerArea

from core.commands.base import _CommandBase

class PlayerCommands(_CommandBase):
    """Player state inspection helpers."""
    
    def get_player(self) -> Player:
        return self.bot.player

    def is_player_alive(self) -> bool:
        return not self.bot.player.ISDEAD

    def is_still_connected(self) -> bool:
        return self.bot.is_client_connected

    def get_farm_class(self) -> str:
        return None if self.bot.farmClass == "" else self.bot.farmClass

    def get_solo_class(self) -> str:
        return None if self.bot.soloClass == "" else self.bot.soloClass

    def get_equipped_class(self):
        equipped_class = self.bot.player.get_equipped_item(ItemType.CLASS)
        return equipped_class if equipped_class else None

    def wait_count_player(self, player_count: int):
        return len(self.bot.user_ids) >= player_count

    def wait_count_player_in_cell(self, cell: str, player_count: int):
        count = 0
        cell = cell.lower()
        for player in self.bot.player_in_area:
            print(player.str_username, player.str_frame, cell)
            if player.str_frame.lower() == cell:
                count += 1
        
        if self.bot.player.CELL.lower() == cell:
            count += 1
        return count >= player_count

    def get_player_in_map(self, name: str) -> PlayerArea:
        for player in self.bot.player_in_area:
            if player.str_username.lower() == name.lower():
                return player
        return None

    def is_player_in_cell(self, name: str, cell: str) -> bool:
        player = self.get_player_in_map(name)
        if player and player.str_frame and player.str_frame.lower() == cell.lower():
            return True
        return False

    def get_player_cell(self) -> str:
        return self.bot.player.getPlayerCell()[0]

    def get_player_pad(self) -> str:
        return self.bot.player.getPlayerCell()[1]

    def get_player_position_xy(self) -> list[int]:
        return self.bot.player.getPlayerPositionXY()
