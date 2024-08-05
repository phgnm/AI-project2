import pygame

class agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.image = pygame.image.load('../assets/images/flower.png').convert()
        self.y = 40 + (x - 1) * 70
        self.x = 40 + (y - 1) * 70
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.spacing = 70
        self.i = x - 1
        self.j = y - 1