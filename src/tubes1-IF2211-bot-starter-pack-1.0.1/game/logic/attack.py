from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class AttackLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = None
        
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
            # find the nearest diamond
            min_distance = 1000000
            nearest_diamond = None
            
            # find the nearest diamond and enemy bot
            for diamond in board.diamonds:
                distance = abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_diamond = diamond
            
            # Check for enemy bots
            for enemy_bot in board.bots:
                if enemy_bot != board_bot:  # Avoid detecting itself
                    distance = abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y)
                    if distance < min_distance:
                        min_distance = distance
                        self.goal_position = enemy_bot.position
            
            # If there is a nearest diamond, set it as the goal
            if nearest_diamond:
                self.goal_position = nearest_diamond.position

            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y
