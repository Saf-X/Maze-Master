import pygame as pg
import sys
import random
import os
import json

# Initialise Pygame
pg.init()
pg.mixer.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (7, 168, 18)
DARK_GREEN = (0, 100, 0)
SPRING_GREEN = (71, 212, 90)
ORANGE = (255, 192, 0)
LIGHT_ORANGE = (255, 204, 153)
RED = (192, 0, 0)
CYAN = (102, 255, 255)
PINK = (255, 0, 255)
GOLD = (255, 215, 0)

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

def draw_text(screen, text, x, y, font, colour = WHITE, align = 'topleft'):
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
        # Sound initialisation
        with open(os.path.join(DATA_DIR, 'settings.json'), 'r') as f:
            settings_info = json.load(f)
        self.mute_sfx = settings_info['mute_sfx']
        self.sfx_volume = settings_info['sfx_volume']
        self.mute_music = settings_info['mute_music']
        self.music_volume = settings_info['music_volume']
        self.click_sound = pg.mixer.Sound(os.path.join(SOUNDS_DIR, 'button_click.wav'))
        self.star_sound = pg.mixer.Sound(os.path.join(SOUNDS_DIR, 'ding.wav'))
        if self.mute_music:
            pg.mixer.music.set_volume(0)
        else:
            pg.mixer.music.set_volume(self.music_volume)
        # Instantiate the different game states
        self.title_screen = TitleScreen(self)
        self.education_mode = EducationMode(self)
        self.play_mode = PlayMode(self)
        self.levels_game_mode = LevelsGameMode(self)
        self.endless_game_mode = EndlessGameMode(self)
        self.pause_menu = PauseMenu(self)
        self.endless_win_screen = EndlessWinScreen(self)
        self.levels_win_screen = LevelsWinScreen(self)
        self.settings = Settings(self)
        self.is_paused = False
        self.win = False
        self.show_settings = False
        self.state = self.title_screen
        # Mouse info
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
                    if self.show_settings: # Processes buttons clicked of states in order of priority
                        self.settings.buttons_clicked()
                    elif self.is_paused:
                        self.pause_menu.buttons_clicked()
                    elif self.win:
                        if self.state == self.endless_game_mode:
                            self.endless_win_screen.buttons_clicked() 
                        elif self.state == self.levels_game_mode:
                            self.levels_win_screen.buttons_clicked()
                    else:
                        self.state.buttons_clicked()
                if event.type == pg.KEYDOWN: # Updates current key pressed
                    self.key_pressed = event.key
            
            # Update mouse coords
            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_x = self.mouse_pos[0]
            self.mouse_y = self.mouse_pos[1]

            self.state.draw()
            
            if self.show_settings: # Draws/updates states in order of priority
                self.settings.draw()
                self.settings.update()
            elif self.is_paused:
                self.pause_menu.draw()
            elif self.win:
                if self.state == self.endless_game_mode:
                    self.endless_win_screen.update()
                    self.endless_win_screen.draw()   
                elif self.state == self.levels_game_mode:
                    self.levels_win_screen.update()
                    self.levels_win_screen.draw()                                        
            else:
                self.state.update()

            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit() # Safely exits the game

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.image = load_image('title_screen.png')
        self.buttons = [
            Button(self.game, SCREEN_WIDTH // 2, 430, 'play_button1.png', self.play_button_clicked),
            Button(self.game, 1146, 668, 'education_button.png', self.education_button_clicked)
        ]
        pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
        pg.mixer.music.play(-1)
    
    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons:
            button.draw()

    def update(self): # The existance of this function is necessary, as it acts as a placeholder for the logic in the Game class
        pass

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def play_button_clicked(self):
        self.game.state = self.game.play_mode

    def education_button_clicked(self):
        self.game.state = self.game.education_mode
        pg.mixer.music.stop()

class PlayMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('play_mode.png')
        self.buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked, 81, 72),
            Button(self.game, 1230, 670, 'settings_button.png', self.settings_button_clicked, 72, 72),
            Button(self.game, SCREEN_WIDTH // 2, 426, ['levels_button.png', 'dark_levels_button.png'], self.levels_button_clicked),
            Button(self.game, SCREEN_WIDTH // 2, 564, ['endless_button.png', 'dark_endless_button.png'], self.endless_button_clicked),
            Button(self.game, 43, 55, ['light_on.png', 'light_off.png'], self.darkness_mode_button_clicked, 55, 110)
        ]
        self.UI_text_font = pg.font.Font(MONTSERRAT_REG, 43)
        self.darkness_mode = False
        self.black_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.black_surface.fill(BLACK)
    
    def draw(self):
        self.game.screen.blit(self.image, (0, 0))
        for button in self.buttons:
            button.draw(int(self.darkness_mode))
        self.draw_UI_elements()

    def update(self): # The existance of this function is necessary, as it acts as a placeholder for the logic in the Game class
        pass

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def back_button_clicked(self):
        self.game.state = self.game.title_screen

    def settings_button_clicked(self):
        self.game.show_settings = True

    def levels_button_clicked(self):
        self.game.state = self.game.levels_game_mode

    def endless_button_clicked(self):
        self.game.state = self.game.endless_game_mode
        self.game.endless_game_mode.reset()
        if self.darkness_mode: # Chooses which soundtrack to play
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_gameplay_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_gameplay_music.mp3'))
            pg.mixer.music.play(-1)
    
    def darkness_mode_button_clicked(self):
        self.darkness_mode = not self.darkness_mode # Toggles darkness mode on/off
        if self.darkness_mode: # Choose which theme to draw and which soundtrack to play
            self.image = load_image('dark_play_mode.png')
            self.game.levels_game_mode.image = self.black_surface
            self.game.endless_game_mode.image = self.black_surface
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_bg_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            self.image = load_image('play_mode.png')
            self.game.levels_game_mode.image = load_image('blank.png')
            self.game.endless_game_mode.image = load_image('blank.png')
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
            pg.mixer.music.play(-1)

    def draw_UI_elements(self):
        draw_text( # Levels button text - shows no. levels completed out of 45
            self.game.screen,
            f'{self.game.levels_game_mode.get_levels_completed()} / 45',
            SCREEN_WIDTH // 2,
            426,
            self.UI_text_font,
            WHITE,
            'center'
        )
        shortest_time = self.game.endless_game_mode.get_shortest_time()
        minutes = shortest_time // 60
        seconds = shortest_time % 60
        time = f'{minutes:01d} : {seconds:02d}' # Clock display MM : SS
        if shortest_time >= 999999999: # Shows a blank time if a shortest time hasn't been set
            time = '-- : --'
        draw_text( # Endless button text - shows the shortest time taken to solve an endless maze
            self.game.screen,
            time,
            SCREEN_WIDTH // 2,
            564,
            self.UI_text_font,
            WHITE,
            'center'
        )

class GameMode: # Parent Class
    def __init__(self, game):
        self.game = game
        self.image = load_image('blank.png')
        self.buttons = [
            Button(self.game, 50, 50, 'pause_button.png', self.pause_button_clicked, 72, 72)
        ]
        self.start_node_pos = (0, 0)
        # Maze dimensions
        self.maze_width = None
        self.maze_height = None
        # Where to draw the maze
        self.maze_surface_pos = (353, 101)
        self.maze_surface_width = 575
        self.maze_surface_height = 575

        self.maze = None
        self.player = None
        self.start_time = pg.time.get_ticks() # Timer value when started
        self.elapsed_time = 0 # Seconds since level started
        self.start_pause_time = 0 # Timer value when paused
        self.elapsed_pause_time = 0 # Pause duration
        self.minutes = 0 # Clock display
        self.seconds = 0 # Clock display
        self.goal_node_pos = None
        self.goal_node_image = None
        self.goal_node_rect = None
        self.UI_label_font = pg.font.Font(MONTSERRAT_BOLD, 40)
        self.UI_text_font = pg.font.Font(MONTSERRAT_REG, 40)
        self.title = None
        self.title_colour = None
        self.title_text_font = pg.font.Font(PARKVANE, 50)
        self.path = None # List of nodes that form the shortest path maze solution
        self.zero_star_image = pg.transform.smoothscale(load_image('0 star.png'), (153, 51))
        self.zero_star_rect = self.zero_star_image.get_rect()
        self.one_star_image = pg.transform.smoothscale(load_image('1 star.png'), (153, 51))
        self.one_star_rect = self.one_star_image.get_rect()
        self.two_star_image = pg.transform.smoothscale(load_image('2 star.png'), (153, 51))
        self.two_star_rect = self.two_star_image.get_rect()
        self.three_star_image = pg.transform.smoothscale(load_image('3 star.png'), (153, 51))
        self.three_star_rect = self.three_star_image.get_rect()
        self.star_rating = 3
        self.speed_constant = 6.02 # Solving speed required to achieve 3/3 stars - increasing it will make achieving 3/3 stars more difficult

    def get_mode(self):
        if self.game.play_mode.darkness_mode:
            return 'darkness'
        else:
            return 'normal'      

    def pause_button_clicked(self):
        self.game.is_paused = True
        self.start_pause_time = pg.time.get_ticks()
        pg.mixer.music.pause()

    def draw_title(self):
        draw_text(
            self.game.screen,
            self.title,
            self.maze_surface_pos[0],
            45,
            self.title_text_font,
            self.title_colour,
            'topleft'
        )

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
            self.UI_label_font,
            LIGHT_ORANGE,
            'center'
        )
        draw_text(
            self.game.screen,
            time,
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            200,
            self.UI_text_font,
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
            self.UI_label_font,
            CYAN,
            'center'
        )
        draw_text(
            self.game.screen,
            moves,
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            410,
            self.UI_text_font,
            CYAN,
            'center'
        )

    def is_winning(self): # Win condition
        if (self.player.x, self.player.y) == self.goal_node_pos:
            if not self.game.win:
                pg.mixer.music.stop()
            self.game.win = True
            if self.game.state == self.game.endless_game_mode:
                self.game.endless_win_screen.next_animation_time = pg.time.get_ticks() # Passes timer value to WinScreen when game won
            elif self.game.state == self.game.levels_game_mode:
                self.game.levels_win_screen.next_animation_time = pg.time.get_ticks() # Passes timer value to WinScreen when game won

    def draw_goal_node(self):
        self.goal_node_rect.center = self.maze.pos_to_px(self.goal_node_pos)
        self.game.screen.blit(self.goal_node_image, self.goal_node_rect)

    def update_star_rating(self): # Calculates the time brackets for achieving 1, 2 or 3 stars
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

    def draw_darkness_mode_overlay(self): # Limits the players vision
        self.darkness_mode_overlay = pg.Surface((self.maze_surface_width, self.maze_surface_height), pg.SRCALPHA)
        self.darkness_mode_overlay.fill((0, 0, 0, 255))
        pixel_x = int(self.player.px[0] - self.maze.start_x) # Relative x-coord of darkness overlay surface
        pixel_y = int(self.player.px[1] - self.maze.start_y) # Relative y-coord of darkness overlay surface
        radius = int(self.maze.cell_size * 2.5) # Give a 5 cell thick diameter
        pg.draw.circle(self.darkness_mode_overlay, (0, 0, 0, 0), (pixel_x, pixel_y), radius) # Draws transparent circle as a hole
        self.game.screen.blit(self.darkness_mode_overlay, self.maze_surface_pos)
        self.maze.draw_border(self.game.screen) 
        
