import pygame
from tools import *

class Projectile(pygame.sprite.Sprite) : 
    def __init__(self, image, coords, direction, collisions) :
        super().__init__()
        self.x = direction[0]
        self.y = direction[1]
        angle = get_angle(self.x, self.y)
        self.image = image
        self.image = pygame.transform.rotate(self.image, angle) 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = coords
        self.coords = coords
        self.i = 0

        #pour éviter que le projectile soit immédiatement stoppé par un mur
        if self.rect.collidelist(collisions) > -1 :
            self.move()

    #exécute le déplacement du projectile
    def move(self) :
        self.i += 1
        self.rect.center = (self.coords[0] + self.i*self.x, self.coords[1] + self.i*self.y)