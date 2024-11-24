# TO-DO
#   POLISH RESTART
#   MAKE IT SO THAT FOOD SPAWNS IN A SPOT NOT OCCUPIED BY SNAKE

import pygame
from random import randint

def move_right(snake):
    x_pos = snake[0].left + 10
    y_pos = snake[0].y + 5
    new_head = snake_surf.get_rect(midleft = (x_pos, y_pos))
    snake.pop(-1)
    snake.insert(0, new_head)

def move_left(snake):
    x_pos = snake[0].right - 10
    y_pos = snake[0].y + 5
    new_head = snake_surf.get_rect(midright = (x_pos, y_pos))
    snake.pop(-1)
    snake.insert(0, new_head)

def move_down(snake):
    x_pos = snake[0].x + 5
    y_pos = snake[0].top + 10
    new_head = snake_surf.get_rect(midtop = (x_pos, y_pos))
    snake.pop(-1)
    snake.insert(0, new_head)

def move_up(snake):
    x_pos = snake[0].x + 5
    y_pos = snake[0].bottom - 10
    new_head = snake_surf.get_rect(midbottom = (x_pos, y_pos))
    snake.pop(-1)
    snake.insert(0, new_head)

def movement(move):
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and not(move == move_down):
        return move_up
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not(move == move_up):
        return move_down
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not(move == move_left):
        return move_right
    elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not(move == move_right):
        return move_left
    else:
        return move

def grow(movement):
    if movement == move_right:
        x_pos = snake[0].left + 10
        y_pos = snake[0].y + 5
        new_head = snake_surf.get_rect(midleft = (x_pos, y_pos))
        snake.insert(0, new_head)
    elif movement == move_left:
        x_pos = snake[0].right - 10
        y_pos = snake[0].y + 5
        new_head = snake_surf.get_rect(midright = (x_pos, y_pos))
        snake.insert(0, new_head)
    elif movement == move_down:
        x_pos = snake[0].x + 5
        y_pos = snake[0].top + 10
        new_head = snake_surf.get_rect(midtop = (x_pos, y_pos))
        snake.insert(0, new_head)
    elif movement == move_up:
        x_pos = snake[0].x + 5
        y_pos = snake[0].bottom - 10
        new_head = snake_surf.get_rect(midbottom = (x_pos, y_pos))
        snake.insert(0, new_head)

def lose_check(snake):
    for n in range(2, len(snake)-1):
        if snake[0].colliderect(snake[n]):
            return True

    if snake[0].left <= 0:
        return True
    elif snake[0].right >= 500:
        return True
    elif snake[0].top <= 0:
        return True
    elif snake[0].bottom >= 300:
        return True

def setup_snake():
    # SNAKE START POSITIONS
    snake_start_right = [snake_surf.get_rect(center = (n, 150)) for n in range(250, 190, -10)]
    snake_start_left = [snake_surf.get_rect(center = (n, 150)) for n in range(250, 310, 10)]
    snake_start_down = [snake_surf.get_rect(center = (250, n)) for n in range(150, 90, -10)]
    snake_start_up = [snake_surf.get_rect(center = (250, n)) for n in range(150, 210, 10)]

    # RANDOM START DIRECTION
    choice = randint(0, 3)
    snake = [snake_start_right, snake_start_left, snake_start_down, snake_start_up][choice]
    move = [move_right, move_left, move_down, move_up][choice]
    return snake, move

def spawn_food(snake):
    x_pos = (randint(3, 47) * 10) - 5
    y_pos = (randint(3, 27) * 10) - 5
    invalid_spot = [(rect.x, rect.y) for rect in snake]
    while (x_pos, y_pos) in invalid_spot:
        x_pos = (randint(3, 47) * 10) - 5
        y_pos = (randint(3, 27) * 10) - 5
    food = pygame.Rect(x_pos, y_pos, 10, 10)
    return food

def display_score():
    score_surf = score_font.render(f"{score}", False, "#6c8773")
    score_rect = score_surf.get_rect(center = (250, 140))
    try_again = text_font.render("press any key to try again", False, "#6c8773")
    try_again_rect = try_again.get_rect(center = (250, 170))
    screen.fill("#132116")
    screen.blit(score_surf, score_rect)
    screen.blit(try_again, try_again_rect)

pygame.init()
screen = pygame.display.set_mode((500, 300))
clock = pygame.time.Clock()

snake_surf = pygame.Surface((10, 10))
snake_surf.fill("#6c8773")
snake, move = setup_snake()

# FOOD
food_surf = pygame.Surface((10, 10))
# food_surf.fill("White")
food = spawn_food(snake)

# SCORE
score = 0
score_font = pygame.font.Font(None, 80)
text_font = pygame.font.Font(None, 40)

start_time = 0
game_state = "PLAY"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if game_state == "SCORE":
            if event.type == pygame.KEYDOWN:
                game_state = "PLAY"
                score = 0

    current_time = pygame.time.get_ticks() - start_time

    if game_state == "PLAY":
        screen.fill("#132116")
        for rect in snake: 
            screen.blit(snake_surf, rect)
        pygame.draw.ellipse(screen, "#874545", food)

        move = movement(move)
        move(snake)

        if snake[0].colliderect(food):
            grow(move)
            score += 1
            food = spawn_food(snake)

        if lose_check(snake):
            game_state = "WAIT"
            start_time = pygame.time.get_ticks()
        
    elif game_state == "WAIT":
        screen.fill("#132116")
        for rect in snake: 
            screen.blit(snake_surf, rect)
        pygame.draw.ellipse(screen, "#874545", food)
        
        if current_time >= 2000:
            game_state = "SCORE"
            snake, move = setup_snake()
            food = spawn_food(snake)

    elif game_state == "SCORE":
        display_score()


    pygame.display.update()
    clock.tick(15)