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
        self.title_screen = TitleScreen(self)
        self.play_mode = PlayMode(self)
        self.endless_game_mode = EndlessGameMode(self)
        self.state = self.title_screen
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
                    self.state.buttons_clicked()
            
            # Update mouse coords
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_x = self.mouse_pos[0]
            self.mouse_y = self.mouse_pos[1]

            self.state.draw()

            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.image = load_image('title_screen.png')
        self.buttons = [
            Button(self.game, SCREEN_WIDTH//2, 430, 'play_button.png', self.play_button_clicked),
            Button(self.game, 1146, 668, 'education_button.png', self.education_button_clicked)
        ]
    
    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def play_button_clicked(self):
        self.game.state = self.game.play_mode

    def education_button_clicked(self):
        print('Education button clicked.')

class PlayMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('play_mode.png')
        self.buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked),
            Button(self.game, 1230, 670, 'settings_button.png', self.settings_button_clicked),
            Button(self.game, SCREEN_WIDTH//2, 426, 'levels_button.png', self.levels_button_clicked),
            Button(self.game, SCREEN_WIDTH//2, 564, 'endless_button.png', self.endless_button_clicked)
        ]
    
    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def back_button_clicked(self):
        self.game.state = self.game.title_screen

    def settings_button_clicked(self):
        print('Settings button clicked.')

    def levels_button_clicked(self):
        print('Levels button clicked.')

    def endless_button_clicked(self):
        self.game.state = self.game.endless_game_mode

class EndlessGameMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('blank.png')
        self.buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked)
        ]
        self.maze = Maze(8, 8)

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()
        self.maze.draw(self.game.screen, (353, 101), 575, 575)

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def back_button_clicked(self):
        self.game.state = self.game.play_mode

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

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_visited = False
        self.walls = {'top':True, 'bottom':True, 'left':True, 'right':True}
        self.distance = float('inf') # Set to infinity
        self.previous_node = None
        self.heuristic = 0

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stack = []
        self.array = self.create_2D_array(width, height)
        self.generate()

    def create_2D_array(self, width, height):
        array = []
        for x in range(width):
            array.append([])
            for y in range(height):
                array[x].append(Node(x, y))
        return array
    
    def get_neighbours(self, node):
        neighbours = []

        if node.y > 0: # Top
            if self.array[node.x][node.y - 1].is_visited == False:
                neighbours.append(self.array[node.x][node.y - 1])
        
        if node.y < self.height - 1: # Bottom
            if self.array[node.x][node.y + 1].is_visited == False:
                neighbours.append(self.array[node.x][node.y + 1])

        if node.x > 0: # Left
            if self.array[node.x - 1][node.y].is_visited == False:
                neighbours.append(self.array[node.x - 1][node.y])   

        if node.x < self.width - 1: # Right
            if self.array[node.x + 1][node.y].is_visited == False:
                neighbours.append(self.array[node.x + 1][node.y])

        return neighbours
    
    def remove_walls(self, node1, node2):
        if node1.x == node2.x and node1.y == node2.y + 1: # Top of node1
            node1.walls['top'] = False
            node2.walls['bottom'] = False
        elif node1.x == node2.x and node1.y == node2.y - 1: # Bottom of node1
            node1.walls['bottom'] = False
            node2.walls['top'] = False
        elif node1.x == node2.x + 1 and node1.y == node2.y: # Left of node1
            node1.walls['left'] = False
            node2.walls['right'] = False
        elif node1.x == node2.x - 1 and node1.y == node2.y: # Right of node1
            node1.walls['right'] = False
            node2.walls['left'] = False
        
    def generate(self):
        start_node = self.array[0][0]
        start_node.is_visited = True
        self.stack.append(start_node)

        while len(self.stack) > 0:
            current_node = self.stack[-1]
            neighbouring_nodes = self.get_neighbours(current_node)

            if len(neighbouring_nodes) > 0:
                next_node = random.choice(neighbouring_nodes)
                self.remove_walls(current_node, next_node)
                next_node.is_visited = True
                self.stack.append(next_node)
            else:
                self.stack.pop()

    def draw(self, screen, surface_pos, surface_width, surface_height, wall_colour=(255,255,255)):
        # Determining the appropriate cell size from the ratio of space given to maze size
        cell_size = min(surface_width // self.width, surface_height // self.height) # Take the smallest value as the node is a square
        surface_x = surface_pos[0]
        surface_y = surface_pos[1]
        # Determine the coords of where to start drawing from to ensure the maze is aligned at the centre
        start_x = surface_x + (surface_width - cell_size * self.width) // 2
        start_y = surface_y + (surface_height - cell_size * self.height) // 2
        wall_thickness = cell_size // 8 # Cell size : Wall thickenss ratio
        # Draw border
        top_border = pg.Rect(
            start_x - wall_thickness,
            start_y - wall_thickness,
            cell_size * self.width + 2 * wall_thickness,
            wall_thickness
        )
        pg.draw.rect(screen, wall_colour, top_border)
        bottom_border = pg.Rect(
            start_x - wall_thickness,
            start_y + cell_size * self.height,
            cell_size * self.width + 2 * wall_thickness,
            wall_thickness
        )
        pg.draw.rect(screen, wall_colour, bottom_border)
        left_border = pg.Rect(
            start_x - wall_thickness,
            start_y - wall_thickness,
            wall_thickness,
            cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, left_border)
        right_border = pg.Rect(
            start_x + cell_size * self.width,
            start_y - wall_thickness,
            wall_thickness,
            cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, right_border)
        # Draw cells
        for x in range(self.width):
            for y in range(self.height):
                cell = self.array[x][y]
                x_pos = start_x + x * cell_size
                y_pos = start_y + y * cell_size

                if cell.walls['top'] == True:
                    top = pg.Rect(x_pos - wall_thickness, y_pos, cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, top)

                if cell.walls['bottom'] == True:
                    bottom = pg.Rect(x_pos - wall_thickness, y_pos + cell_size - wall_thickness, cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, bottom)

                if cell.walls['left'] == True:
                    left = pg.Rect(x_pos, y_pos - wall_thickness, wall_thickness, cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, left)

                if cell.walls['right'] == True:
                    right = pg.Rect(x_pos + cell_size - wall_thickness, y_pos - wall_thickness, wall_thickness, cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, right)


    



        

    



# Code execution
new_game = Game()
new_game.run()