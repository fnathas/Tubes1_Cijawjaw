import heapq
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class GreedyLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def next_move(self, board_bot: GameObject, board: Board):
        temp: List[GameObject] = [
            d for d in board.game_objects if d.type == "DiamondButtonGameObject"
        ]
        button: GameObject = temp[0]
        props = board_bot.properties
        print(board)
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
            # Create a list to use as a priority queue
            diamonds_queue = []
            for index, diamond in enumerate(board.diamonds):
                distance = abs(diamond.position.x - current_position.x) + abs(diamond.position.y - current_position.y)
                # Use the distance as the priority
                heapq.heappush(diamonds_queue, (distance, index))
            
            # Get the diamond with the smallest distance
            if props.diamonds == 4:
                if board.diamonds[0].properties.points == 1:
                    min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                    # if the distance to the base is nearer than the nearest diamond, move to the base
                    if (abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y)) < min_distance and props.diamonds != 0:
                        self.goal_position = props.base
                    else:
                        self.goal_position = board.diamonds[nearest_diamond_index].position
                else:
                    min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                    if (abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y)) < min_distance and props.diamonds != 0:
                        min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                        self.goal_position = props.base
                    else:
                        min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                        self.goal_position = board.diamonds[nearest_diamond_index].position 
            else:          
                min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                if (abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y)) < min_distance and props.diamonds != 0:
                        self.goal_position = props.base
                else:
                    self.goal_position = board.diamonds[nearest_diamond_index].position

            # if the distance to the base is the same with the time left, move to the base
            if (props.milliseconds_left / 1000) <= (abs(props.base.x - current_position.x) + abs(props.base.y - current_position.y) + 2):
                self.goal_position = props.base
            
            if (props.milliseconds_left / 1000) < 1:
                min_distance, nearest_diamond_index = heapq.heappop(diamonds_queue)
                self.goal_position = board.diamonds[nearest_diamond_index].position 

            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y
