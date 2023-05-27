import math
import os.path
import random
import time
import neat
import pygame as pg


def draw_window():
    displayX = 400
    displayY = 400
    pg.init()
    dy = pg.display.set_mode((displayX, displayY))
    pg.display.set_caption("Snake")
    pg.display.update()
    return dy


class Snake:
    displayX = 400
    displayY = 400

    def __init__(self, x, y, screen):
        self.foodY = 0
        self.foodX = 0
        self.x = x
        self.y = y
        self.xChange = 0
        self.yChange = 0
        self.snakeList = []
        self.dead = False
        self.score = 0
        self.screen = screen
        self.lastFood = time.time()
        self.lastMove = 0

    def createFood(self):
        self.foodX = round(random.randrange(0, 400 - 20) / 20) * 20
        self.foodY = round(random.randrange(0, 400 - 20) / 20) * 20
        pg.draw.rect(self.screen, (255, 0, 0), [self.foodX, self.foodY, 20, 20])
        pg.display.update()

    def foodCollision(self):
        hit = False
        if self.x == self.foodX and self.y == self.foodY:
            self.score += 1
            self.lastFood = time.time()
            self.createFood()
            print(self.score)
            hit = True
        else:
            pg.draw.rect(self.screen, (255, 0, 0), [self.foodX, self.foodY, 20, 20])
            pg.display.update()
        return hit

    def create(self):
        pg.draw.rect(self.screen, (0, 0, 255), [self.x, self.y, 20, 20])
        pg.display.update()

    def snakeRender(self):
        for x in self.snakeList:
            pg.draw.rect(self.screen, (0, 0, 255), [x[0], x[1], 20, 20])

    def moveUp(self):
        if self.lastMove == 4:
            self.dead = True
        self.xChange = 0
        self.yChange = 20
        self.lastMove = 1

    def moveLeft(self):
        if self.lastMove == 3:
            self.dead = True
        self.xChange = -20
        self.yChange = 0
        self.lastMove = 2

    def moveRight(self):
        if self.lastMove == 2:
            self.dead = True
        self.xChange = 20
        self.yChange = 0
        self.lastMove = 3

    def moveDown(self):
        if self.lastMove == 1:
            self.dead = True
        self.xChange = 0
        self.yChange = -20
        self.lastMove = 4

    def distanceToFood(self):
        xDifference = abs(self.x - self.foodX)
        yDifference = abs(self.y - self.foodY)
        difference = math.sqrt((xDifference ** 2) + (yDifference ** 2))
        return difference

    def move(self):
        if self.x >= 400 or self.x < 0 or self.y >= 400 or self.y < 0:
            self.dead = True

        self.x += self.xChange
        self.y += self.yChange
        snakeHead = (self.x, self.y)
        self.snakeList.append(snakeHead)

        if len(self.snakeList) > self.score + 1:
            del self.snakeList[0]

        for x in self.snakeList[:-1]:
            if x == snakeHead:
                self.dead = True

        if time.time() - self.lastFood > 5:
            self.dead = True
        self.snakeRender()
        pg.display.update()
        return self.dead


# class keyHandler:

#    def __init__(self, up, down, left, right):
#        self.up = up
#        self.down = down
#        self.left = left
#        self.right = right
#
#    def checkKeys(self, keyPress):
#        if keyPress == self.up:
#            myEvent = move_up
#        elif keyPress == self.left:
#            myEvent = move_left
#        elif keyPress == self.down:
#            myEvent = move_down
#        elif keyPress == self.right:
#            myEvent = move_right
#        return myEvent


def Game(genomes, config):
    display = draw_window()

    nets = []
    ge = []
    snakes = []

    #   start snakes and assign them genomes and neural networks
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake(200, 200, display))
        g.fitness = 0
        ge.append(g)

    clock = pg.time.Clock()

    #   create snakes and their first food item
    for snake in snakes:
        snake.create()
        snake.createFood()

    pg.display.update()

    while snakes:

        display.fill((255, 255, 255))

        for x, snake in enumerate(snakes):

            outputs = nets[x].activate([snake.x, snake.y, snake.distanceToFood(), snake.foodX, snake.foodY, 400, 400])

#           calculate the next input
            if max(outputs) == outputs[0]:
                snake.moveUp()
            elif max(outputs) == outputs[1]:
                snake.moveLeft()
            elif max(outputs) == outputs[2]:
                snake.moveRight()
            elif max(outputs) == outputs[3]:
                snake.moveDown()

            punish = snake.move()
            if snake.distanceToFood() > 0:
                ge[x].fitness += (1 / snake.distanceToFood())

            if punish:
                ge[x].fitness -= 10
                snakes.pop(x)
                nets.pop(x)
                ge.pop(x)

            reward = snake.foodCollision()

            if reward:
                ge[x].fitness += 5


def run(configP):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(Game, 500)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "Config")
    run(config_path)
