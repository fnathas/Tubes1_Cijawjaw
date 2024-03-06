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

        # Check if there are nearby enemy bots
        nearby_enemy_bots = [enemy_bot for enemy_bot in board.bots if enemy_bot != board_bot and self.is_nearby(current_position, enemy_bot.position)]

        if nearby_enemy_bots:
            # Attack the nearest enemy bot carrying diamonds
            enemy_bots_with_diamonds = [enemy_bot for enemy_bot in nearby_enemy_bots if enemy_bot.properties.diamonds > 0]
            if enemy_bots_with_diamonds:
                nearest_enemy_bot = min(enemy_bots_with_diamonds, key=lambda bot: self.calculate_distance(current_position, bot.position))
                self.goal_position = nearest_enemy_bot.position
            else:
                # Roam around and find the nearest diamond, but avoid diamonds if inventory is almost full
                if props.diamonds < 4:
                    self.goal_position = self.find_nearest_diamond(current_position, board.diamonds)
                else:
                    # Choose between picking up a diamond or returning to base
                    nearest_diamond_position = self.find_nearest_diamond(current_position, board.diamonds)
                    distance_to_base = self.calculate_distance(current_position, props.base)
                    distance_to_nearest_diamond = self.calculate_distance(current_position, nearest_diamond_position)

                    if distance_to_nearest_diamond < distance_to_base:
                        self.goal_position = nearest_diamond_position
                    else:
                        self.goal_position = props.base
        elif props.diamonds == 5:
            # Move to base if carrying 5 diamonds
            self.goal_position = props.base
        else:
            # Roam around and find the nearest diamond, but avoid diamonds if inventory is almost full
            if props.diamonds < 4:
                self.goal_position = self.find_nearest_diamond(current_position, board.diamonds)
            else:
                # Choose between picking up a diamond or returning to base
                nearest_diamond_position = self.find_nearest_diamond(current_position, board.diamonds)
                distance_to_base = self.calculate_distance(current_position, props.base)
                distance_to_nearest_diamond = self.calculate_distance(current_position, nearest_diamond_position)

                if distance_to_nearest_diamond < distance_to_base:
                    self.goal_position = nearest_diamond_position
                else:
                    self.goal_position = props.base

        # Calculate delta to reach the goal position
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y

    def is_nearby(self, position1: Position, position2: Position, distance_threshold: int = 1):
        """Check if two positions are nearby within a given distance threshold."""
        distance = abs(position1.x - position2.x) + abs(position1.y - position2.y)
        return distance <= distance_threshold

    def calculate_distance(self, position1: Position, position2: Position):
        """Calculate the distance between two positions."""
        return abs(position1.x - position2.x) + abs(position1.y - position2.y)

    def find_nearest_diamond(self, current_position: Position, diamonds: list[GameObject]):
        """Find the nearest diamond from the current position."""
        min_distance = float('inf')
        nearest_diamond_position = None

        for diamond in diamonds:
            distance = self.calculate_distance(current_position, diamond.position)
            if distance < min_distance:
                min_distance = distance
                nearest_diamond_position = diamond.position

        return nearest_diamond_position
