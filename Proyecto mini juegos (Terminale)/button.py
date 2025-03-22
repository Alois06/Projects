import pygame
from sound import sound

class Button :
    def __init__(self, screen, images, coords) : 
        self.screen = screen

        #création de l'image et du rectangle du bouton
        self.images = images
        self.image = images[0]
        self.rect = self.images[1].get_rect()
        self.rect.center = coords
        self.rect_img = self.image.get_rect()
        self.rect_img.center = coords

    def apply(self) :
        self.change_image()
        self.draw()

    #Bouge le bouton aux coordonnées données en paramètres
    def move(self, coords) :
        self.rect.center = coords
        self.rect_img = self.rect.center

    #Affiche le bouton sur l'écran
    def draw(self) :
        self.screen.blit(self.image, self.rect_img)

    #Vérifie si le bouton est appuyé ou pas
    def click(self) : 
        if self.rect.collidepoint(pygame.mouse.get_pos()) :
            if pygame.mouse.get_pressed()[0] :
                sound.select_sound.play()
                return True
        return False
    
    #Change l'image si le bouton est appuyé
    def change_image(self) : 
        if self.rect.collidepoint(pygame.mouse.get_pos()) :
            self.image = self.images[1]
        else : 
            self.image = self.images[0]

        self.rect_img = self.image.get_rect()
        self.rect_img.center = self.rect.center