class EndlessGameMode(GameMode):
    def __init__(self, game):
        super().__init__(game)
        with open(os.path.join(DATA_DIR, 'stats.json'), 'r') as f: # Loads from JSON
            self.stats = json.load(f) # Stats dictionary
        self.current_streak = 0 # Refers to the no. of consecutive three-star runs currently achieved
        self.maze_width = 20
        self.maze_height = 20
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height) # Generates new maze
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1]) # Instantiates player
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        self.goal_node_image = pg.transform.smoothscale(load_image('goal_node.png'), (self.maze.cell_size, self.maze.cell_size))
        self.goal_node_rect = self.goal_node_image.get_rect()
        self.title = 'Endless'
        self.title_colour = PINK
        self.path = self.maze.run_dijkstra(self.start_node_pos, self.goal_node_pos) # List of nodes that form the shortest path maze solution

    def get_shortest_time(self): # Gets either normal mode or darkness mode's shortest time stat
        return self.stats['shortest_time'][self.get_mode()]

    def get_best_streak(self): # Gets either normal mode or darkness mode's best streak stat
        return self.stats['best_streak'][self.get_mode()]

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        if not self.game.is_paused and not self.game.win:
            for button in self.buttons: # Only activates these buttons if not paused or game is not won
                button.draw()
        self.maze.draw(self.game.screen)
        self.draw_goal_node()
        self.player.draw()
        self.draw_title()
        if self.game.play_mode.darkness_mode:
            self.draw_darkness_mode_overlay()
        if not self.game.win:
            self.draw_timer()
            self.draw_moves_counter()
            self.draw_current_streak()
            self.draw_best_streak()
            self.draw_star_rating()

    def update(self):
        if not self.game.win:
            self.player.update()
            self.update_star_rating()
            self.update_timer()
            self.is_winning()
    
    def reset(self):
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height) # Generates a new maze
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1]) # Instantiates player
        self.start_time = pg.time.get_ticks() # Timer value when started
        self.elapsed_time = 0 # Seconds since level started
        self.start_pause_time = 0 # Timer value when paused
        self.elapsed_pause_time = 0 # Pause duration
        self.minutes = 0 # Clock display
        self.seconds = 0 # Clock display
        self.path = self.maze.run_dijkstra(self.start_node_pos, self.goal_node_pos) # List of nodes that form the shortest path maze solution
        self.star_rating = 3
        self.game.win = False

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def draw_current_streak(self):
        draw_text(
            self.game.screen,
            'Current Streak:',
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            130,
            self.UI_label_font,
            WHITE,
            'center'
        )
        draw_text(
            self.game.screen,
            str(self.current_streak),
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            200,
            self.UI_text_font,
            WHITE,
            'center'
        )

    def draw_best_streak(self):
        draw_text(
            self.game.screen,
            'Best Streak:',
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            340,
            self.UI_label_font,
            GOLD,
            'center'
        )
        draw_text(
            self.game.screen,
            str(self.get_best_streak()),
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            410,
            self.UI_text_font,
            GOLD,
            'center'
        )

