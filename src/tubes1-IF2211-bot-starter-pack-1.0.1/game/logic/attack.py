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
        current_position = board_bot.position

        # Calculate distance to base
        distance_to_base = abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y)
        
        if props.diamonds == 5 or distance_to_base < 3:
            # Move to base
            self.goal_position = props.base
        else:
            # Just roam around
            self.goal_position = None
        
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
            min_distance_diamond = 1000000
            nearest_diamond = None
            
            # find the nearest diamond
            for diamond in board.diamonds:
                distance = abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
                if distance < min_distance_diamond:
                    min_distance_diamond = distance
                    nearest_diamond = diamond
            
            # find the nearest enemy bot
            min_distance_bot = 1000000
            nearest_bot = None
            
            for enemy_bot in board.bots:
                if enemy_bot != board_bot:  # Avoid detecting itself
                    distance = abs(enemy_bot.position.x - current_position.x) + abs(enemy_bot.position.y - current_position.y)
                    if distance < min_distance_bot:
                        min_distance_bot = distance
                        nearest_bot = enemy_bot
            
            # Compare distances and set the appropriate goal
            if min_distance_diamond < min_distance_bot and min_distance_diamond < distance_to_base:
                self.goal_position = nearest_diamond.position
            elif nearest_bot and min_distance_bot < distance_to_base:
                self.goal_position = nearest_bot.position

            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y