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
CYAN = (102, 255, 255)

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

def draw_text(screen, text, x, y, font, colour = (255, 255, 255), align = 'topleft'):
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
        self.start_node_pos = (0, 0)
        self.maze_width = 25
        self.maze_height = 25
        self.maze_surface_pos = (353, 101)
        self.maze_surface_width = 575
        self.maze_surface_height = 575
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height)
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1])
        self.start_time = pg.time.get_ticks()
        self.elapsed_time = 0 # Seconds since level started
        self.minutes = 0 # Clock display
        self.seconds = 0 # Clock display
        self.win = False
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        self.goal_node_image = pg.transform.smoothscale(load_image('goal_node.png'), (self.maze.cell_size, self.maze.cell_size))
        self.goal_node_rect = self.goal_node_image.get_rect()
        self.timer_label_font = pg.font.Font(MONTSERRAT_BOLD, 40)
        self.timer_text_font = pg.font.Font(MONTSERRAT_REG, 40)
        self.moves_counter_label_font = pg.font.Font(MONTSERRAT_BOLD, 40)
        self.moves_counter_text_font = pg.font.Font(MONTSERRAT_REG, 40)
        self.path = self.maze.run_dijkstra(self.start_node_pos, self.goal_node_pos)
        self.zero_star_image = pg.transform.smoothscale(load_image('0 star.png'), (153, 51))
        self.zero_star_rect = self.zero_star_image.get_rect()
        self.one_star_image = pg.transform.smoothscale(load_image('1 star.png'), (153, 51))
        self.one_star_rect = self.zero_star_image.get_rect()
        self.two_star_image = pg.transform.smoothscale(load_image('2 star.png'), (153, 51))
        self.two_star_rect = self.zero_star_image.get_rect()
        self.three_star_image = pg.transform.smoothscale(load_image('3 star.png'), (153, 51))
        self.three_star_rect = self.zero_star_image.get_rect()
        self.star_rating = 3
        self.speed_constant = 6.02 # Solving speed to acheive 3/3 stars

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()
        self.maze.draw(self.game.screen)
        self.draw_goal_node()
        self.player.draw()
        self.draw_timer()
        self.draw_moves_counter()
        self.draw_star_rating()

    def update(self, game):
        self.game = game
        self.player.update(self.game, self.maze)
        self.update_star_rating()
        if not self.win:
            self.update_timer()
        self.is_winning()

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
        time = f'{self.minutes:02d}:{self.seconds:02d}' # Clock display MM:SS
        draw_text(
            self.game.screen,
            'Timer:',
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            130,
            self.timer_label_font,
            LIGHT_ORANGE,
            'center'
        )
        draw_text(
            self.game.screen,
            time,
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            200,
            self.timer_text_font,
            LIGHT_ORANGE,
            'center'
        )

    def draw_moves_counter(self):
        moves = str(self.player.moves) # Obtain the no. moves made from Player class
        draw_text(
            self.game.screen,
            'Moves:',
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            340,
            self.moves_counter_label_font,
            CYAN,
            'center'
        )
        draw_text(
            self.game.screen,
            moves,
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            410,
            self.moves_counter_text_font,
            CYAN,
            'center'
        )

    def is_winning(self):
        if (self.player.x, self.player.y) == self.goal_node_pos:
            self.win = True

    def draw_goal_node(self):
        self.goal_node_rect.center = self.maze.pos_to_px(self.goal_node_pos)
        self.game.screen.blit(self.goal_node_image, self.goal_node_rect)

    def update_star_rating(self):
        three_star_time = len(self.path) / self.speed_constant # Max time to achieve 3/3 stars
        if self.elapsed_time <= three_star_time:
            self.star_rating = 3
        elif self.elapsed_time <= three_star_time + 5:
            self.star_rating = 2
        else:
            self.star_rating = 1
    
    def draw_star_rating(self):
        match self.star_rating:
            case 3:
                self.three_star_rect.topleft = (775, 45)
                self.game.screen.blit(self.three_star_image, self.three_star_rect)
            case 2:
                self.two_star_rect.topleft = (775, 45)
                self.game.screen.blit(self.two_star_image, self.two_star_rect)
            case 1:
                self.one_star_rect.topleft = (775, 45)
                self.game.screen.blit(self.one_star_image, self.one_star_rect)

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
        self.is_visited = False # Visited flag for maze generation
        self.is_path_visited = False # Visited flag for pathfinding
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
    
    def get_unvisited_neighbours(self, node): # Returns a list of univisited neighbouring nodes for maze generation
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
            neighbouring_nodes = self.get_unvisited_neighbours(current_node)

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
    
    def get_reachable_neighbours(self, node): # Returns a list of adjacent nodes with no wall in between
        neighbours = []

        if not node.walls['top']:
            neighbours.append(self.array[node.x][node.y - 1])
        if not node.walls['bottom']:
            neighbours.append(self.array[node.x][node.y + 1])
        if not node.walls['left']:
            neighbours.append(self.array[node.x - 1][node.y])
        if not node.walls['right']:
            neighbours.append(self.array[node.x + 1][node.y])
        return neighbours
    
    def run_dijkstra(self, start_node_pos, goal_node_pos):
        start_node = self.array[start_node_pos[0]][start_node_pos[1]]
        goal_node = self.array[goal_node_pos[0]][goal_node_pos[1]]
        return Dijkstra(self).run(start_node, goal_node)


    
class Player:
    def __init__(self, game, maze, x = 0, y = 0):
        self.game = game # Reference to the Game object
        self.maze = maze # Reference to the maze object
        self.x = x # Position in the maze array
        self.y = y # Position in the maze array
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
        self.moves = 0 

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
                    self.moves += 1
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
                    self.moves += 1
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
                    self.moves += 1
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
                    self.moves += 1
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

class Dijkstra:
    def __init__(self, maze):
        self.maze = maze

    def reset_nodes(self): # Resets all nodes' pathfinding attributes
        for column in self.maze.array:
            for node in column:
                node.is_path_visited = False
                node.distance = float('inf') # Set to infinity
                node.previous_node = None
                node.heuristic = 0

    def retrace(self, goal_node): # Outputs the path of nodes from goal node to start node
        current_node = goal_node
        path = [goal_node]
        while current_node.previous_node:
            current_node = current_node.previous_node
            path.append(current_node)
        return path

    def run(self, start_node, goal_node):
        self.reset_nodes()
        start_node.distance = 0
        open_set = []
        open_set.append(start_node)

        while open_set:
            closest_node = open_set[0]
            index = 0
            for i in range(len(open_set)): # Finds the closest node in the open set
                if open_set[i].distance < closest_node.distance:
                    closest_node = open_set[i]
                    index = i
            
            current_node = open_set.pop(index)
            current_node.is_path_visited = True

            if current_node == goal_node:
                return self.retrace(goal_node)
            
            neighbouring_nodes = self.maze.get_reachable_neighbours(current_node)
            for i in range(len(neighbouring_nodes)): # Find an unvisited neighbouring node
                if not neighbouring_nodes[i].is_path_visited:
                    new_distance = current_node.distance + 1 # Distance from start increases by 1 each square
                    if new_distance < neighbouring_nodes[i].distance: # Updates the nodes' distance from start
                        neighbouring_nodes[i].distance = new_distance
                        neighbouring_nodes[i].previous_node = current_node
                        open_set.append(neighbouring_nodes[i])
            




            


        


    



        

    



# Code execution
new_game = Game()
new_game.run()