class LevelsGameMode(GameMode):
    def __init__(self, game):
        super().__init__(game)
        with open(os.path.join(DATA_DIR, 'levels.json'), 'r') as f: # Loads from JSON
            self.levels = json.load(f) # Levels dictionary
        self.current_level = self.levels[0] # Loads 1st level by default, changed later on
        self.maze_width = len(self.current_level['maze']) # Length of the 1st dimension in the 2D array
        self.maze_height = len(self.current_level['maze'][0]) # Length of the 2nd dimension in the 2D array
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height, self.current_level['maze']) # Loads current level maze layout
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1]) # Instantiates player
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        self.goal_node_image = pg.transform.smoothscale(load_image('goal_node.png'), (self.maze.cell_size, self.maze.cell_size))
        self.goal_node_rect = self.goal_node_image.get_rect()
        self.path = self.maze.run_dijkstra(self.start_node_pos, self.goal_node_pos) # List of nodes that form the shortest path maze solution
        self.star_rating = 3
        self.page = 1 # Loads the first page, which is the easy levels page
        self.page_image = [ # Images of the three dots which indicate what page the user is on
            pg.transform.smoothscale(load_image('page1.png'), (60, 14)),
            pg.transform.smoothscale(load_image('page2.png'), (60, 14)),
            pg.transform.smoothscale(load_image('page3.png'), (60, 14))
        ]
        self.star_image = pg.transform.smoothscale(load_image('yellow_star.png'), (30, 30))
        self.select_title_text_font = pg.font.Font(PARKVANE, 80)
        self.level_number_font = pg.font.Font(MONTSERRAT_BOLD, 64)
        self.stars_collected_font = pg.font.Font(MONTSERRAT_REG, 24)
        self.state = 'select' # This mode has two states: Select (choose level) & Play (play level)
        self.select_buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked, 81, 72),
            Button(self.game, 1230, 670, 'settings_button.png', self.settings_button_clicked, 72, 72),
            Button(self.game, 140, 400, 'previous_button.png', self.previous_button_clicked, 182, 182),
            Button(self.game, 1140, 400, 'next_button.png', self.next_button_clicked, 182, 182)
        ]
        self.levels_icons = []
        levels_icon_start_x = 263
        levels_icon_start_y = 211
        levels_icon_spacing = (SCREEN_WIDTH - 2 * levels_icon_start_x) // 4
        for i in range(45): # Instantates all of the levels icons 1-45
            # Calculates icon position
            column = i % 5
            row = i // 5 % 3
            x = levels_icon_start_x + column * levels_icon_spacing
            y = levels_icon_start_y + row * levels_icon_spacing
            # Choose icon image color
            if i // 15 == 0:
                image = 'easy_icon.png'
            elif i // 15 == 1:
                image = 'medium_icon.png'
            else:
                image = 'hard_icon.png'

            self.levels_icons.append(Button(self.game, x, y, [image, 'dark_icon.png'], self.play_level, 182, 182, i + 1))
        self.play_buttons = self.buttons # Taken from parent class and also used for endless game mode

    def get_levels_completed(self): # Counts the no. levels completed (levels that have >= 1 star rating achieved)
        levels_completed = 0
        for level in self.levels:
            if level['stars'][self.get_mode()] > 0:
                levels_completed += 1
        return levels_completed
    
    def get_stars_collected(self): # Counts the number of stars collected in total from all levels
        stars_collected = 0
        for level in self.levels:
            stars_collected += level['stars'][self.get_mode()]
        return stars_collected

    def draw(self):
        self.game.screen.blit(self.image, (0, 0))
        match self.page: # Chooses which title to draw for the Levels Selector
                case 1:
                    self.difficulty = 'Easy'
                    self.title_colour = SPRING_GREEN
                case 2:
                    self.difficulty = 'Medium'
                    self.title_colour = ORANGE
                case 3:
                    self.difficulty = 'Hard'
                    self.title_colour = RED
        if self.state == 'select':
            draw_text( # Draws the Levels Selector Title
                self.game.screen,
                self.difficulty,
                SCREEN_WIDTH // 2,
                67,
                self.select_title_text_font,
                self.title_colour,
                'center'
            )    
            for button in self.select_buttons[:2]: # Draws all of the static buttons
                button.draw()
            self.game.screen.blit(self.page_image[self.page - 1], (610, 686)) # Draws the correct three dots image pased on current page number
            match self.page: # Draws easy/medium/hard levels icons
                case 1:
                    self.select_buttons[3].draw() # Draws the next button to allow user to go to the next page of levels
                    for icon in self.levels_icons[:15]: # Draws levels icons 1-15 which are the easy levels
                        icon.draw(int(self.game.play_mode.darkness_mode)) # Draws icon in a dark colour is darkness mode is on
                case 2:
                    self.select_buttons[2].draw() # Draws the previous button to allow user to go to the previous page of levels
                    self.select_buttons[3].draw() # Draws the next button to allow user to go to the next page of levels
                    for icon in self.levels_icons[15:30]: # Draws levels icons 16-30 which are the medium levels
                        icon.draw(int(self.game.play_mode.darkness_mode)) # Draws icon in a dark colour is darkness mode is on
                case 3:
                    self.select_buttons[2].draw() # Draws the previous button to allow user to go to the previous page of levels
                    for icon in self.levels_icons[30:]: # Draws levels icons 31-45 which are the hard levels
                        icon.draw(int(self.game.play_mode.darkness_mode)) # Draws icon in a dark colour is darkness mode is on
            self.draw_icon_info() # Draws no. stars achieved and level number for each level icon
            self.draw_stars_collected() # Draws total no. stars collected from every level
        if self.state == 'play':
            if not self.game.is_paused and not self.game.win:
                for button in self.play_buttons: # Only activates these buttons if not paused or game is not won
                    button.draw()
            self.maze.draw(self.game.screen)
            self.draw_goal_node()
            self.player.draw()
            self.title = f'Level {self.current_level["number"]}'
            self.draw_title()
            if self.game.play_mode.darkness_mode:
                self.draw_darkness_mode_overlay()
            self.draw_instructions()
            if not self.game.win:
                self.draw_timer()
                self.draw_moves_counter()
                self.draw_star_rating()

    def update(self):
        if not self.game.win and self.state == 'play':
            self.player.update()
            self.update_star_rating()
            self.update_timer()
            self.is_winning()
    
    def reset(self):
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1])
        self.start_time = pg.time.get_ticks() # Timer value when started
        self.elapsed_time = 0 # Seconds since level started
        self.start_pause_time = 0 # Timer value when paused
        self.elapsed_pause_time = 0 # Pause duration
        self.minutes = 0 # Clock display
        self.seconds = 0 # Clock display
        self.star_rating = 3
        self.game.win = False

    
    def buttons_clicked(self): # Chooses which buttons to activate based on current state and page no.
        if self.state == 'select':
            for button in self.select_buttons[:2]:
                button.clicked()
            match self.page:
                case 1:
                    self.select_buttons[3].clicked()
                    for icon in self.levels_icons[:15]:
                        icon.clicked()
                case 2:
                    self.select_buttons[2].clicked()
                    self.select_buttons[3].clicked()
                    for icon in self.levels_icons[15:30]:
                        icon.clicked()
                case 3:
                    self.select_buttons[2].clicked()
                    for icon in self.levels_icons[30:]:
                        icon.clicked()
        elif self.state == 'play':
            for button in self.play_buttons:
                button.clicked()

    def back_button_clicked(self):
        self.game.state = self.game.play_mode

    def settings_button_clicked(self):
        self.game.show_settings = True

    def previous_button_clicked(self):
        self.page -= 1

    def next_button_clicked(self):
        self.page += 1
    
    def play_level(self, num):
        self.current_level = self.levels[num - 1]
        self.maze_width = len(self.current_level['maze'])
        self.maze_height = len(self.current_level['maze'][0])
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height, self.current_level['maze']) # Loads maze layout for the current level
        self.player = Player(self.game, self.maze, self.start_node_pos[0], self.start_node_pos[1]) # Instantiates player
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        self.goal_node_image = pg.transform.smoothscale(load_image('goal_node.png'), (self.maze.cell_size, self.maze.cell_size))
        self.goal_node_rect = self.goal_node_image.get_rect()
        self.path = self.maze.run_dijkstra(self.start_node_pos, self.goal_node_pos) # List of nodes that form the shortest path maze solution
        self.star_rating = 3
        self.state = 'play'
        self.reset()
        if self.game.play_mode.darkness_mode: # Chooses which soundtrack to play
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_gameplay_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_gameplay_music.mp3'))
            pg.mixer.music.play(-1)
        
    def draw_icon_info(self): # Draw the numbers and star rating on each level icon button
        match self.page:
            case 1:
                start, stop = 0, 15
            case 2:
                start, stop = 15, 30
            case 3:
                start, stop = 30, 45
        for i in range(start, stop):
            # Draw the level numbering
            draw_text(
                self.game.screen,
                str(i + 1),
                self.levels_icons[i].x,
                self.levels_icons[i].y,
                self.level_number_font,
                WHITE,
                'center'
            )
            # Draws the level star ratings
            match self.levels[i]['stars'][self.get_mode()]:
                case 0:
                    star_rating_image = self.zero_star_image
                    star_rating_rect = self.zero_star_rect
                    star_rating_rect.center = (self.levels_icons[i].x, self.levels_icons[i].y + 70)
                case 1:
                    star_rating_image = self.one_star_image
                    star_rating_rect = self.one_star_rect
                    star_rating_rect.center = (self.levels_icons[i].x, self.levels_icons[i].y + 70)
                case 2:
                    star_rating_image = self.two_star_image
                    star_rating_rect = self.two_star_rect
                    star_rating_rect.center = (self.levels_icons[i].x, self.levels_icons[i].y + 70)
                case 3:
                    star_rating_image = self.three_star_image
                    star_rating_rect = self.three_star_rect
                    star_rating_rect.center = (self.levels_icons[i].x, self.levels_icons[i].y + 70)
            self.game.screen.blit(star_rating_image, star_rating_rect)
    
    def draw_instructions(self):
        if self.current_level['number'] == 1: # Draws instructions only in Level 1
            draw_text( # Line 1
                self.game.screen,
                'Press',
                (self.maze_surface_pos[0]) // 2,
                SCREEN_HEIGHT // 2 - 125,
                self.UI_text_font,
                WHITE,
                'center'
            )
            draw_text( # Line 2
                self.game.screen,
                'ARROW',
                (self.maze_surface_pos[0]) // 2 - 51,
                SCREEN_HEIGHT // 2 - 75,
                self.UI_label_font,
                WHITE,
                'center'
            )
            draw_text( # Line 2
                self.game.screen,
                'keys',
                (self.maze_surface_pos[0]) // 2 + 89,
                SCREEN_HEIGHT // 2 - 75,
                self.UI_text_font,
                WHITE,
                'center'
            )
            draw_text( # Line 3
                self.game.screen,
                'or',
                (self.maze_surface_pos[0]) // 2,
                SCREEN_HEIGHT // 2 - 25,
                self.UI_text_font,
                WHITE,
                'center'
            )
            draw_text( # Line 4
                self.game.screen,
                'W A S D',
                (self.maze_surface_pos[0]) // 2,
                SCREEN_HEIGHT // 2 + 25,
                self.UI_label_font,
                WHITE,
                'center'
            )
            draw_text( # Line 5
                self.game.screen,
                'to move',
                (self.maze_surface_pos[0]) // 2,
                SCREEN_HEIGHT // 2 + 125,
                self.UI_text_font,
                WHITE,
                'center'
            )
    
    def draw_stars_collected(self): # Draws total no. stars collected from every level out of 135 stars (45 * 3 = 135)
        draw_text(
            self.game.screen,
            f'{self.get_stars_collected()} / 135',
            SCREEN_WIDTH - 100,
            8,
            self.stars_collected_font,
            WHITE,
            'topleft'
        )
        self.game.screen.blit(self.star_image, (SCREEN_WIDTH - 133, 7))

class Button:
    def __init__(self, game, x, y, images, action = None, width = None, height = None, name = None):
        self.game = game
        self.x = x
        self.y = y
        self.images = [] # List of image variants or 'costumes'
        if width and height:
            if isinstance(images, list): # If list and has width and height scaling
                for image in images:
                    self.images.append(pg.transform.smoothscale(load_image(image), (width, height)))
            else: # If not list and has width and height scaling
                self.images.append(pg.transform.smoothscale(load_image(images), (width, height)))
        else:
            if isinstance(images, list): # If list and has no width and height scaling
                for image in images:
                    self.images.append(load_image(image))
            else: # Not list and has no width and height scaling
                self.images.append(load_image(images))
        self.mask = pg.mask.from_surface(self.images[0]) # Creates mask of button
        self.rect = self.images[0].get_rect(center = (x, y))
        self.action = action
        self.name = name # This is an option attribute that stores the button's name

    def draw(self, index = 0):
        self.game.screen.blit( # Draws correct image according to theme/state
            self.images[min(len(self.images) - 1, index)],
            self.rect
        )
    
    def clicked(self): # Button clicking detection
        if self.rect.collidepoint(self.game.mouse_pos): # First checks if button rectangle is clicked
            pixel_x = self.game.mouse_x - self.rect.left # Relative x-coord of image pixel clicked
            pixel_y = self.game.mouse_y - self.rect.top # Relative y-coord of image pixel clicked
            if self.mask.get_at((pixel_x, pixel_y)): # Checks if pixel clicked is not transparent and activates on-click function if so
                if self.name:
                    self.action(self.name) # Passes name for reference if included
                else:
                    self.action()
                # Plays clicking sound effect
                if self.game.mute_sfx:
                    self.game.click_sound.set_volume(0)
                else:
                    self.game.click_sound.set_volume(self.game.sfx_volume)
                self.game.click_sound.play()

