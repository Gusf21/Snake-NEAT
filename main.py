import os.path
import random
import time

import neat
from neat import *
import pygame as pg


def setup():
    pg.init()
    dy = pg.display.set_mode((400, 400))
    pg.display.set_caption("Snake")
    pg.display.update()
    return dy


def snake(snakeList):
    for x in snakeList:
        pg.draw.rect(display, (0, 0, 255), [x[0], x[1], 20, 20])


def Game():
    global display
    playing = True
    x1 = 300
    y1 = 300
    x1_change = 0
    y1_change = 0
    snake_speed = 10
    displayX = 400
    displayY = 400
    score = 0

    clock = pg.time.Clock()

    display = setup()
    foodX = round(random.randrange(0, displayX - 20) / 20) * 20
    foodY = round(random.randrange(0, displayY - 20) / 20) * 20
    snake_List = []
    lengthOfSnake = 1

    while playing:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    x1_change = 0
                    y1_change = -20
                    print("Moving Up")
                elif event.key == pg.K_a:
                    x1_change = -20
                    y1_change = 0
                    print("Moving Left")
                elif event.key == pg.K_s:
                    x1_change = 0
                    y1_change = 20
                    print("Moving Down")
                elif event.key == pg.K_d:
                    x1_change = 20
                    y1_change = 0
                    print("Moving Right")
        if x1 >= displayX or x1 < 0 or y1 >= displayY or y1 < 0:
            playing = False
        print(x1)
        print(y1)
        x1 += x1_change
        y1 += y1_change
        display.fill((255, 255, 255))
        #pg.draw.rect(display, (0, 0, 255), [x1, y1, 20, 20])
        pg.draw.rect(display, (255, 0, 0), [foodX, foodY, 20, 20])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        #print(snake_Head)
        snake_List.append(snake_Head)
        #print(snake_List)
        if len(snake_List) > lengthOfSnake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                playing = False

        snake(snake_List)

        pg.display.update()

        if x1 == foodX and y1 == foodY:
            print("eat")
            foodX = round(random.randrange(0, displayX - 20) / 20) * 20
            foodY = round(random.randrange(0, displayY - 20) / 20) * 20
            lengthOfSnake += 1
            score += 1

        clock.tick(snake_speed)

    display.blit((pg.font.SysFont(None, 50).render("You Lost", True, (255, 0, 0))), [displayX / 2, displayY / 2])
    pg.display.update()
    time.sleep(2)
    print(score)
    pg.quit()
    quit()

Game()


def run(configP):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(Game, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "Config")
    run(config_path)
