from random import randint

SMOOTH_BALL_DIR_CHANGE = (-3, 3)
NORMAL_BALL_DIR_CHANGE = (-5, 5)

PERCENTAGE_CHANCE = (1, 10)

class Randomizer:
    @classmethod
    def get_initial_ball_movement(cls, initial_speed: int):
        return (-initial_speed, randint(*SMOOTH_BALL_DIR_CHANGE))
    
    @classmethod
    def get_new_ball_movement(cls, ball_movement: tuple):
        ball_x_movement = ball_movement[0]
        ball_y_movement = ball_movement[1]
        
        speed_up = randint(*PERCENTAGE_CHANCE)
        direction_change = randint(*PERCENTAGE_CHANCE)
        
        # Change speed with 20% chance
        if speed_up > 8:
            if ball_x_movement < 0:
                ball_x_movement -= 1
            else:
                ball_x_movement += 1
                
        # If ball's moving straight, change direction with 80% chance;
        # Else, 30% of direction change
        if ball_y_movement == 0:
            if direction_change > 2:
                ball_y_movement = randint(*SMOOTH_BALL_DIR_CHANGE)
        elif direction_change > 7:
            ball_y_movement = randint(*NORMAL_BALL_DIR_CHANGE)
                
        return (-ball_x_movement, ball_y_movement)