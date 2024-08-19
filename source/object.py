import pygame

class Pit:
    def __init__(self, x, y):
        self.image = pygame.image.load('../assets/images/pit.png')
        self.image = pygame.transform.scale(self.image, (150, 300))
        self.is_discovered = None
        self.size = 10
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.pit_pos = [[False for i in range(self.size)] for j in range(self.size)]
        for i in range(len(x)):
            print(x[i], y[i])
            self.pit_pos[x[i]][y[i]] = True

    def pit_discovered(self):
        self.is_discovered = True

    def pit_notification(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.pit_pos[i][j]:
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def update(self, screen, font, is_discovered):
            for i in range(self.size):
                for j in range(self.size):
                    if self.noti[i][j] and is_discovered[i][j]:
                        
                        text = font.render('Breeze', True, (0, 0, 0))
                        textRect = text.get_rect()
                        textRect.center = (42 + j * 70, 40 + i * 70)
                        screen.blit(text, textRect)
                        pygame.display.update()
    
class Wumpus:
    def __init__(self, x, y):
        self.image = pygame.image.load('../assets/images/wumpus_alive.png').convert()
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.size = 10
        self.pos = (835, 100)
        self.is_discovered = None
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.wumpus_pos = [[False for i in range(self.size)] for j in range(self.size)]
        for i in range(len(x)):
            self.wumpus_pos[x[i]][y[i]] = True
        
    def wumpus_kill_notif(self, screen, font):
        self.image = pygame.image.load('../assets/images/wumpus_dead.png').convert()
        text = font.render('A wumpus is killed!', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        screen.blit(self.image, (800,200))
        pygame.display.update()
    
    def wumpus_notification(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.wumpus_pos[i][j]:
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def wumpus_killed_notification(self, i, j):
        self.wumpus_pos[i][j] = False
        if i > 0:
            self.noti[i - 1][j] = False
        if i < self.size - 1:
            self.noti[i + 1][j] = False
        if j > 0:
            self.noti[i][j - 1] = False
        if j < self.size - 1:
            self.noti[i][j + 1] = False

    def update(self, screen, font, is_discovered):
        for i in range(self.size):
            for j in range (self.size):
                if self.noti[i][j] and is_discovered[i][j]:
                    text = font.render('Stench', True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (45 + j * 70, 30 + i * 70)
                    screen.blit(text, textRect)
                    pygame.display.update()

    def stench_found(self, i, j):
        return self.noti[i][j]
    
class Gold:
    def __init__(self):
        self.image = pygame.image.load('../assets/images/gold.png')
        self.image = pygame.transform.scale(self.image, (150, 300))
        self.pos = (835, 100)
    
    def grab_gold(self, screen, font):
        text = font.render('You found gold!', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        screen.blit(self.image, (750, 200))
        text = font.render('Score + 5000', True, (0, 0, 0))
        textRect.center = (900, 600)
        screen.blit(text, textRect)
        pygame.display.update()

class Gas:
    def __init__(self, x, y):
        self.image = pygame.image.load('../assets/images/gas.png').convert()
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.size = 10
        self.pos = (835, 100)
        self.is_discovered = None
        self.noti = [[False for i in range(self.size)] for j in range(self.size)]
        self.gas_pos = [[False for i in range(self.size)] for j in range(self.size)]
        for i in range(len(x)):
            self.gas_pos[x[i]][y[i]] = True
    
    def grab_poison(self, screen, font):
        text = font.render('You sniffed poisonous gas!', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        screen.blit(self.image, (750, 200))
        text = font.render('Health - 25', True, (0, 0, 0))
        textRect.center = (900, 600)
        screen.blit(text, textRect)
        pygame.display.update()

    def gas_discovered(self):
        self.is_discovered = True

    def gas_notification(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.gas_pos[i][j]:
                    if i > 0:
                        self.noti[i - 1][j] = True
                    if i < self.size - 1:
                        self.noti[i + 1][j] = True
                    if j > 0:
                        self.noti[i][j - 1] = True
                    if j < self.size - 1:
                        self.noti[i][j + 1] = True

    def update(self, screen, font, is_discovered):
        for i in range(self.size):
            for j in range (self.size):
                if self.noti[i][j] and is_discovered[i][j]:
                    text = font.render('Whiff', True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (45 + j * 70, 30 + i * 70)
                    screen.blit(text, textRect)
                    pygame.display.update()

class Potion:
    def __init__(self):
        self.image = pygame.image.load('../assets/images/potion.png')
        self.image = pygame.transform.scale(self.image, (150, 300))
        self.pos = (835, 100)
    
    def grab_potion(self, screen, font):
        text = font.render('You found potion!', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        screen.blit(self.image, (750, 200))
        pygame.display.update()
    
    def use_potion(self, screen, font):
        text = font.render('Potion used', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = self.pos
        screen.blit(text, textRect)
        pygame.display.update()

class Arrow:
    def __init__(self):
        self.img_list = []
        direction = ['left', 'down', 'right', 'up']
        for i in range(0, 4):
            filename = f'../assets/images/arrow_{direction[i]}.png'
            img = pygame.image.load(filename).convert()
            self.img_list.append(img)

    def shoot(self, direct, screen, y, x):
        if direct == 0:
            self.shoot_left(screen, x, y)
        elif direct == 1:
            self.shoot_down(screen, x, y)
        elif direct == 2:
            self.shoot_right(screen, x, y)
        elif direct == 3:
            self.shoot_up(screen, x, y)

    def shoot_left(self, screen, x, y):
        x = 10 + (x - 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[0], (x, y))
        pygame.display.update()
    
    def shoot_down(self, screen, x, y):
        x = 10 + x * 70
        y = 10 + (y + 1) * 70
        screen.blit(self.img_list[1], (x, y))
        pygame.display.update()

    def shoot_right(self, screen, x, y):
        x = 10 + (x + 1) * 70
        y = 10 + y * 70
        screen.blit(self.img_list[2], (x, y))
        pygame.display.update()

    def shoot_up(self, screen, x, y):
        x = 10 + x * 70
        y = 10 + (y - 1) * 70
        screen.blit(self.img_list[3], (x, y))
        pygame.display.update()