class Node: # Nodes are each square that forms the 2D maze array
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
    def __init__(self, width, height, surface_pos, surface_width, surface_height, walls_dict = None):
        self.width = width
        self.height = height
        self.stack = [] # Temporary stack used for the DFS maze generation algorithm
        self.array = self.create_2D_array(width, height) # Creates a 2D array full of Node objects
        # Determining the appropriate cell size from the ratio of space given to maze size
        self.cell_size = min(surface_width // self.width, surface_height // self.height) # Take the smallest value as the node is a square
        # Determine the coords of where to start drawing from to ensure the maze is aligned at the centre
        self.start_x = surface_pos[0] + (surface_width - self.cell_size * self.width) // 2
        self.start_y = surface_pos[1] + (surface_height - self.cell_size * self.height) // 2
        if walls_dict: # If walls dict provided (from Levels game mode) then fill in walls to acheive the maze layout of the current level to be played
            for x in range(self.width):
                for y in range(self.height):
                    self.array[x][y].walls = walls_dict[x][y]
        else: # Else generate walls (for Endless game mode)
            self.generate()

    def to_dict(self): # This function is redundant as it was used solely for making the maze layout for levels 1-45 in Levels game mode
        array = []     # Converts Maze object into a JSON-friendly dictionary (so that it can be saved to JSON)
        for x in range(self.width):
            array.append([])
            for y in range(self.height):
                array[x].append(self.array[x][y].walls)
        return array

    def create_2D_array(self, width, height): # Creates a 2D array full of Node objects
        array = []
        for x in range(width):
            array.append([])
            for y in range(height):
                array[x].append(Node(x, y))
        return array
    
    def get_unvisited_neighbours(self, node): # Returns a list of univisited neighbouring nodes for maze generation
        neighbours = []

        if node.y > 0: # Checks top neighbour (only if exists)
            if self.array[node.x][node.y - 1].is_visited == False:
                neighbours.append(self.array[node.x][node.y - 1])
        
        if node.y < self.height - 1: # Checks bottom neighbour (only if exists)
            if self.array[node.x][node.y + 1].is_visited == False:
                neighbours.append(self.array[node.x][node.y + 1])

        if node.x > 0: # Checks left neighbour (only if exists)
            if self.array[node.x - 1][node.y].is_visited == False:
                neighbours.append(self.array[node.x - 1][node.y])   

        if node.x < self.width - 1: # Checks right neighbour (only if exists)
            if self.array[node.x + 1][node.y].is_visited == False:
                neighbours.append(self.array[node.x + 1][node.y])

        return neighbours
    
    def remove_walls(self, node1, node2): # Removes the walls seperating two nodes
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
        
    def generate(self): # Randomly generates maze using DFS algorithm (aka recursive backtracking algorithm)
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

    def draw(self, screen, pathfinding_algorithm = None, path = None, path_pointer = None, wall_colour = WHITE): # Draws the maze
        wall_thickness = max(self.cell_size // 12, 1) # Cell size : Wall thickenss ratio - minimum 1px

        # Draws the colour coding of the pathfinding algorithm visualiser
        if pathfinding_algorithm:
            for x in range(self.width):
                for y in range(self.height):
                    cell = self.array[x][y]
                    x_pos = self.start_x + x * self.cell_size
                    y_pos = self.start_y + y * self.cell_size
                    cell_rect = pg.Rect(x_pos, y_pos, self.cell_size, self.cell_size)

                    if cell == pathfinding_algorithm.start_node:
                        colour = CYAN # Represents start node
                    elif cell == pathfinding_algorithm.goal_node:
                        colour = GOLD # Represents goal node
                    elif path and cell in path[:path_pointer + 1]:
                        colour = DARK_GREEN # Represents path node if exists
                    elif cell == pathfinding_algorithm.current_node:
                        colour = RED # Represents current node
                    elif cell in pathfinding_algorithm.open_set:
                        colour = PINK # Represents queued node
                    elif cell.is_path_visited:
                        colour = GREEN # Represents visited node
                    else:
                        colour = None
                    if colour:
                        pg.draw.rect(screen, colour, cell_rect)

        # Draw cell walls
        for x in range(self.width):
            for y in range(self.height):
                cell = self.array[x][y]
                x_pos = self.start_x + x * self.cell_size
                y_pos = self.start_y + y * self.cell_size

                if cell.walls['top'] == True: # Draws top wall
                    top = pg.Rect(x_pos - wall_thickness, y_pos, self.cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, top)

                if cell.walls['bottom'] == True: # Draws bottom wall
                    bottom = pg.Rect(x_pos - wall_thickness, y_pos + self.cell_size - wall_thickness, self.cell_size + 2 * wall_thickness, wall_thickness)
                    pg.draw.rect(screen, wall_colour, bottom)

                if cell.walls['left'] == True: # Draws left wall
                    left = pg.Rect(x_pos, y_pos - wall_thickness, wall_thickness, self.cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, left)

                if cell.walls['right'] == True: # Draws right wall
                    right = pg.Rect(x_pos + self.cell_size - wall_thickness, y_pos - wall_thickness, wall_thickness, self.cell_size + 2 * wall_thickness)
                    pg.draw.rect(screen, wall_colour, right)
        
        # Draws border around the maze
        self.draw_border(screen, wall_colour)

    def draw_border(self, screen, wall_colour = WHITE): # Draws border around the maze
        wall_thickness = max(self.cell_size // 12, 1) # Cell size : Wall thickenss ratio - minimum 1px
        # Draws border
        top_border = pg.Rect( # Draws top border
            self.start_x - wall_thickness,
            self.start_y - wall_thickness,
            self.cell_size * self.width + 2 * wall_thickness,
            wall_thickness * 2
        )
        pg.draw.rect(screen, wall_colour, top_border)
        bottom_border = pg.Rect( # Draws bottom border
            self.start_x - wall_thickness,
            self.start_y + self.cell_size * self.height - wall_thickness,
            self.cell_size * self.width + 2 * wall_thickness,
            wall_thickness * 2
        )
        pg.draw.rect(screen, wall_colour, bottom_border)
        left_border = pg.Rect( # Draws left border
            self.start_x - wall_thickness,
            self.start_y - wall_thickness,
            wall_thickness * 2,
            self.cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, left_border)
        right_border = pg.Rect( # Draws right border
            self.start_x + self.cell_size * self.width - wall_thickness,
            self.start_y - wall_thickness,
            wall_thickness * 2,
            self.cell_size * self.height + 2 * wall_thickness
        )
        pg.draw.rect(screen, wall_colour, right_border)

    def pos_to_px(self, pos): # Converts position in the maze to pixel position on the screen
        return [self.start_x + (pos[0] + 0.5) * self.cell_size, self.start_y + (pos[1] + 0.5) * self.cell_size]

    def px_to_pos(self, px): # Converts pixel position on the screen to position in the maze
        return [(px[0] - self.start_x) / self.cell_size - 0.5, (px[1] - self.start_y) / self.cell_size - 0.5]
    
    def target_node(self, pos, direction): # Finds the furthest node a player can reach when travelling in one direction without crossing a junction
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
    
    def run_dijkstra(self, start_node_pos, goal_node_pos): # Runs Dijkstra's algorithm to find the shortest path
        start_node = self.array[start_node_pos[0]][start_node_pos[1]]
        goal_node = self.array[goal_node_pos[0]][goal_node_pos[1]]
        return Dijkstra(self).run(start_node, goal_node)
    
    def setup_dijkstra(self, start_node_pos, goal_node_pos): # Sets up the animation for the Dijkstra's algorithm visualiser
        start_node = self.array[start_node_pos[0]][start_node_pos[1]]
        goal_node = self.array[goal_node_pos[0]][goal_node_pos[1]]
        dijkstra = Dijkstra(self)
        dijkstra.setup(start_node, goal_node)
        return dijkstra

    def setup_astar(self, start_node_pos, goal_node_pos): # Sets up the animation for the A* algorithm visualiser
        start_node = self.array[start_node_pos[0]][start_node_pos[1]]
        goal_node = self.array[goal_node_pos[0]][goal_node_pos[1]]
        astar = AStar(self)
        astar.setup(start_node, goal_node)
        return astar

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
        # Target node - the furthest node a player can reach when travelling in one direction without crossing a junction
        self.target_node_pos = None
        self.target_node_px = None

        self.speed = 5 # Moves 5 pixels per frame
        self.colour = GREEN
        self.trail_colour = GREEN
        self.trail = [(self.x, self.y)] # Trail path nodes
        self.moves = 0 # No. moves made

    def update(self):
        self.handle_input()
        self.move()

    def handle_input(self):
        if not self.is_moving: # Resets queued direction to none when stationary
            self.queued_direction = None

        if self.game.key_pressed == pg.K_UP or self.game.key_pressed == pg.K_w: # Up key / W clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['top'] and not self.is_moving: # Moves north if no top wall and stationary
                self.direction = 'north'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking() # Corrects trail animation when backtracking
            elif self.is_moving: # Sets queued direction to north if there is a top wall and player is in motion
                self.queued_direction = 'north'
        elif self.game.key_pressed == pg.K_DOWN or self.game.key_pressed == pg.K_s: # Down key / S clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['bottom'] and not self.is_moving: # Moves south if no bottom wall and stationary
                self.direction = 'south'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking() # Corrects trail animation when backtracking
            elif self.is_moving: # Sets queued direction to south if there is a bottom wall and player is in motion
                self.queued_direction = 'south'
        elif self.game.key_pressed == pg.K_LEFT or self.game.key_pressed == pg.K_a: # Left key / A clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['left'] and not self.is_moving: # Moves west if no left wall and stationary
                self.direction = 'west'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking() # Corrects trail animation when backtracking
            elif self.is_moving: # Sets queued direction to west if there is a left wall and player is in motion
                self.queued_direction = 'west'
        elif self.game.key_pressed == pg.K_RIGHT or self.game.key_pressed == pg.K_d: # Right key / D clicked
            if not self.maze.array[int(self.x)][int(self.y)].walls['right'] and not self.is_moving: # Moves east if no right wall and stationary
                self.direction = 'east'
                self.is_moving = True
                self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
                self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
                self.handle_backtracking() # Corrects trail animation when backtracking
            elif self.is_moving: # Sets queued direction to east if there is a right wall and player is in motion
                self.queued_direction = 'east'

    def move(self):
        if self.is_moving:
            if self.direction == 'north':
                if self.px[1] > self.target_node_px[1]: # Moves if hasn't reach target node
                    self.px[1] -= self.speed # Move up
                else:
                     # Snaps the players px coords to taget node px coords, to align the player in the cell when stationary
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]

                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    self.moves += 1 # Increment moves counter
                    if (self.x, self.y) != self.trail[-1]: # If new node visited
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop() # Remove last item if player is backtracking
                        else:
                            self.trail.append((self.x, self.y)) # Add item if new node visiited

            elif self.direction == 'east':
                if self.px[0] < self.target_node_px[0]: # Moves if hasn't reach target node
                    self.px[0] += self.speed # Move right
                else:
                     # Snaps the players px coords to taget node px coords, to align the player in the cell when stationary
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]

                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    self.moves += 1 # Increment moves counter
                    if (self.x, self.y) != self.trail[-1]: # If new node visited
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop() # Remove last item if player is backtracking
                        else:
                            self.trail.append((self.x, self.y)) # Add item if new node visiited

            elif self.direction == 'south':
                if self.px[1] < self.target_node_px[1]: # Moves if hasn't reach target node
                    self.px[1] += self.speed # Move down
                else:
                     # Snaps the players px coords to taget node px coords, to align the player in the cell when stationary
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]
                    
                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    self.moves += 1 # Increment moves counter
                    if (self.x, self.y) != self.trail[-1]: # If new node visited
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop() # Remove last item if player is backtracking
                        else:
                            self.trail.append((self.x, self.y)) # Add item if new node visiited

            elif self.direction == 'west':
                if self.px[0] > self.target_node_px[0]: # Moves if hasn't reach target node
                    self.px[0] -= self.speed # Move left
                else:
                     # Snaps the players px coords to taget node px coords, to align the player in the cell when stationary
                    self.px[0] = self.target_node_px[0]
                    self.px[1] = self.target_node_px[1]

                    self.x = self.target_node_pos[0]
                    self.y = self.target_node_pos[1]
                    self.is_moving = False
                    self.moves += 1 # Increment moves counter
                    if (self.x, self.y) != self.trail[-1]: # If new node visited
                        if len(self.trail) >= 2 and (self.x, self.y) == self.trail[-2]:
                            self.trail.pop() # Remove last item if player is backtracking
                        else:
                            self.trail.append((self.x, self.y)) # Add item if new node visiited

        if self.queued_direction and not self.is_moving: # Checks for any queued direction
            self.direction = self.queued_direction # Queued direction now becomes the current direction
            self.queued_direction = None # Current queued direction is cleared
            self.is_moving = True
            self.target_node_pos = self.maze.target_node((self.x, self.y), self.direction)
            self.target_node_px = self.maze.pos_to_px(self.target_node_pos)
            self.handle_backtracking() # Corrects trail animation when backtracking

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

    def create_rect(self, start_px, end_px, thickness): # Draws a vertical or horizontal rectangle based on the two points given
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
            self.trail.pop() # Remove last item if player is backtracking

    def draw(self): # Draws player as a circle and the trail
        self.draw_trail()
        pg.draw.circle(self.game.screen, self.colour, (int(self.px[0]), int(self.px[1])), self.maze.cell_size // 2.5)

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.image = pg.transform.smoothscale(load_image('paused.png'), (419, 161)) # Pause title
        self.buttons = [
            Button(self.game, SCREEN_WIDTH // 2, 421, 'play_button2.png', self.play_button_clicked, 206, 206),
            Button(self.game, 452, 421, 'home_button.png', self.home_button_clicked, 139, 139),
            Button(self.game, 828, 421, 'controls_button.png', self.controls_button_clicked, 139, 139),
        ]
        self.overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA) # Darkens screen
        self.overlay.fill((0, 0, 0, 180))
    
    def draw(self):
        self.game.screen.blit(self.overlay, (0, 0))
        self.game.screen.blit(self.image, (431, 170))
        for button in self.buttons:
            button.draw()

    def buttons_clicked(self):
        for button in self.buttons:
            button.clicked()

    def play_button_clicked(self):
        self.game.is_paused = False # Exits pause menu state
        self.game.state.elapsed_pause_time = pg.time.get_ticks() - self.game.state.start_pause_time # Calculate pause duration
        self.game.state.start_time += self.game.state.elapsed_pause_time # Shifts start time forward when unpaused
        pg.mixer.music.unpause()

    def home_button_clicked(self):
        self.game.is_paused = False # Exits pause menu state
        # Returns to correct game mode
        if self.game.state == self.game.levels_game_mode:
            self.game.state.state = 'select'
        else:
            self.game.state = self.game.play_mode
        # Choose which soundtrack to play based on the darkness mode theme being on/off
        if self.game.play_mode.darkness_mode:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_bg_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
            pg.mixer.music.play(-1)
        pg.mixer.music.unpause()

    def controls_button_clicked(self):
        self.game.show_settings = True

class WinScreen: # Parent class
    def __init__(self, game):
        self.game = game
        self.image1 = pg.transform.smoothscale(load_image('win1.png'), (720, 649)) # Win screen image without icons for time taken and moves made
        self.image2 = pg.transform.smoothscale(load_image('win2.png'), (720, 649)) # Win screen image with icons for time taken and no. moves made
        self.overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA) # Darkens screen
        self.overlay.fill((0, 0, 0, 180))
        self.font = pg.font.Font(MONTSERRAT_BOLD, 32)
        self.zero_star_image = pg.transform.smoothscale(load_image('0 star.png'), (261, 87))
        self.one_star_image = pg.transform.smoothscale(load_image('1 star.png'), (261, 87))
        self.two_star_image = pg.transform.smoothscale(load_image('2 star.png'), (261, 87))
        self.three_star_image = pg.transform.smoothscale(load_image('3 star.png'), (261, 87))
        self.current_star = 0 # Current star value during animation
        self.current_star_image = self.zero_star_image # Current star animated
        self.next_animation_time = 0
        self.animation_delay = 500 # ms between each animation frame
        self.stop_animation = False
    
    def draw(self):
        self.game.screen.blit(self.overlay, (0, 0))
        self.game.screen.blit(self.current_star_image, (510, 186))
        if self.stop_animation:
            self.game.screen.blit(self.image2, (280, 41)) # Draws the 2nd image when animation finished
            for button in self.buttons:
                button.draw()
            time = f'{self.game.state.minutes:02d}:{self.game.state.seconds:02d}' # Clock display MM:SS
            draw_text(self.game.screen, time, SCREEN_WIDTH // 2, 590, self.font, WHITE, 'center') # Draws time taken
            moves = str(self.game.state.player.moves) # Obtain the no. moves made from Player class
            draw_text(self.game.screen, moves, SCREEN_WIDTH // 2, 667, self.font, WHITE, 'center') # Draws no. moves made
        else:
            self.game.screen.blit(self.image1, (280, 41)) # Draws the 1st image during animation

    def update(self):
        self.animate()

    def reset(self):
        self.game.state.reset()
        self.current_star = 0 # Current star value during animation
        self.current_star_image = self.zero_star_image # Current star animated
        self.next_animation_time = 0
        self.stop_animation = False

    def animate(self):
        if self.game.win and not self.stop_animation:
            current_time = pg.time.get_ticks() 
            if self.current_star < self.game.state.star_rating: # Animates until star rating is displayed
                if current_time - self.next_animation_time > self.animation_delay: # Display each star at intervals
                    self.current_star += 1
                    match self.current_star:
                        case 0:
                            self.current_star_image = self.zero_star_image
                        case 1:
                            self.current_star_image = self.one_star_image
                        case 2:
                            self.current_star_image = self.two_star_image
                        case 3:
                            self.current_star_image = self.three_star_image
                    # Plays the star 'ding' sound effect
                    if self.game.mute_sfx:
                        self.game.star_sound.set_volume(0)
                    else:
                        self.game.star_sound.set_volume(self.game.sfx_volume)
                    self.game.star_sound.play()

                    self.next_animation_time = current_time
            else:
                if current_time - self.next_animation_time > self.animation_delay: # Adds delay between star animation and rest of UI display
                    self.stop_animation = True
                    self.update_score()

    def buttons_clicked(self):
        if self.stop_animation:
            for button in self.buttons:
                button.clicked()

    def replay_button_clicked(self):
        self.reset()
        # Choose which soundtrack to play based on the darkness mode theme being on/off
        if self.game.play_mode.darkness_mode:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_gameplay_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_gameplay_music.mp3'))
            pg.mixer.music.play(-1)

    def controls_button_clicked(self):
        self.game.show_settings = True

class EndlessWinScreen(WinScreen):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            Button(self.game, SCREEN_WIDTH // 2, 421, 'replay_button.png', self.replay_button_clicked, 139, 139),
            Button(self.game, 452, 421, 'home_button.png', self.home_button_clicked, 139, 139),
            Button(self.game, 828, 421, 'controls_button.png', self.controls_button_clicked, 139, 139)
        ]
    
    def home_button_clicked(self):
        self.reset()
        self.game.state = self.game.play_mode
        # Choose which soundtrack to play based on the darkness mode theme being on/off
        if self.game.play_mode.darkness_mode:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_bg_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
            pg.mixer.music.play(-1)

    def update_score(self):
        if self.game.state.elapsed_time < self.game.state.get_shortest_time(): # Check high score for time
            self.game.state.stats['shortest_time'][self.game.state.get_mode()] = self.game.state.elapsed_time
            with open(os.path.join(DATA_DIR, 'stats.json'), 'w') as f: # Update .json file if there is a change
                json.dump(self.game.state.stats, f, indent = 4)
        if self.game.state.star_rating == 3:
            self.game.state.current_streak += 1 # Increment current streak
            if self.game.state.current_streak > self.game.state.get_best_streak(): # Check high score for streak
                self.game.state.stats['best_streak'][self.game.state.get_mode()] = self.game.state.current_streak
                with open(os.path.join(DATA_DIR, 'stats.json'), 'w') as f: # Update .json file if there is a change
                    json.dump(self.game.state.stats, f, indent = 4)
        else:
            self.game.state.current_streak = 0 # Streak broken


class LevelsWinScreen(WinScreen):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            Button(self.game, 574, 421, 'replay_button.png', self.replay_button_clicked, 119, 119),
            Button(self.game, 442, 421, 'home_button.png', self.home_button_clicked, 119, 119),
            Button(self.game, 838, 421, 'controls_button.png', self.controls_button_clicked, 119, 119),
            Button(self.game, 706, 421, 'continue_button.png', self.continue_button_clicked, 119, 119)
        ]
    
    def home_button_clicked(self):
        self.reset()
        self.game.state.state = 'select'
        # Choose which soundtrack to play based on the darkness mode theme being on/off
        if self.game.play_mode.darkness_mode:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_bg_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
            pg.mixer.music.play(-1)
    
    def continue_button_clicked(self): # Continues to next level
        if self.game.state.current_level['number'] == 45: # Quits to levels selector on last level
            self.home_button_clicked()
        else: # Continues to next level if not last level
            self.reset()
            self.game.state.play_level(self.game.state.current_level['number'] + 1)
    
    def update_score(self):
        if self.game.state.star_rating > self.game.state.levels[self.game.state.current_level['number'] - 1]['stars'][self.game.state.get_mode()]: # Check high score for star rating
            self.game.state.levels[self.game.state.current_level['number'] - 1]['stars'][self.game.state.get_mode()] = self.game.state.star_rating
            with open(os.path.join(DATA_DIR, 'levels.json'), 'w') as f: # Update .json file if there is a change
                json.dump(self.game.state.levels, f, indent = 4)

class Settings:
    def __init__(self, game):
        self.game = game
        self.image = pg.transform.smoothscale(load_image('settings.png'), (508, 170)) # Settings title
        self.buttons = [
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked, 81, 72),
            Button(self.game, 466, 360, ['sfx_on.png', 'sfx_off.png'], self.sfx_button_clicked, 76, 76),
            Button(self.game, 466, 500, ['music_on.png', 'music_off.png'], self.music_button_clicked, 76, 76)
        ]
        self.sfx_buttons = [ # SFX volume divisions
            Button(self.game, 549, 360, ['white_left_half_stadium.png', 'grey_left_half_stadium.png'], self.set_sfx_volume, 62, 44, 1),
            Button(self.game, 615, 360, ['white_rectangle.png', 'grey_rectangle.png'], self.set_sfx_volume, 62, 44, 2),
            Button(self.game, 681, 360, ['white_rectangle.png', 'grey_rectangle.png'], self.set_sfx_volume, 62, 44, 3),
            Button(self.game, 747, 360, ['white_rectangle.png', 'grey_rectangle.png'], self.set_sfx_volume, 62, 44, 4),
            Button(self.game, 813, 360, ['white_right_half_stadium.png', 'grey_right_half_stadium.png'], self.set_sfx_volume, 62, 44, 5)
        ]
        self.music_buttons = [ # Music volume divisions
            Button(self.game, 549, 500, ['white_left_half_stadium.png', 'grey_left_half_stadium.png'], self.set_music_volume, 62, 44, 1),
            Button(self.game, 615, 500, ['white_rectangle.png', 'grey_rectangle.png'], self.set_music_volume, 62, 44, 2),
            Button(self.game, 681, 500, ['white_rectangle.png', 'grey_rectangle.png'], self.set_music_volume, 62, 44, 3),
            Button(self.game, 747, 500, ['white_rectangle.png', 'grey_rectangle.png'], self.set_music_volume, 62, 44, 4),
            Button(self.game, 813, 500, ['white_right_half_stadium.png', 'grey_right_half_stadium.png'], self.set_music_volume, 62, 44, 5)
        ]
        self.overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA) # Darkens screen
        self.overlay.fill((0, 0, 0, 180))
    
    def draw(self):
        self.game.screen.blit(self.overlay, (0, 0))
        self.game.screen.blit(self.image, (386, 126))
        self.buttons[0].draw() # Draws back button
        self.buttons[1].draw(int(self.game.mute_sfx)) # Draws the mute/unmute SFX button whether the SFX is muted/unmuted
        self.buttons[2].draw(int(self.game.mute_music)) # Draws the mute/unmute music button whether the music is muted/unmuted
        for button in self.sfx_buttons: # Makes all SFX volume divisions grey at first
            button.draw(1)
        for button in self.music_buttons: # Makes all music volume divisions grey at first
            button.draw(1)
        if not self.game.mute_sfx:
            for button in self.sfx_buttons[:int(self.game.sfx_volume * 5)]: # Makes divisions 1 to x white until they correspond to the current SFX volume
                button.draw(0)
        if not self.game.mute_music:
            for button in self.music_buttons[:int(self.game.music_volume * 5)]: # Makes divisions 1 to x white until they correspond to the current music volume
                button.draw(0)
    
    def update(self): # The existance of this function is necessary, as it acts as a placeholder for the logic in the Game class
        pass

    def buttons_clicked(self): # Activates all buttons
        for button in self.buttons:
            button.clicked()
        for button in self.sfx_buttons:
            button.clicked()
        for button in self.music_buttons:
            button.clicked()

    def back_button_clicked(self):
        self.game.show_settings = False # Exits settings

    def sfx_button_clicked(self):
        self.game.mute_sfx = not self.game.mute_sfx # Switches between mute and unmuted state
        self.save_to_json() # Saves changes to the settings.json file

    def music_button_clicked(self):
        self.game.mute_music = not self.game.mute_music # Switches between mute and unmuted state
        if self.game.mute_music:
            pg.mixer.music.set_volume(0) # Sets music volume to zero if muted
        else:
            pg.mixer.music.set_volume(self.game.music_volume) # Sets music volume to current value
        self.save_to_json() # Saves changes to the settings.json file

    def set_sfx_volume(self, num):
        self.game.sfx_volume = num * 0.2 # Converts from divisions 1, 2, 3, 4, 5 to decimals 0.2, 0.4, 0.6, 0.8, 1.0 respectively
        self.game.mute_sfx = False # Breaks out of muted state
        self.save_to_json() # Saves changes to the settings.json file

    def set_music_volume(self, num):
        self.game.music_volume = num * 0.2 # Converts from divisions 1, 2, 3, 4, 5 to decimals 0.2, 0.4, 0.6, 0.8, 1.0 respectively
        self.game.mute_music = False # Breaks out of muted state
        pg.mixer.music.set_volume(self.game.music_volume) # Sets music volume to current value
        self.save_to_json() # Saves changes to the settings.json file

    def save_to_json(self): # Saves the volume control values to the settings.json file
        settings_info = {
            'mute_sfx': self.game.mute_sfx,
            'sfx_volume': self.game.sfx_volume,
            'mute_music': self.game.mute_music,
            'music_volume': self.game.music_volume
        }
        with open(os.path.join(DATA_DIR, 'settings.json'), 'w') as f:
            json.dump(settings_info, f, indent = 4)

