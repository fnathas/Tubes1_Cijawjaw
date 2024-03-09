import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class GreedyLogic2(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.current_direction = 0

    def find_nearest_diamond(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        diamonds_positions = [diamond.position for diamond in board.diamonds]

        if diamonds_positions:
            # Find the nearest diamond using the Manhattan distance
            min_distance = float('inf')
            for diamond_position in diamonds_positions:
                distance = abs(current_position.x - diamond_position.x) + abs(current_position.y - diamond_position.y)
                if distance < min_distance:
                    min_distance = distance
                    self.goal_position = diamond_position

    def next_move(self, board_bot: GameObject, board: Board):
        temp: List[GameObject] = [
            d for d in board.game_objects if d.type =="TeleportGameObject"
        ]
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5 or props.milliseconds_left < 10000:
            # Move to base
            self.goal_position = board_bot.properties.base
        else:
            # Find the nearest diamond
            self.find_nearest_diamond(board_bot, board)

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam towards the nearest diamond
            delta_x, delta_y = self.directions[self.current_direction]

            # Check if a random move should be made
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )

        return delta_x, delta_y
