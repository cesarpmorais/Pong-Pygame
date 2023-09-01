
class CollisionSystem:
    def __init__(self, screen_height, screen_width, ball_width):
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.ball_width = ball_width
        
    def collision_with_four_edges(self, value: tuple):
        if value[0] < self.screen_width/30:
            return 'W'
        elif value[0] > (self.screen_width - (self.screen_width/38)):
            return 'E'
        elif value[1] < 0:
            return 'N'
        elif value[1] > self.screen_height:
            return 'S'
        return 'F'
    
    def vertical_collision(self, top, bottom):
        if top < 0:
            return "N"
        elif bottom > self.screen_height:
            return "S"
        return "F"
    
    def ball_collided_with_player(self, ball_center: tuple, rect):
        ball_spot = (ball_center[0]-(self.ball_width/2), ball_center[1])
        rect_x = rect.x + 2*(rect.width/2)
        
        if (ball_spot[0] < rect_x and (ball_spot[1] > rect.top and ball_spot[1] < rect.bottom)):
            return True
        return False
    
    def ball_collided_with_rival(self, ball_center: tuple, rect):
        ball_spot = (ball_center[0]+(self.ball_width/2), ball_center[1])
        
        if (ball_spot[0] > rect.x and (ball_spot[1] > rect.top and ball_spot[1] < rect.bottom)):
            return True
        return False