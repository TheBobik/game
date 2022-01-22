import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

size = 850

screen = pygame.display.set_mode((size, size))
pygame.display.set_caption('Snake Game by Pythonist')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 20

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(screen, black, [i[0], i[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [size / 3, size / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = size / 2
    y1 = size / 2

    x_change = 0
    y_change = 0

    snake_List = []
    length = 1

    food_x = round(random.randrange(0, size - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, size - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            screen.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        if x1 >= size or x1 < 0 or y1 >= size or y1 < 0:
            game_close = True
        x1 += x_change
        y1 += y_change
        screen.fill(blue)
        pygame.draw.rect(screen, green, [food_x, food_y, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List) > length:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(length - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(200, size - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(200, size - snake_block) / 10.0) * 10.0
            length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
