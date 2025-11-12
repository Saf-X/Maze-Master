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

# Global functions
def load_image(filename):
    return pg.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()

# Classes
class Game:
    def __init__(self):
        # Initialise screen display
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Maze Master')
        pg.display.set_icon(load_image('maze_icon.png'))

        self.clock = pg.time.Clock()
        self.is_running = True
        self.state = 'TITLESCREEN'
        self.title_screen = TitleScreen(self)
        self.play_mode = PlayMode(self)
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_x = self.mouse_pos[0]
        self.mouse_y = self.mouse_pos[1]

    def run(self):
        while self.is_running:
            # Event handler
            for event in pg.event.get():
                if event.type == pg.QUIT: # Close window
                    self.is_running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # Mouse left-click
                    if self.state == 'TITLESCREEN':
                        self.title_screen.buttons_clicked()
                    elif self.state == 'PLAYMODE':
                        self.play_mode.buttons_clicked()
            
            # Update mouse coords
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_x = self.mouse_pos[0]
            self.mouse_y = self.mouse_pos[1]

            if self.state == 'TITLESCREEN':
                self.title_screen.draw()
            elif self.state == 'PLAYMODE':
                self.play_mode.draw()

            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.image = load_image('title_screen.png')
        self.play_button = Button(self.game, SCREEN_WIDTH//2, 430, 'play_button.png', self.play_button_clicked)
        self.education_button = Button(self.game, 1146, 668, 'education_button.png', self.education_button_clicked)

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        self.play_button.draw()
        self.education_button.draw()

    def buttons_clicked(self):
        self.play_button.clicked()
        self.education_button.clicked()

    def play_button_clicked(self):
        self.game.state = 'PLAYMODE'

    def education_button_clicked(self):
        print('Education button clicked.')

class PlayMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('play_mode.png')
        self.back_button = Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked)
        self.settings_button = Button(self.game, 1230, 670, 'settings_button.png', self.settings_button_clicked)
        self.levels_button = Button(self.game, SCREEN_WIDTH//2, 426, 'levels_button.png', self.levels_button_clicked)
        self.endless_button = Button(self.game, SCREEN_WIDTH//2, 564, 'endless_button.png', self.endless_button_clicked)

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        self.back_button.draw()
        self.settings_button.draw()
        self.levels_button.draw()
        self.endless_button.draw()

    def buttons_clicked(self):
        self.back_button.clicked()
        self.settings_button.clicked()
        self.levels_button.clicked()
        self.endless_button.clicked()

    def back_button_clicked(self):
        self.game.state = 'TITLESCREEN'

    def settings_button_clicked(self):
        print('Settings button clicked.')

    def levels_button_clicked(self):
        print('Levels button clicked.')

    def endless_button_clicked(self):
        print('Endless button clicked.')    

class Button:
    def __init__(self, game, x, y, image, action = None):
        self.game = game
        self.x = x
        self.y = y
        self.image = load_image(image)
        self.mask = pg.mask.from_surface(self.image) # Creates mask of button
        self.rect = self.image.get_rect(center = (x, y))
        self.action = action

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
    
    def clicked(self):
        if self.rect.collidepoint(self.game.mouse_pos): # First checks if button rectangle is clicked
            pixel_x = self.game.mouse_x - self.rect.left # Relative x-coord of image pixel clicked
            pixel_y = self.game.mouse_y - self.rect.top # Relative y-coord of image pixel clicked
            if self.mask.get_at((pixel_x, pixel_y)): # Checks if pixel clicked is not transparent
                self.action()

# Code execution
new_game = Game()
new_game.run()