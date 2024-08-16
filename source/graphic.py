import sys
from agent import *
from map import *
import Algorithms

# Colours definition
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0)

# Buttons definition
LEVEL_1_POS = pygame.Rect(235, 120, 500, 50)
LEVEL_2_POS = pygame.Rect(235, 200, 500, 50)
LEVEL_3_POS = pygame.Rect(235, 280, 500, 50)
LEVEL_4_POS = pygame.Rect(235, 360, 500, 50)
LEVEL_5_POS = pygame.Rect(235, 440, 500, 50)
EXIT_POS = pygame.Rect(235, 520, 500, 50)

#List of maps
MAP_LIST = ['../assets/input/map_1.txt',
            '../assets/input/map_2.txt',
            '../assets/input/map_3.txt',
            '../assets/input/map_4.txt',
            '../assets/input/map_5.txt',]

#List of output files
OUTPUT_LIST = ['../assets/output/output_1.txt',
               '../assets/output/output_2.txt',
               '../assets/output/output_3.txt',
               '../assets/output/output_4.txt',
               '../assets/output/output_5.txt',]
class graphics:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((970, 710))
        self.caption = pygame.display.set_caption("Wumpus World")
        self.clock = pygame.time.Clock()
        self.map = None
        self.agent = None
        self.gold = None
        self.wumpus = None
        self.pit = None
        self.arrow = None
        self.font = pygame.font.Font('../assets/fonts/CenturyGothic.ttf', 30)
        self.noti = pygame.font.Font('../assets/fonts/CenturyGothic.ttf', 15)
        self.victory = pygame.font.Font('../assets/fonts/CenturyGothic.ttf', 50)
        self.all_sprites = pygame.sprite.Group()

        self.state = 'menu'
        self.map_i = 1
        self.mouse = None
        self.background = pygame.image.load('../assets/images/you_win.png').convert()
        self.background = pygame.transform.scale(self.background, (970, 710))
        self.direction = 0

    def draw_button(self, surf, rect, button_colour, text_colour, text):
        pygame.draw.rect(surf, button_colour, rect)
        text_surf = self.font.render(text, True, text_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    def game_draw(self):
        self.screen.fill(WHITE)
        self.map.draw(self.screen)
        score = self.agent.get_score()
        text = self.font.render(f'Your score: {score}', True, BLACK)
        textRect = text.get_rect()
        textRect.center = (820, 25)
        self.screen.blit(text, textRect)

    def home_draw(self):
        self.screen.fill(WHITE)

    def home_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 235 <= self.mouse[0] <= 735 and 120 <= self.mouse[1] <= 170:
                    self.state = 'game'
                    self.map_i = 1
                elif 235 <= self.mouse[0] <= 735 and 200 <= self.mouse[1] <= 250:
                    self.state = 'game'
                    self.map_i = 2
                elif 235 <= self.mouse[0] <= 735 and 280 <= self.mouse[1] <= 330:
                    self.state = 'game'
                    self.map_i = 3
                elif 235 <= self.mouse[0] <= 735 and 360 <= self.mouse[1] <= 410:
                    self.state = 'game'
                    self.map_i = 4
                elif 235 <= self.mouse[0] <= 735 and 440 <= self.mouse[1] <= 490:
                    self.state = 'game'
                    self.map_i = 5
                elif 235 <= self.mouse[0] <= 735 and 520 <= self.mouse[1] <= 570:
                    pygame.quit()
                    sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 235 <= self.mouse[0] <= 735 and 120 <= self.mouse[1] <= 170:
                self.draw_button(self.screen, LEVEL_1_POS, DARK_GREY, RED, "MAP 1")
            else:
                self.draw_button(self.screen, LEVEL_1_POS, LIGHT_GREY, BLACK, "MAP 1")
            if 235 <= self.mouse[0] <= 735 and 200 <= self.mouse[1] <= 250:
                self.draw_button(self.screen, LEVEL_2_POS, DARK_GREY, RED, "MAP 2")
            else:
                self.draw_button(self.screen, LEVEL_2_POS, LIGHT_GREY, BLACK, "MAP 2")
            if 235 <= self.mouse[0] <= 735 and 280 <= self.mouse[1] <= 330:
                self.draw_button(self.screen, LEVEL_3_POS, DARK_GREY, RED, "MAP 3")
            else:
                self.draw_button(self.screen, LEVEL_3_POS, LIGHT_GREY, BLACK, "MAP 3")
            if 235 <= self.mouse[0] <= 735 and 360 <= self.mouse[1] <= 410:
                self.draw_button(self.screen, LEVEL_4_POS, DARK_GREY, RED, "MAP 4")
            else:
                self.draw_button(self.screen, LEVEL_4_POS, LIGHT_GREY, BLACK, "MAP 4")
            if 235 <= self.mouse[0] <= 735 and 440 <= self.mouse[1] <= 490:
                self.draw_button(self.screen, LEVEL_5_POS, DARK_GREY, RED, "MAP 5")
            else:
                self.draw_button(self.screen, LEVEL_5_POS, LIGHT_GREY, BLACK, "MAP 5")
            if 235 <= self.mouse[0] <= 735 and 520 <= self.mouse[1] <= 570:
                self.draw_button(self.screen, EXIT_POS, DARK_GREY, RED, "EXIT")
            else:
                self.draw_button(self.screen, EXIT_POS, LIGHT_GREY, BLACK, "EXIT")
            pygame.display.update()
    
    def run(self):
        while 1:
            if self.state == 'menu':
                self.home_draw()
                self.home_event()
            elif self.state == 'game':
                self.state = 'try'

                action_list, cave_cell, cell_matrix = Algorithms.AgentBrain(MAP_LIST[self.map_i - 1], OUTPUT_LIST[self.map_i - 1]).solve_wumpus_world()
                self.map = Map((len(cell_matrix) - map_pos[i] + 1, map_pos[0]))

                self.agent = agent(len(cell_matrix) - map_pos[i] + 1, map_pos[0])
                self.agent.load_image()
                self.all_sprites = pygame.sprite.Group()
                self.all_sprites.add(self.agent)
                
                self.game_draw()
            else:
                pygame.quit()
                sys.exit()
            self.clock.tick(60)