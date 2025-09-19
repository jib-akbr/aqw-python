import asyncio

from core.commands.base import _CommandBase, check_alive

class MapCommands(_CommandBase):
    """Map travel and positioning helpers."""

    @check_alive
    async def goto_player(self, player_name: str) -> None:
        """Jump to another player on the current server.

        Args:
            player_name (str): Target player name to follow.
        """
        await self.bot.ensure_leave_from_combat(always=True)
        self.bot.write_message(f"%xt%zm%cmd%1%goto%{player_name}%")
        await self.sleep(1000)

    @check_alive
    async def join_house(self, houseName: str, safeLeave: bool = True) -> None:
        """Join a player house while optionally leaving combat safely.

        Args:
            houseName (str): Name of the house to join.
            safeLeave (bool): Leave combat via spawn before issuing the join request.
        """
        self.stop_aggro()
        if self.bot.strMapName.lower() == houseName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)
        msg = f"%xt%zm%house%1%{houseName}%"
        self.bot.write_message(msg)

    @check_alive
    async def join_map(self, mapName: str, roomNumber: int = None, safeLeave: bool = True) -> None:
        """Join a map instance, picking the appropriate room.

        Args:
            mapName (str): Map identifier to join.
            roomNumber (int | None): Specific room number to target when provided.
            safeLeave (bool): Leave combat before transferring maps.

        Returns:
            None: Records join state and sends the transfer packet.
        """
        self.stop_aggro()
        if self.bot.strMapName.lower() == mapName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)

        if roomNumber != None:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{roomNumber}%"
        elif self.bot.roomNumber != None:
            roomNumber = self.bot.roomNumber
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{self.bot.roomNumber}%"
        else:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}%"
        self.bot.write_message(msg)

    def is_not_in_map(self, mapName: str) -> bool:
        """Return True when the player is not currently in the given map.

        Args:
            mapName (str): Map identifier to compare.

        Returns:
            bool: True when the current map differs from ``mapName``.
        """
        return mapName.lower() != self.bot.strMapName.lower()

    @check_alive
    async def jump_cell(self, cell: str, pad: str) -> None:
        """Jump to a specific cell and pad if not already positioned there.

        Args:
            cell (str): Cell name to move to.
            pad (str): Pad identifier within the cell.

        Returns:
            None: Executes a jump command and waits briefly for sync.
        """
        if self.bot.player.CELL.lower() != cell.lower() or self.bot.player.PAD.lower() != pad.lower():
            self.bot.jump_cell(cell, pad)
            #print(f"jump cell: {cell} {pad}")
            await asyncio.sleep(1)

    def is_not_in_cell(self, cell: str) -> bool:
        """Check whether the player is standing in a different cell.

        Args:
            cell (str): Cell name to compare with the current position.

        Returns:
            bool: True when the active cell does not match ``cell``.
        """
        return self.bot.player.CELL.lower() != cell.lower()

    @check_alive
    async def walk_to(self, X: int, Y: int, speed: int = 8) -> None:
        """Walk to a coordinate within the current map.

        Args:
            X (int): Target X coordinate.
            Y (int): Target Y coordinate.
            speed (int): Movement speed for the walk animation."""
        await self.bot.walk_to(X, Y, speed)
        await self.sleep(200)
