import pygame as pg
import sys
import random
import os

# Initialise Pygame
pg.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# File directories
MAIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MAIN_DIR, 'data')
ASSETS_DIR = os.path.join(MAIN_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Initialise display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Maze Master")
pg.display.set_icon(pg.image.load(os.path.join(IMAGES_DIR, 'maze_icon.png')))

# Global functions


# Classes
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Maze Master")
        pg.display.set_icon(pg.image.load(os.path.join(IMAGES_DIR, 'maze_icon.png')))
        self.clock = pg.time.Clock()
        self.is_running = True
        self.title_screen = TitleScreen(self)
        self.mouse_pos = pg.mouse.get_pos()

    def run(self):
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.title_screen.play_button.clicked()
            
            self.mouse_pos = pg.mouse.get_pos()

            self.title_screen.draw()

            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.image = pg.image.load(os.path.join(IMAGES_DIR, 'title_screen.png'))
        self.play_button = Button(self.game, SCREEN_WIDTH//2, 430, 'play_button.png', self.play_button_clicked)
    
    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        self.play_button.draw()

    def play_button_clicked(self):
        print("Clicked")

class Button:
    def __init__(self, game, x, y, image, action = None):
        self.game = game
        self.x = x
        self.y = y
        self.image = pg.image.load(os.path.join(IMAGES_DIR, image))
        self.rect = self.image.get_rect(center = (x, y))
        self.action = action

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
    
    def clicked(self):
        if self.rect.collidepoint(new_game.mouse_pos):
            self.action()


    


# Code execution
new_game = Game()
new_game.run()