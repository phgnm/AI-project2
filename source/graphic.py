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
        self.potion = None
        self.wumpus = None
        self.pit = None
        self.gas = None
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

    def win_draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))

        if self.state == 'win':
            text = self.victory.render('CONGRATULATIONS', True, BLACK)
        elif self.state == 'try':
            text = self.victory.render('BETTER LUCK NEXT TIME', True, BLACK)
        
        textRect = text.get_rect()
        textRect.center = (500, 50)
        self.screen.blit(text, textRect)
        score = self.agent.get_score()
        text = self.victory.render('Your score: ' + str(score), True, BLACK)
        textRect.center = (450, 100)
        self.screen.blit(text, textRect)

    def win_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.delay(200)
        self.state = 'map'

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
                map_pos = cave_cell.map_pos
                
                self.map = Map((len(cell_matrix) - map_pos[1] + 1, map_pos[0]))
                self.arrow = Arrow()
                self.gold = Gold()
                self.potion = Potion()
                self.agent = agent(len(cell_matrix) - map_pos[1] + 1, map_pos[0])
                self.agent.load_image()
                self.all_sprites = pygame.sprite.Group()
                self.all_sprites.add(self.agent)
                
                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_pit():
                            x.append(ir)
                            y.append(ic)
                self.pit = Pit(x, y)
                self.pit.pit_notification()

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_wumpus():
                            x.append(ir)
                            y.append(ic)
                self.wumpus = Wumpus(x, y)
                self.wumpus.wumpus_notification()

                x = []
                y = []
                for ir in range(len(cell_matrix)):
                    for ic in range(len(cell_matrix)):
                        if cell_matrix[ir][ic].exist_poison():
                            x.append(ir)
                            y.append(ic)
                self.poison = Gas(x, y)
                self.poison.gas_notification()

                self.game_draw()

                for action in action_list:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    self.display_action(action)
                    pygame.display.flip()

                    self.clock.tick(30)

                    if action == Algorithms.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD:
                        self.state = 'win'
                    
                    if action == Algorithms.Action.FALL_INTO_PIT or action == Algorithms.Action.BE_EATEN_BY_WUMPUS or action == Algorithms.Action.DIE_OF_GAS:
                        self.state = 'gameover'
                        break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            elif self.state == 'win' or self.state == 'try':
                self.win_draw()
                self.win_event()

            self.clock.tick(60)
    def display_action(self, action: Algorithms.Action):
        if action == Algorithms.Action.TURN_LEFT:
            self.direction = self.agent.turn_left()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_DOWN:
            self.direction = self.agent.turn_down()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_RIGHT:
            self.direction = self.agent.turn_right()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.TURN_UP:
            self.direction = self.agent.turn_up()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.MOVE_FORWARD:
            self.agent.move(self.direction)
            i, j = self.agent.get_position()
            self.map.discover_new_cell(i, j)
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
        elif action == Algorithms.Action.GRAB_GOLD:
            self.agent.grab_gold()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            self.gold.grab_gold(self.screen, self.font)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.GRAB_POTION:
            self.agent.grab_potion()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            self.gold.grab_gold(self.screen, self.font)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.SHOOT:
            self.agent.shoot()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            i, j = self.agent.get_position()
            self.arrow.shoot(self.direction, self.screen, i, j)
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.KILL_WUMPUS:
            i, j = self.agent.get_position()
            if self.direction == 0:
                j -= 1
            elif self.direction == 1:
                i += 1
            elif self.direction == 2:
                j += 1
            elif self.direction == 3:
                i -= 1
            self.wumpus.wumpus_killed_notification(i, j)
            self.wumpus.wumpus_notification()
            i, j = self.agent.get_position()
            if not self.wumpus.stench_found(i, j):
                self.wumpus.wumpus_kill_notif(self.screen, self.font)
            temp = self.map.discovered()
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.KILL_NO_WUMPUS:
            pass
        elif action == Algorithms.Action.SNIFF_GAS:
            self.agent.grab_poison()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            self.poison.grab_poison()
            temp = self.map.discovered()
            self.wumpus.update(self.screen, self.noti, temp)
            self.pit.update(self.screen, self.noti, temp)
            self.poison.update(self.screen, self.noti, temp)
            pygame.display.update()
            pygame.time.delay(500)
        elif action == Algorithms.Action.BE_EATEN_BY_WUMPUS:
            self.agent.wumpus_or_pit_or_poison()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.state = 'gameover'
        elif action == Algorithms.Action.FALL_INTO_PIT:
            self.agent.wumpus_or_pit_or_poison()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.state = 'gameover'
        elif action == Algorithms.Action.DIE_OF_GAS:
            self.agent.wumpus_or_pit_or_poison()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
            self.state = 'gameover'
        elif action == Algorithms.Action.HEAL:
            self.agent.use_potion()
            self.all_sprites.update()
            self.game_draw()
            self.potion.use_potion()
            self.all_sprites.draw(self.screen)
            pygame.display.update()
        elif action == Algorithms.Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD:
            self.state = 'win'
            pass
        elif action == Algorithms.Action.CLIMB_OUT_OF_THE_CAVE:
            self.agent.climb()
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            self.map.agent_climb(self.screen, self.font)
            pygame.display.update()
            pygame.time.delay(2000)
        elif action == Algorithms.Action.DETECT_PIT:
            i, j = self.agent.get_position()
            if self.direction == 0:
                j -= 1
            elif self.direction == 1:
                i += 1
            elif self.direction == 2:
                j += 1
            elif self.direction == 3:
                i -= 1
            self.map.pit_detect(i, j)
            self.all_sprites.update()
            self.game_draw()
            self.all_sprites.draw(self.screen)
            pygame.time.delay(1000)
        elif action == Algorithms.Action.DETECT_WUMPUS:
            pass
        elif action == Algorithms.Action.DETECT_NO_PIT:
            pass
        elif action == Algorithms.Action.DETECT_NO_WUMPUS:
            pass
        elif action == Algorithms.Action.DETECT_SAFE:
            pass
        elif action == Algorithms.Action.DETECT_GAS:
            pass
        elif action == Algorithms.Action.DETECT_NO_GAS:
            pass
        elif action == Algorithms.Action.INFER_PIT:
            pass
        elif action == Algorithms.Action.INFER_NOT_PIT:
            pass
        elif action == Algorithms.Action.INFER_WUMPUS:
            pass
        elif action == Algorithms.Action.INFER_NOT_WUMPUS:
            pass
        elif action == Algorithms.Action.INFER_SAFE:
            pass
        elif action == Algorithms.Action.INFER_GAS:
            pass
        elif action == Algorithms.Action.INFER_NOT_GAS:
            pass
        elif action == Algorithms.Action.PERCEIVE_BREEZE:
            pass
        elif action == Algorithms.Action.PERCEIVE_STENCH:
            pass
        elif action == Algorithms.Action.PERCEIVE_GLOW:
            pass
        elif action == Algorithms.Action.PERCEIVE_WHIFF:
            pass
        else:
            raise TypeError("Error: " + self.display_action.__name__)