class Dijkstra:
    def __init__(self, maze):
        self.maze = maze
        self.current_node = None
        self.open_set = None # List of nodes the algorithm is queueing

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
            path.append(current_node) # Connects the previous node pointers to form a list
        return path

    def run(self, start_node, goal_node): # Gives the shortest path instantly
        self.reset_nodes()
        start_node.distance = 0
        open_set = [] # List of nodes the algorithm is queueing
        open_set.append(start_node)

        while open_set:
            closest_node = open_set[0]
            index = 0
            # Finds the closest node in the open set based on distance cost
            for i in range(len(open_set)):
                if open_set[i].distance < closest_node.distance:
                    closest_node = open_set[i]
                    index = i
            # Visits the closest node in the open set and removes it from open set
            current_node = open_set.pop(index)
            current_node.is_path_visited = True 
            # Algorithm stops if the goal node is found
            if current_node == goal_node:
                return self.retrace(goal_node) # Returns the path nodes list if goal node is found
            # Investigates the current node's neighbours
            neighbouring_nodes = self.maze.get_reachable_neighbours(current_node)
            for i in range(len(neighbouring_nodes)): # Find an unvisited neighbouring node
                if not neighbouring_nodes[i].is_path_visited:
                    new_distance = current_node.distance + 1 # Distance from start increases by 1 each square
                    if new_distance < neighbouring_nodes[i].distance: # Updates the nodes' distance from start if a shorter distance is found
                        neighbouring_nodes[i].distance = new_distance
                        neighbouring_nodes[i].previous_node = current_node
                        open_set.append(neighbouring_nodes[i])

    def setup(self, start_node, goal_node): # Sets up the animation for the Dijkstra's algorithm visualiser
        self.reset_nodes()
        self.start_node = start_node
        self.goal_node = goal_node
        self.start_node.distance = 0
        self.open_set = [] # List of nodes the algorithm is queueing
        self.open_set.append(self.start_node)

    
    def run_frame(self):
        if self.open_set:
            self.closest_node = self.open_set[0]
            index = 0
             # Finds the closest node in the open set based on distance cost
            for i in range(len(self.open_set)):
                if self.open_set[i].distance < self.closest_node.distance:
                    self.closest_node = self.open_set[i]
                    index = i
            # Visits the closest node in the open set and removes it from open set
            self.current_node = self.open_set.pop(index)
            self.current_node.is_path_visited = True
            # Algorithm stops if the goal node is found
            if self.current_node == self.goal_node:
                return self.retrace(self.goal_node) # Returns the path nodes list if goal node is found
            # Investigates the current node's neighbours
            self.neighbouring_nodes = self.maze.get_reachable_neighbours(self.current_node)
            for i in range(len(self.neighbouring_nodes)): # Find an unvisited neighbouring node
                if not self.neighbouring_nodes[i].is_path_visited:
                    new_distance = self.current_node.distance + 1 # Distance from start increases by 1 each square
                    if new_distance < self.neighbouring_nodes[i].distance: # Updates the nodes' distance from start if a shorter distance is found
                        self.neighbouring_nodes[i].distance = new_distance
                        self.neighbouring_nodes[i].previous_node = self.current_node
                        self.open_set.append(self.neighbouring_nodes[i])
            
            return False # Returns False if search needs to carry on
        else:
            return True # Returns True if search is finished

