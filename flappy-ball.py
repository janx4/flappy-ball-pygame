import pygame as pg
import random
from pygame import mixer

# ***************************************
# * Author            : Cong Huy        *
# * Date of Execution : Nov 17th, 2020  *
# * Made with love and improving skills *
# ***************************************

pg.init()
WIDTH = 600
HEIGHT = 700
MIN_RANGE = 250
MAX_RANGE = 450
SIZE_BORDER = 7

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Something from CongHuy Dev :)")
clock = pg.time.Clock()

bg_image = pg.image.load("assets/bg.jpg")
icon_image = pg.image.load("assets/icon.png")
mixer.music.load("assets/music.wav")
pg.display.set_icon(icon_image)
mixer.music.play(-1)

font_30 = pg.font.SysFont('cons', 30)
font_40 = pg.font.SysFont('cons', 40)

# color
RED = (255, 31, 94)
BLACK = (5, 5, 5)
WHITE = (255, 255, 255)
YELLOW = (255, 247, 0)
GREEN = (31, 255, 53)
BLUE = (12, 78, 245)
PURPLE = (242, 12, 250)
ORANGE = (250, 159, 12)
STD_ORANGE = (255, 123, 0)
GRAY = (150, 136, 132)
AQUA = (20, 247, 255)
DARK_PINK = (250, 10, 118)
BRIGHT_GREEN = (77, 250, 20)
DARK_GREEN = (52, 135, 16)
LIGHT_PURPLE = (192, 72, 240)
BROWN = (199, 139, 18)
STD_RED = (255, 0, 17)

ball_color = WHITE
set_color = (STD_ORANGE, STD_RED, DARK_GREEN, YELLOW, GREEN, BLUE, PURPLE,
             ORANGE, GRAY, AQUA, DARK_PINK, BRIGHT_GREEN, BROWN, LIGHT_PURPLE)
color1 = random.choice(set_color)
color2 = random.choice(set_color)
color3 = random.choice(set_color)

# Checking variable
running = True
status_game = True
pass_tube = False
pause_status = False
ready = False

FPS = 60
score = 0

# Variable game
BALL_X = WIDTH // 9
BALL_Y = HEIGHT // 2
BALL_RADIUS = 25
ball_drop_velocity = 2.5
GRAVITY = 0.65

TUBE_GAP = 190
TUBE_WIDTH = 85
TUBE_VELOCITY = 3

tube1_x = 550
tube2_x = 850
tube3_x = 1150
tube1_height = random.randint(MIN_RANGE, MAX_RANGE)
tube2_height = random.randint(MIN_RANGE, MAX_RANGE)
tube3_height = random.randint(MIN_RANGE, MAX_RANGE)

while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    screen.blit(bg_image, (0, 0))
    pause_status = False
    # Draw tubes
    tube1 = pg.draw.rect(screen, color1, (tube1_x, 0, TUBE_WIDTH, tube1_height))
    tube2 = pg.draw.rect(screen, color2, (tube2_x, 0, TUBE_WIDTH, tube2_height))
    tube3 = pg.draw.rect(screen, color3, (tube3_x, 0, TUBE_WIDTH, tube3_height))

    tube1_inverse = pg.draw.rect(screen, color1,
                                 (tube1_x, tube1_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube1_height - TUBE_GAP))
    tube2_inverse = pg.draw.rect(screen, color2,
                                 (tube2_x, tube2_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube2_height - TUBE_GAP))
    tube3_inverse = pg.draw.rect(screen, color3,
                                 (tube3_x, tube3_height + TUBE_GAP, TUBE_WIDTH, HEIGHT - tube3_height - TUBE_GAP))
    # Create list of the drawing tubes
    list_tube = [tube1, tube2, tube3, tube1_inverse, tube2_inverse, tube3_inverse]
    ball = pg.draw.circle(screen, ball_color, (BALL_X, BALL_Y), BALL_RADIUS)
    if ready:
        tube1_x -= TUBE_VELOCITY
        tube2_x -= TUBE_VELOCITY
        tube3_x -= TUBE_VELOCITY

    # Draw the ball

        BALL_Y += ball_drop_velocity
        ball_drop_velocity += GRAVITY

    if tube1_x <= -TUBE_WIDTH:
        tube1_x = 1.5 * WIDTH - TUBE_WIDTH
        tube1_height = random.randint(MIN_RANGE, MAX_RANGE)
        color1 = random.choice(set_color)
        pass_tube = False
    if tube2_x <= -TUBE_WIDTH:
        tube2_x = 1.5 * WIDTH - TUBE_WIDTH
        tube2_height = random.randint(MIN_RANGE, MAX_RANGE)
        color2 = random.choice(set_color)
        pass_tube = False
    if tube3_x <= -TUBE_WIDTH:
        tube3_x = 1.5 * WIDTH - TUBE_WIDTH
        tube3_height = random.randint(MIN_RANGE, MAX_RANGE)
        color3 = random.choice(set_color)
        pass_tube = False

    # Change color of the ball
    if BALL_X >= tube1_x:
        ball_color = color1
    if BALL_X >= tube2_x:
        ball_color = color2
    if BALL_X >= tube3_x:
        ball_color = color3

    # Calculate score and show it on screen
    for check in [tube1_x, tube2_x, tube3_x]:
        if (BALL_X >= check + TUBE_WIDTH) and not pass_tube:
            score += 1
            pass_tube = True
    score_txt = font_30.render("Your Score : " + str(score), True, RED)
    screen.blit(score_txt, (10, 10))

    for tube in list_tube:
        if ball.colliderect(tube) or BALL_Y >= HEIGHT + BALL_RADIUS:
            pause_status = True
            ball_drop_velocity = 0
            TUBE_VELOCITY = 0
            status_game = False
            pg.draw.rect(screen, WHITE, (WIDTH // 8.5, 47 * HEIGHT // 100, 13 * WIDTH // 17, HEIGHT // 6))
            pg.draw.rect(screen, RED, (
                WIDTH // 8.5 + SIZE_BORDER, 47 * HEIGHT // 100 + SIZE_BORDER, 13 * WIDTH // 17 - 2 * SIZE_BORDER,
                HEIGHT // 6 - 2 * SIZE_BORDER))

            game_over = font_40.render("Press Space to Play Again !", True, WHITE)
            score_txt = font_40.render("YOUR SCORE : " + str(score), True, WHITE)
            screen.blit(game_over, (WIDTH // 5, HEIGHT // 2))
            screen.blit(score_txt, (WIDTH // 3.2, 57 * HEIGHT // 100))
    # Process event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                ready = True
                if status_game:
                    ball_drop_velocity = 0
                    ball_drop_velocity -= 10
                if pause_status:
                    ready = False
                    status_game = True
                    BALL_Y = HEIGHT // 2
                    TUBE_VELOCITY = 3
                    tube1_x = 550
                    tube2_x = 850
                    tube3_x = 1150
                    ball_drop_velocity = 2.5
                    score = 0
                    ball_color = WHITE
    pg.display.flip()
pg.quit()

# made with 3000 <3