import pygame

from libs.collision_system import CollisionSystem
from libs.randomizer import Randomizer
from libs.high_score import HighScore

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

# Static Variables
PLAYER_COLOR = (15, 56, 15)
BALL_COLOR = (48, 98, 48)
BACKGROUND_COLOR = (155, 188, 15)
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
BALL_WIDTH = 8
INITIAL_BALL_SPEED = 6
ORIGINAL_BALL_MOVEMENT = Randomizer.get_initial_ball_movement(INITIAL_BALL_SPEED)

# Variables
game_state = "start_menu"
collision_sys = CollisionSystem(SCREEN_HEIGHT, SCREEN_WIDTH, BALL_WIDTH)

# Text
pygame.font.init()
menus_font = pygame.font.Font('fonts/early_gameboy.ttf', 110)
score_font = pygame.font.Font('fonts/early_gameboy.ttf', 60)
start_game_font = pygame.font.Font('fonts/early_gameboy.ttf', 30)
hs_score_font = pygame.font.Font('fonts/early_gameboy.ttf', 20)
credits_font = pygame.font.Font('fonts/early_gameboy.ttf', 15)

# Music
pygame.mixer.init()
pygame.mixer.music.load("music/The Pong Song.mp3")
pygame.mixer.music.play(-1)

# High Score File
high_score_file = open("docs/high_score.txt", "r")
high_score = high_score_file.read()
high_score = int(high_score) if high_score.strip() else 0
high_score_file.close()


# Running program
while running:
    for event in pygame.event.get():
        # If pressed "X", quit
        if event.type == pygame.QUIT:
            running = False
            
        # If button "Start game" or "Restart", start game
        if game_state != "game" and event.type == pygame.MOUSEBUTTONDOWN:
            if start_game_text_rect.collidepoint(event.pos):
                game_state = "game"
                
                # Variables for game start
                player_score = 0
                player = pygame.Rect(SCREEN_WIDTH/15, (SCREEN_HEIGHT/2)-65, 20, 130)
                rival = pygame.Rect(14*(SCREEN_WIDTH/15), (SCREEN_HEIGHT/2)-65, 20, 130)
                ball_placement = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                ball_movement = Randomizer.get_initial_ball_movement(INITIAL_BALL_SPEED)
            
            
    screen.fill(BACKGROUND_COLOR)
    
    if game_state == "start_menu":
        title_text_surface = menus_font.render(f'PONG!', False, PLAYER_COLOR)
        title_text_rect = title_text_surface.get_rect(center=(SCREEN_WIDTH/2, 4*(SCREEN_HEIGHT/10)))
        
        credits_text_surface = hs_score_font.render(f'Game and Music By Cesar Morais', False, PLAYER_COLOR)
        credits_text_rect = credits_text_surface.get_rect(center=(SCREEN_WIDTH/2, 9*(SCREEN_HEIGHT/10)))
        
        start_game_text_surface = start_game_font.render(f'Start Game', False, BALL_COLOR)
        start_game_text_rect = start_game_text_surface.get_rect(center=(SCREEN_WIDTH/2, 12*(SCREEN_HEIGHT/20)))
        
        screen.blit(title_text_surface, title_text_rect)
        screen.blit(credits_text_surface, credits_text_rect)
        screen.blit(start_game_text_surface, start_game_text_rect)
        
        
    elif game_state == "game":
        # Move player
        player_collision = collision_sys.vertical_collision(player.top, player.bottom)
        pressed=pygame.key.get_pressed()
        if player_collision == 'N':
            player.y += 1
        elif player_collision == 'S':
            player.y -= 1
        else:
            if pressed[pygame.K_w]:
                player.y -= 5
            elif pressed[pygame.K_s]:
                player.y += 5
        
        # Move ball
        ball_edge_collision = collision_sys.collision_with_four_edges(ball_placement)
        ball_player_collision = collision_sys.ball_collided_with_player(ball_placement, player)
        ball_rival_collision = collision_sys.ball_collided_with_rival(ball_placement, rival)
        
        if ball_edge_collision == 'W':   # Lost
            game_state = "game_over"
            high_score = HighScore.change_high_score(player_score, high_score)
        elif ball_edge_collision == 'E':  # Score!
            player_score += 1
            ball_placement = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            ball_movement = Randomizer.get_initial_ball_movement(INITIAL_BALL_SPEED)
        elif ball_edge_collision != 'F':  # Hit upper/lower screen
            ball_movement = (ball_movement[0], -ball_movement[1])
        elif ball_player_collision == True or ball_rival_collision == True:     # Hit a player
            ball_movement = Randomizer.get_new_ball_movement(ball_movement)
        ball_placement = tuple(map(lambda i, j: i + j, ball_placement, ball_movement))
        
        # Move rival
        rival_collision = collision_sys.vertical_collision(rival.top, rival.bottom)
        if rival_collision == 'N':
            rival.y += 1
        elif rival_collision == 'S':
            rival.y -= 1
        elif (ball_placement[0] > 2*(SCREEN_WIDTH/5)):
            if rival.center[1] > ball_placement[1]:
                rival.y -= 5
            elif rival.center[1] < ball_placement[1]:
                rival.y += 5
            
        # Draw stuff
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.draw.rect(screen, PLAYER_COLOR, rival)
        pygame.draw.circle(screen, BALL_COLOR, ball_placement, BALL_WIDTH)
        
        # Draw text
        score_text_surface = score_font.render(f'Score: {player_score}', False, BALL_COLOR)
        score_text_rect = score_text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/10))

        hs_text_surface = hs_score_font.render(f'High Score: {high_score}', False, PLAYER_COLOR)
        hs_text_rect = hs_text_surface.get_rect(center=(SCREEN_WIDTH/2, 7*(SCREEN_HEIGHT/40)))
        
        screen.blit(score_text_surface, score_text_rect)
        screen.blit(hs_text_surface, hs_text_rect)
        
    elif game_state == "game_over":
        # Render text
        title_text_surface = score_font.render(f'GAME OVER', False, PLAYER_COLOR)
        title_text_rect = title_text_surface.get_rect(center=(SCREEN_WIDTH/2, 4*(SCREEN_HEIGHT/10)))
        
        start_game_text_surface = start_game_font.render(f'Restart', False, BALL_COLOR)
        start_game_text_rect = start_game_text_surface.get_rect(center=(SCREEN_WIDTH/2, 11*(SCREEN_HEIGHT/20)))
        
        screen.blit(title_text_surface, title_text_rect)
        screen.blit(start_game_text_surface, start_game_text_rect)


    # Rendering stuff
    pygame.display.flip()
    dt = clock.tick(60) / 1000

high_score_file.close()

pygame.quit()