class AStar:
    def __init__(self, maze):
        self.maze = maze
        self.current_node = None
        self.open_set = None # List of nodes the algorithm is queueing

    def get_heuristic(self, node):
        return abs(node.x - self.goal_node.x) + abs(node.y - self.goal_node.y) # Returns the manhattan distance as the heuristic value

    def reset_nodes(self): # Resets all nodes' pathfinding attributes
        for column in self.maze.array:
            for node in column:
                node.is_path_visited = False
                node.distance = float('inf') # Set to infinity
                node.previous_node = None
                node.heuristic = self.get_heuristic(node)

    def retrace(self, goal_node): # Outputs the path of nodes from goal node to start node
        current_node = goal_node
        path = [goal_node]
        while current_node.previous_node:
            current_node = current_node.previous_node
            path.append(current_node) # Connects the previous node pointers to form a list
        return path

    def setup(self, start_node, goal_node): # Sets up the animation for the A* algorithm visualiser
        self.start_node = start_node
        self.goal_node = goal_node
        self.reset_nodes()
        self.start_node.distance = 0
        self.open_set = [] # List of nodes the algorithm is queueing
        self.open_set.append(self.start_node)
    
    def run_frame(self):
        if self.open_set:
            self.closest_node = self.open_set[0]
            index = 0
            # Finds the closest node in the open set based on distance + heuristic cost
            for i in range(len(self.open_set)):
                if self.open_set[i].distance + self.open_set[i].heuristic < self.closest_node.distance + self.closest_node.heuristic:
                    self.closest_node = self.open_set[i]
                    index = i
            # Visits the closest node in the open set and removes it from open set
            self.current_node = self.open_set.pop(index)
            self.current_node.is_path_visited = True
            # Algorithm stops if the goal node is found
            if self.current_node == self.goal_node:
                return self.retrace(self.goal_node) # Returns the path nodes list if goal node is found
            # Investigates the current node's neighbours
            self.neighbouring_nodes = self.maze.get_reachable_neighbours(self.current_node)
            for i in range(len(self.neighbouring_nodes)): # Find an unvisited neighbouring node
                if not self.neighbouring_nodes[i].is_path_visited:
                    new_distance = self.current_node.distance + 1 # Distance from start increases by 1 each square
                    if new_distance < self.neighbouring_nodes[i].distance: # Updates the nodes' distance from start if a shorter distance is found
                        self.neighbouring_nodes[i].distance = new_distance
                        self.neighbouring_nodes[i].previous_node = self.current_node
                        self.open_set.append(self.neighbouring_nodes[i])
            
            return False # Returns False if search needs to carry on
        else:
            return True # Returns True if search is finished

