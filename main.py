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
GREEN = (7, 168, 18)
LIGHT_ORANGE = (255, 204, 153)

# File directories
MAIN_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MAIN_DIR, 'data')
ASSETS_DIR = os.path.join(MAIN_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Fonts
MONTSERRAT_REG = os.path.join(FONTS_DIR, 'Montserrat_Font_Family', 'Montserrat Regular 400.ttf')
MONTSERRAT_BOLD = os.path.join(FONTS_DIR, 'Montserrat_Font_Family', 'Montserrat Bold 700.ttf')
PARKVANE = os.path.join(FONTS_DIR, 'Parkvane_Font_Family', 'Parkvane Regular 400.ttf')

# Global functions
def load_image(filename):
    return pg.image.load(os.path.join(IMAGES_DIR, filename)).convert_alpha()

def draw_text(screen, text, x, y, size = 32, colour = (255, 255, 255), font_type = MONTSERRAT_REG, align = 'topleft'):
    font = pg.font.Font(font_type, size)
    text_surface = font.render(text, True, colour)

    rect = text_surface.get_rect()
    if align == 'center':
        rect.center = (x, y)
    elif align == 'topright':
        rect.topright = (x, y)
    elif align == 'bottomleft':
        rect.bottomleft = (x, y)
    elif align == 'bottomright':
        rect.bottomright = (x, y)
    else:  # default is topleft
        rect.topleft = (x, y)

    screen.blit(text_surface, rect)

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
        self.key_pressed = None # Current key pressed in a frame

    def run(self):
        while self.is_running:
            # Event handler
            self.key_pressed = None
            for event in pg.event.get():
                if event.type == pg.QUIT: # Close window
                    self.is_running = False
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # Mouse left-click
                    self.state.buttons_clicked()
                if event.type == pg.KEYDOWN: # Updates current key pressed
                    self.key_pressed = event.key
            
            # Update mouse coords
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_x = self.mouse_pos[0]
            self.mouse_y = self.mouse_pos[1]

            self.state.draw()

            self.state.update(self)
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

    def update(self, game):
        self.game = game

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

    def update(self, game):
        self.game = game

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
        self.game.endless_game_mode.start_time = pg.time.get_ticks()

class EndlessGameMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('blank.png')
        self.buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked)
        ]
        self.maze_width = 10
        self.maze_height = 10
        self.maze_surface_pos = (353, 101)
        self.maze_surface_width = 575
        self.maze_surface_height = 575
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height)
        self.player = Player(self.game, self.maze)
        self.start_time = pg.time.get_ticks()
        self.elapsed_time = 0
        self.minutes = 0
        self.seconds = 0

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()
        self.maze.draw(self.game.screen)
        self.player.draw()
        self.draw_timer()

    def update(self, game):
        self.game = game
        self.player.update(self.game, self.maze)
        self.update_timer()

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def back_button_clicked(self):
        self.game.state = self.game.play_mode

    def update_timer(self):
        self.elapsed_time = (pg.time.get_ticks() - self.start_time) // 1000 # Elapsed time in seconds
        self.minutes = self.elapsed_time // 60
        self.seconds = self.elapsed_time % 60
    
    def draw_timer(self):
        time = f'{self.minutes:02d}:{self.seconds:02d}'
        draw_text(
            self.game.screen,
            'Timer:',
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            130,
            40,
            LIGHT_ORANGE,
            MONTSERRAT_BOLD,
            'center'
        )
        draw_text(
            self.game.screen,
            time,
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            200,
            40,
            LIGHT_ORANGE,
            MONTSERRAT_REG,
            'center'
        )


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
    def __init__(self, width, height, surface_pos, surface_width, surface_height):
        self.width = width
        self.height = height
        self.stack = []
        self.array = self.create_2D_array(width, height)
        # Determining the appropriate cell size from the ratio of space given to maze size
        self.cell_size = min(surface_width // self.width, surface_height // self.height) # Take the smallest value as the node is a square
        # Determine the coords of where to start drawing from to ensure the maze is aligned at the centre
        self.start_x = surface_pos[0] + (surface_width - self.cell_size * self.width) // 2
        self.start_y = surface_pos[1] + (surface_height - self.cell_size * self.height) // 2
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

    def draw(self, screen, wall_colour=(255,255,255)):
        wall_thickness = max(self.cell_size // 12, 1) # Cell size : Wall thickenss ratio - minimum 1px
        # Draw border
        top_border = pg.Rect(
            self.start_x - wall_thickness,
            self.start_y - wall_thickness,
            self.cell_size * self.width + 2 * wall_thickness,
            wall_thickness
        )
        pg.draw.rect(screen, wall_colour, top_border)
        bottom_border = pg.Rect(
            self.start_x - wall_thickness,
            self.start_y + self.cell_size * self.height,
            self.cell_size * self.width + 2 * wall_thickness,
            wall_thickness
        )
        pg.draw.rect(screen, wall_colour, bottom_border)
        left_border = pg.Rect(
            self.start_x - wall_thickness,
            self.start_y - wall_thickness,
            wall_thickness,
            self.cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, left_border)
        right_border = pg.Rect(
            self.start_x + self.cell_size * self.width,
            self.start_y - wall_thickness,
            wall_thickness,
            self.cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, right_border)
        # Draw cells
        for x in range(self.width):
            for y in range(self.height):
                cell = self.array[x][y]
                x_pos = self.start_x + x * self.cell_size
                y_pos = self.start_y + y * self.cell_size

                if cell.walls['top'] == True:
                    top = pg.Rect(x_pos - wall_thickness, y_pos, self.cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, top)

                if cell.walls['bottom'] == True:
                    bottom = pg.Rect(x_pos - wall_thickness, y_pos + self.cell_size - wall_thickness, self.cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, bottom)

                if cell.walls['left'] == True:
                    left = pg.Rect(x_pos, y_pos - wall_thickness, wall_thickness, self.cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, left)

                if cell.walls['right'] == True:
                    right = pg.Rect(x_pos + self.cell_size - wall_thickness, y_pos - wall_thickness, wall_thickness, self.cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, right)

    def pos_to_px(self, pos):
        return [self.start_x + (pos[0] + 0.5) * self.cell_size, self.start_y + (pos[1] + 0.5) * self.cell_size]

    def px_to_pos(self, px):
        return [(px[0] - self.start_x) / self.cell_size - 0.5, (px[1] - self.start_y) / self.cell_size - 0.5]
    
    def target_node(self, pos, direction):
        x = pos[0]
        y = pos[1]
        match direction:
            case 'north':
                while not self.array[x][y].walls['top']:
                    y -= 1
                    if not self.array[x][y].walls['left'] or not self.array[x][y].walls['right']:
                        return (x, y) # When a junction is reached
                
            case 'east':
                while not self.array[x][y].walls['right']:
                    x += 1
                    if not self.array[x][y].walls['top'] or not self.array[x][y].walls['bottom']:
                        return (x, y) # When a junction is reached
                    
            case 'south':
                while not self.array[x][y].walls['bottom']:
                    y += 1
                    if not self.array[x][y].walls['left'] or not self.array[x][y].walls['right']:
                        return (x, y) # When a junction is reached
                    
            case 'west':
                while not self.array[x][y].walls['left']:
                    x -= 1
                    if not self.array[x][y].walls['top'] or not self.array[x][y].walls['bottom']:
                        return (x, y) # When a junction is reached
        return (x, y) # When a dead end is reached

    
class Player:
    def __init__(self, game, maze):
        self.game = game # Reference to the Game object
        self.maze = maze # Reference to the maze object
        self.x = 0 # Position in the maze array
        self.y = 0 # Position in the maze array
        self.px = self.maze.pos_to_px((self.x, self.y)) # Converts player position to pixel coords
        self.direction = None
        self.queued_direction = None
        self.is_moving = False
        self.target_node_pos = None
        self.target_node_px = None
        self.speed = 5
        self.colour = GREEN
        self.trail_colour = GREEN
        self.trail = [(self.x, self.y)] # Trail path nodes
        self.toggle_trail = True

    def update(self, game, maze): # Updates attributes every frame
        self.game = game
        self.maze = maze
        self.handle_input()
        self.move()

    def handle_input(self):
        if not self.is_moving: # Resets queued direction to none when stationary
            self.queued_direction = None

        if self.game.key_pressed == pg.K_UP: # Up key clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['top'] and not self.is_moving:
                self.direction = 'north'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking()
            elif self.is_moving:
                self.queued_direction = 'north'
        elif self.game.key_pressed == pg.K_DOWN: # Down key clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['bottom'] and not self.is_moving:
                self.direction = 'south'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking()
            elif self.is_moving:
                self.queued_direction = 'south'
        elif self.game.key_pressed == pg.K_LEFT: # Left key clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['left'] and not self.is_moving:
                self.direction = 'west'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking()
            elif self.is_moving:
                self.queued_direction = 'west'
        elif self.game.key_pressed == pg.K_RIGHT: # Right key clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['right'] and not self.is_moving:
                self.direction = 'east'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking()
            elif self.is_moving:
                self.queued_direction = 'east'

    def move(self):
        if self.is_moving:
            if self.direction == 'north':
                if self.px[1] > self.target_node_px[1]:
                    self.px[1] -= self.speed # Move up
                else:
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]
                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    if (self.x, self.y) != self.trail[-1]: # If new node visited
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop() # Remove last item if player is backtracking
                        else:
                            self.trail.append((self.x, self.y)) # Add item if new node visiited

            elif self.direction == 'east':
                if self.px[0] < self.target_node_px[0]:
                    self.px[0] += self.speed # Move right
                else:
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]
                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    if (self.x, self.y) != self.trail[-1]:
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop()
                        else:
                            self.trail.append((self.x, self.y))

            elif self.direction == 'south':
                if self.px[1] < self.target_node_px[1]:
                    self.px[1] += self.speed # Move down
                else:
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]
                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    if (self.x, self.y) != self.trail[-1]:
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop()
                        else:
                            self.trail.append((self.x, self.y))

            elif self.direction == 'west':
                if self.px[0] > self.target_node_px[0]:
                    self.px[0] -= self.speed # Move left
                else:
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]
                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    if (self.x, self.y) != self.trail[-1]:
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop()
                        else:
                            self.trail.append((self.x, self.y))

        if self.queued_direction and not self.is_moving: # Checks for any queued direction
            self.direction = self.queued_direction
            self.queued_direction = None
            self.is_moving = True
            self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
            self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
            self.handle_backtracking()

    def draw_trail(self):
        trail_thickness = max(self.maze.cell_size // 3, 1)
        for i in range(len(self.trail) - 1): # Draws the static part of the trail
            start_pos = self.trail[i]
            end_pos = self.trail[i + 1]
            start_px = self.maze.pos_to_px(start_pos)
            end_px = self.maze.pos_to_px(end_pos)

            static_rect = self.create_rect(start_px, end_px, trail_thickness)
            pg.draw.rect(self.game.screen, self.trail_colour, static_rect)

        last_px = self.maze.pos_to_px(self.trail[-1]) # Draws the dynamic part of the trail
        dynamic_rect = self.create_rect(last_px, self.px, trail_thickness)
        pg.draw.rect(self.game.screen, self.trail_colour, dynamic_rect)

    def create_rect(self, start_px, end_px, thickness):
        if start_px[0] == end_px[0]: # Draw a vertical rectangle
            length = abs(start_px[1] - end_px[1]) + thickness
            x = start_px[0] - thickness // 2
            y = min(start_px[1], end_px[1]) - thickness // 2
            return pg.Rect(x, y, thickness, length)


        elif start_px[1] == end_px[1]: # Draw a horizontal rectangle
            length = abs(start_px[0] - end_px[0]) + thickness
            x = min(start_px[0], end_px[0]) - thickness // 2
            y = start_px[1] - thickness // 2
            return pg.Rect(x, y, length, thickness)

    def handle_backtracking(self):
        if len(self.trail) > 1 and self.target_node_pos == self.trail[-2]:
            self.trail.pop()

    def draw(self): # Draws player as a circle
        self.draw_trail()
        pg.draw.circle(self.game.screen, self.colour, (int(self.px[0]), int(self.px[1])), self.maze.cell_size // 2.5)

        


            


        


    



        

    



# Code execution
new_game = Game()
new_game.run()