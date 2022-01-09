import random as rd
import sys

import pygame

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

GRIDSIZE = 25
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class snakes(object):
    def __init__(self):
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.color = (0, 64, 255)
        self.length = 1
        self.direction = rd.choice([UP, DOWN, LEFT, RIGHT])
        self.score_count = 0

    def get_snake_position(self):
        return self.positions[0]

    def move(self):
        current_position = self.get_snake_position()
        x, y = self.direction
        new = (
            ((current_position[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
            (current_position[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = rd.choice([UP, DOWN, LEFT, RIGHT])
        self.score_count = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (170, 215, 81), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class foods(object):
    def __init__(self):
        self.positions = (0, 0)
        self.color = (202, 0, 42)
        self.get_food_positions()

    def get_food_positions(self):
        self.positions = (rd.randint(0, GRID_WIDTH - 1) * GRIDSIZE, rd.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw_food(self, surface):
        r = pygame.Rect((self.positions[0], self.positions[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (170, 215, 81), r, 1)


class bombs(object):
    def __init__(self):
        self.positions = (0, 0)
        self.color = (0, 0, 0)
        self.get_bomb_positions()

    def get_bomb_positions(self):
        self.positions = (rd.randint(0, GRID_WIDTH - 1) * GRIDSIZE, rd.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)

    def draw_bomb(self, surface):
        r = pygame.Rect((self.positions[0], self.positions[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (170, 215, 81), r, 1)


def draw_background(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (170, 215, 81), r)
            else:
                g = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (162, 209, 73), g)


white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Snake Attack")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_background(surface)

    snake_obj = snakes()
    food_obj = foods()
    bomb_obj = bombs()

    font1 = pygame.font.SysFont("monospace", 16)

    score_count = 0

    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText

    font = "Retro.ttf"

    def main1():
        while (True):
            clock.tick(10)
            snake_obj.handle_keys()
            draw_background(surface)
            snake_obj.move()

            if snake_obj.get_snake_position() == food_obj.positions:
                snake_obj.length += 1
                snake_obj.score_count += 1
                food_obj.get_food_positions()
                bomb_obj.get_bomb_positions()

            if snake_obj.get_snake_position() == bomb_obj.positions:
                main_menu("You lost", red)

            snake_obj.draw(surface)
            food_obj.draw_food(surface)
            bomb_obj.draw_bomb(surface)
            screen.blit(surface, (0, 0))
            text = font1.render("Score: {0}".format(snake_obj.score_count), 1, (0, 0, 0))
            screen.blit(text, (5, 10))
            pygame.display.update()

    def main_menu(word, color):
        menu = True
        selected = "start"
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            snake_obj.reset()
                            main1()

                        if selected == "quit":
                            pygame.quit()
                            quit()

            # Main Menu UI
            screen.fill(color)
            title = text_format(word, font, 90, yellow)
            if selected == "start":
                text_start = text_format("START", font, 75, white)
            else:
                text_start = text_format("START", font, 75, black)
            if selected == "quit":
                text_quit = text_format("QUIT", font, 75, white)
            else:
                text_quit = text_format("QUIT", font, 75, black)

            title_rect = title.get_rect()
            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            # Main Menu Text
            screen.blit(title, (SCREEN_WIDTH / 2 - (title_rect[2] / 2), 80))
            screen.blit(text_start, (SCREEN_WIDTH / 2 - (start_rect[2] / 2), 300))
            screen.blit(text_quit, (SCREEN_WIDTH / 2 - (quit_rect[2] / 2), 360))
            pygame.display.update()
            clock.tick(30)

    main_menu("Snake Attack", blue)


main()