class EducationMode:
    def __init__(self, game):
        self.game = game
        self.image = load_image('blank.png')
        self.buttons = [
            # Static buttons
            Button(self.game, 56, 670, 'back_button.png', self.back_button_clicked, 81, 72),
            Button(self.game, 1230, 670, 'settings_button.png', self.settings_button_clicked, 72, 72),
            Button(self.game, SCREEN_WIDTH // 2 - 89, 682, 'slow_down_button.png', self.slow_down_button_clicked, 59, 59),
            Button(self.game, SCREEN_WIDTH // 2 + 89, 682, 'speed_up_button.png', self.speed_up_button_clicked, 59, 59),
            Button(self.game, 146, 204, 'minus_button.png', self.decrement_width, 37, 37),
            Button(self.game, 216, 204, 'plus_button.png', self.increment_width, 37, 37),
            Button(self.game, 146, 354, 'minus_button.png', self.decrement_height, 37, 37),
            Button(self.game, 216, 354, 'plus_button.png', self.increment_height, 37, 37),
            Button(self.game, 906, 55, 'refresh_button.png', self.refresh_button_clicked, 30, 30),
            Button(self.game, 100, 507, 'previous_button.png', self.previous_button_clicked, 55, 55),
            Button(self.game, 262, 507, 'next_button.png', self.next_button_clicked, 55, 55),
            # Dynamic buttons
            Button(self.game, SCREEN_WIDTH // 2, 682, 'play_button2.png', self.play_button_clicked, 59, 59),
            Button(self.game, SCREEN_WIDTH // 2, 682, 'pause_button.png', self.pause_button_clicked, 59, 59),
            Button(self.game, SCREEN_WIDTH // 2, 682, 'replay_button.png', self.replay_button_clicked, 59, 59),
            Button(self.game, 1222, 147, 'down_button.png', self.show_info_button_clicked, 55, 55),
            Button(self.game, 1222, 147, 'up_button.png', self.hide_info_button_clicked, 55, 55),
            Button(self.game, 1222, 395, 'down_button.png', self.show_stats_button_clicked, 55, 55),
            Button(self.game, 1222, 395, 'up_button.png', self.hide_stats_button_clicked, 55, 55)
        ]
        # Where to draw the maze
        self.maze_surface_pos = (353, 73)
        self.maze_surface_width = 575
        self.maze_surface_height = 575
        # Maze dimensions
        self.maze_width = 20
        self.maze_height = 20

        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height) # Generates new maze
        self.start_node_pos = (0, 0)
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        self.dijkstra = self.maze.setup_dijkstra(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the Dijkstra's algorithm visualiser
        self.astar = self.maze.setup_astar(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the A* algorithm visualiser
        self.current_algorithm_name = "Dijkstra's" # Current algrothm to run
        self.current_algorithm = self.dijkstra # Current algorithm running
        self.status = "Ready" # Part of the info text which describes the status of the algorithm
        self.next_animation_time = 0
        self.animation_delay = 100 # ms between each animation frame
        self.speed_multiplier = { # Describes the animation delay as a multiple of the default speed (100ms) so I can display as text
            0: "Max",
            50: "2x",
            100: "1x",
            150: "0.67x",
            200: "0.5x",
            250: "0.4x",
            300: "0.33x",
            350: "0.29x",
            400: "0.25x",
            450: "0.22x",
            500: "Min"
        }
        self.stop_animation = False
        self.stop_path_animation = False
        self.is_paused = True
        self.path = None # List of nodes that form the shortest path maze solution
        self.path_pointer = 0 # Slice index value of the path list for the final path animation
        # Stats
        self.visited_nodes = 0
        self.queued_nodes = 0
        self.path_length = 0

        self.show_stats = False
        self.show_info = False
        # Info text line-by-line
        self.lines = [
            "Dijkstra's Algorithm:",
            "",
            "Finds shortest path from start to goal",
            "Explores nodes by lowest distance",
            "Selects node with lowest distance",
            "",
            "No heuristic used",
            "",
            f"Status: {self.status}"
        ]

        self.UI_label_font = pg.font.Font(MONTSERRAT_BOLD, 26)
        self.UI_text_font1 = pg.font.Font(MONTSERRAT_REG, 26)
        self.UI_text_font2 = pg.font.Font(MONTSERRAT_REG, 16)
        self.title = "Visualiser"
        self.title_colour = CYAN
        self.title_text_font = pg.font.Font(PARKVANE, 50)
        self.horizontal_line1 = pg.Rect(970, 168, 265, 2) # Drawn underneath info title
        self.horizontal_line2 = pg.Rect(970, 416, 265, 2) # Drawn underneath stats title
        # Legend for the colour coding of the pathfinding algorithm visualiser
        self.visited_nodes_rect = pg.Rect(988, 436, 9, 9)
        self.queued_nodes_rect = pg.Rect(988, 476, 9, 9)
        self.path_length_rect = pg.Rect(988, 516, 9, 9)

    def draw(self):
        self.game.screen.blit(self.image,(0,0))
        for button in self.buttons[:-7]: # Draws the static buttons
            button.draw()
        self.maze.draw(self.game.screen, self.current_algorithm, self.path, self.path_pointer)
        self.draw_info()
        self.draw_stats()
        self.draw_maze_dimension_controls()
        self.draw_algorithm_switcher()
        self.draw_title()
        self.draw_speed_multiplier()
        # Choose which of the dynamic buttons to draw
        if self.show_info:
            self.buttons[-3].draw() # Draw hide info button
        else:
            self.buttons[-4].draw() # Draw show info button

        if self.show_stats:
            self.buttons[-1].draw() # Draw hide stats button
        else:
            self.buttons[-2].draw() # Draw show stats button

        if self.stop_path_animation:
            self.buttons[-5].draw() # Draw replay button
        elif self.is_paused:
            self.buttons[-7].draw() # Draw play button
        else:
            self.buttons[-6].draw() # Draw pause button

    def update(self):
        self.run_animation()
        self.visited_nodes = 0
        for x in range(self.maze.width): # Computes no. nodes visited
            for y in range(self.maze.height):
                if self.maze.array[x][y].is_path_visited:
                    self.visited_nodes += 1
        self.queued_nodes = len(self.current_algorithm.open_set) # Updates no. queued nodes
        if self.path:
            self.path_length = len(self.path[:self.path_pointer + 1]) # Updates final path length
        self.update_info() # Updates info text

    def buttons_clicked(self):
        for button in self.buttons[:-7]: # Activates the static buttons
            button.clicked()
        # Choose which of the dynamic buttons to activate
        if self.show_info:
            self.buttons[-3].clicked() # Hide info button activated
        else:
            self.buttons[-4].clicked() # Show info button activated

        if self.show_stats:
            self.buttons[-1].clicked() # Hide stats button activated
        else:
            self.buttons[-2].clicked() # Show stats button activated

        if self.stop_path_animation:
            self.buttons[-5].clicked() # Replay button activated
        elif self.is_paused:
            self.buttons[-7].clicked() # Play button activated
        else:
            self.buttons[-6].clicked() # Pause button activated

    def back_button_clicked(self): # Exits education mode
        self.game.state = self.game.title_screen
        # Choose which soundtrack to play based on the darkness mode theme being on/off
        if self.game.play_mode.darkness_mode:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'darkness_bg_music.mp3'))
            pg.mixer.music.play(-1)
        else:
            pg.mixer.music.load(os.path.join(SOUNDS_DIR, 'normal_bg_music.mp3'))
            pg.mixer.music.play(-1)

    def settings_button_clicked(self):
        self.game.show_settings = True

    def show_info_button_clicked(self):
        self.show_info = True

    def hide_info_button_clicked(self):
        self.show_info = False

    def show_stats_button_clicked(self):
        self.show_stats = True

    def hide_stats_button_clicked(self):
        self.show_stats = False

    def play_button_clicked(self):
        self.is_paused = False

    def pause_button_clicked(self):
        self.is_paused = True

    def replay_button_clicked(self):
        if self.current_algorithm_name == "Dijkstra's":
            self.dijkstra = self.maze.setup_dijkstra(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the Dijkstra's algorithm visualiser
            self.current_algorithm = self.dijkstra
        else:
            self.astar = self.maze.setup_astar(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the A* algorithm visualiser
            self.current_algorithm = self.astar
        self.stop_animation = False
        self.stop_path_animation = False
        self.is_paused = False
        self.path = None # List of nodes that form the shortest path maze solution
        self.path_pointer = 0 # Slice index value of the path list for the final path animation
        # Stats
        self.visited_nodes = 0
        self.queued_nodes = 0
        self.path_length = 0

    def slow_down_button_clicked(self):
        self.animation_delay = min(500, self.animation_delay + 50) # Animation delay is capped to 500

    def speed_up_button_clicked(self):
        self.animation_delay = max(0, self.animation_delay - 50) # Animation delay cannot be negative

    def decrement_width(self):
        self.maze_width = max(6, self.maze_width - 1) # Maze width cannot go below 6 as this will lead to UI elements overlapping

    def increment_width(self):
        self.maze_width = min(50, self.maze_width + 1) # Maze width is capped to 50 as the game performance will slow down beyond 50

    def decrement_height(self):
        self.maze_height = max(6, self.maze_height - 1) # Maze height cannot go below 6 as this will lead to UI elements overlapping

    def increment_height(self):
        self.maze_height = min(50, self.maze_height + 1) # Maze height is capped to 50 as the game performance will slow down beyond 50

    def refresh_button_clicked(self):
        self.maze = Maze(self.maze_width, self.maze_height, self.maze_surface_pos, self.maze_surface_width, self.maze_surface_height) # Generates new maze
        self.start_node_pos = (0, 0)
        self.goal_node_pos = (self.maze_width - 1, self.maze_height - 1)
        if self.current_algorithm_name == "Dijkstra's":
            self.dijkstra = self.maze.setup_dijkstra(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the Dijkstra's algorithm visualiser
            self.current_algorithm = self.dijkstra
        else:
            self.astar = self.maze.setup_astar(self.start_node_pos, self.goal_node_pos) # Sets up the animation for the A* algorithm visualiser
            self.current_algorithm = self.astar
        self.status = "Ready" # Part of the info text which describes the status of the algorithm
        self.stop_animation = False
        self.stop_path_animation = False
        self.is_paused = True
        self.path = None # List of nodes that form the shortest path maze solution
        self.path_pointer = 0 # Slice index value of the path list for the final path animation
        # Stats
        self.visited_nodes = 0
        self.queued_nodes = 0
        self.path_length = 0

    def previous_button_clicked(self): # Switches algorithms
        if self.current_algorithm_name == "Dijkstra's":
            self.current_algorithm_name = 'A*'
        else:
            self.current_algorithm_name = "Dijkstra's"

    def next_button_clicked(self): # Switches algorithms
        if self.current_algorithm_name == "Dijkstra's":
            self.current_algorithm_name = 'A*'
        else:
            self.current_algorithm_name = "Dijkstra's"

    def run_animation(self):
        if not self.is_paused:
            if not self.stop_animation: # Runs the pathfinding animation until its stopped
                self.status = "Exploring" # Part of the info text which describes the status of the algorithm
                current_time = pg.time.get_ticks()
                if current_time - self.next_animation_time > self.animation_delay: # Runs each frame of the pathfinding animation at intervals
                    output = self.current_algorithm.run_frame()
                    self.next_animation_time = current_time
                    # Processes the value returned by the run_frame() method
                    if isinstance(output, list):
                        self.stop_animation = True
                        self.path = output # List of nodes that form the shortest path maze solution
                    else:
                        self.stop_animation = output

            elif not self.stop_path_animation and self.path: # Runs the final path animation until its stopped
                self.status = "Goal found - retracing path" # Part of the info text which describes the status of the algorithm
                current_time = pg.time.get_ticks()
                if current_time - self.next_animation_time > self.animation_delay: # Runs each frame of the final path animation at intervals
                    if self.path_pointer < len(self.path) - 1: # Updates the slice index value of the path list for the final path animation
                        self.path_pointer += 1
                        self.next_animation_time = current_time
                    else:
                        self.status = "Finished" # Part of the info text which describes the status of the algorithm
                        self.stop_path_animation = True

    def update_info(self): # Updates info text based on the current algorithm running
        if self.current_algorithm == self.dijkstra:
            self.lines = [
                "Dijkstra's Algorithm:",
                "",
                "Finds shortest path from start to goal",
                "Explores nodes by lowest distance",
                "Selects node with lowest distance",
                "",
                "No heuristic used",
                "",
                f"Status: {self.status}"
            ]
        else:
            self.lines = [
                "A* Algorithm:",
                "",
                "Finds shortest path from start to goal",
                "Uses distance + heuristic",
                "Selects node with lowest f(n)",
                "f(n) = g(n) + h(n)",
                "",
                "Usually faster than Dijkstra's",
                f"Status: {self.status}"
            ]

    def draw_info(self):
        draw_text( # Info title
            self.game.screen,
            'Info:',
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            147,
            self.UI_label_font,
            WHITE,
            'center'
        )
        pg.draw.rect(self.game.screen, WHITE, self.horizontal_line1)

        if self.show_info:
            line_spacing = 20
            for i, line in enumerate(self.lines):
                draw_text( # Each line
                    self.game.screen,
                    line,
                    (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
                    191 + i * line_spacing,
                    self.UI_text_font2,
                    WHITE,
                    'center'
                )    

    def draw_stats(self):
        draw_text( # Stats title
            self.game.screen,
            'Stats:',
            (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2,
            395,
            self.UI_label_font,
            WHITE,
            'center'
        )
        pg.draw.rect(self.game.screen, WHITE, self.horizontal_line2)

        if self.show_stats:
            draw_text( # Visited nodes stat
                self.game.screen,
                f'Visited nodes: {self.visited_nodes}',
                (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2 - 98,
                431,
                self.UI_text_font2,
                WHITE,
                'topleft'
            )
            draw_text( # Queued nodes stat
                self.game.screen,
                f'Queued nodes: {self.queued_nodes}',
                (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2 - 98,
                471,
                self.UI_text_font2,
                WHITE,
                'topleft'
            )
            draw_text( # Shortest path length stat
                self.game.screen,
                f'Shortest path length: {self.path_length}',
                (SCREEN_WIDTH + self.maze_surface_pos[0] + self.maze_surface_width) // 2 - 98,
                511,
                self.UI_text_font2,
                WHITE,
                'topleft'
            )
            # Legend
            pg.draw.rect(self.game.screen, GREEN, self.visited_nodes_rect)
            pg.draw.rect(self.game.screen, PINK, self.queued_nodes_rect)
            pg.draw.rect(self.game.screen, DARK_GREEN, self.path_length_rect)

    def draw_maze_dimension_controls(self):
        draw_text( # Width title
            self.game.screen,
            'Width:',
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            147,
            self.UI_label_font,
            WHITE,
            'center'
        )
        draw_text( # Width value
            self.game.screen,
            str(self.maze_width),
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2 + 5,
            202,
            self.UI_text_font1,
            WHITE,
            'center'
        )
        draw_text( # Height title
            self.game.screen,
            'Height:',
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            299,
            self.UI_label_font,
            WHITE,
            'center'
        )
        draw_text( # Height value
            self.game.screen,
            str(self.maze_height),
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2 + 5,
            354,
            self.UI_text_font1,
            WHITE,
            'center'
        )

    def draw_algorithm_switcher(self):
        draw_text( # Algorithm switcher title
            self.game.screen,
            'Algorithm:',
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2,
            451,
            self.UI_label_font,
            WHITE,
            'center'
        )
        draw_text( # Current algorithm
            self.game.screen,
            self.current_algorithm_name,
            (SCREEN_WIDTH - self.maze_surface_pos[0] - self.maze_surface_width) // 2 + 5,
            506,
            self.UI_text_font1,
            WHITE,
            'center'
        )

    def draw_title(self):
        draw_text(
            self.game.screen,
            self.title,
            SCREEN_WIDTH // 2,
            self.maze_surface_pos[1] // 2 + 4,
            self.title_text_font,
            self.title_colour,
            'center'
        )

    def draw_speed_multiplier(self):
        draw_text(
            self.game.screen,
            f'Speed: {self.speed_multiplier[self.animation_delay]}',
            self.maze_surface_pos[0] + self.maze_surface_width,
            self.maze_surface_pos[1] + self.maze_surface_height,
            self.UI_text_font2,
            WHITE,
            'topright'
        )

# Code execution
new_game = Game()
new_game.run()