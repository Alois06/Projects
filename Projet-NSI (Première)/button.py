import pygame
from sound import sound

class Button :
    def __init__(self, img, coords, screen) :
        self.img = img
        self.rect = self.img.get_rect() #ajoute une version de l'image en rectangle
        self.rect.center = coords #met le bouton aux coordonnées (x, y)
        self.screen = screen
        self.coords_init = coords
    def move(self, coords) :
        self.rect.center = coords
    def draw(self) :
        self.screen.blit(self.img, (self.rect.x, self.rect.y)) #dessine l'image du bouton aux coordonnés du rectangle associé
    def click(self) : #fonction qui vérifie si le bouton a été cliqué : si c'est le cas, alors elle renvoie True et lance un son de clic
        pos_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_mouse) :
            if pygame.mouse.get_pressed()[0] :
                sound.select_sound.play()
                return True
            else : return False
        else :
            return False
