import pygame

from button import Button

#Classe mère Menu 
class Menu : 
    def __init__(self, screen, police1, police2) -> None:
        self.screen = screen

        self.etat = False

        #boutons
        self.img_button = pygame.image.load("assets/boutons.png")
        self.img_button = self.img_button.convert_alpha().subsurface((370, 280, 220, 110))

        #bouton retour
        img_return_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_return_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_return_1.blit(police1.render("Back", False, 0), (76, 32))
        img_return_2.blit(police2.render("Back", False, 0), (68, 28))

        self.button_return = Button(screen, [img_return_1, img_return_2], (100, 650))

    #Ouvre le menu
    def set(self) :
        self.etat = True

    #Quitte le menu
    def unset(self) :
        self.etat = False

    #Affiche les éléments du menu
    def draw(self) :
        pass


#Menu principal
class Menu_Principal(Menu) : 
    def __init__(self, screen, police1, police2) -> None :

        super().__init__(screen, police1, police2)

        self.set()

        #bouton solo
        img_solo_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_solo_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_solo_1.blit(police1.render("Solo", False, 0), (76, 32))
        img_solo_2.blit(police2.render("Solo", False, 0), (68, 28))

        self.button_play_solo = Button(screen, [img_solo_1, img_solo_2], (540, 300))
        
        #bouton multiplayer
        img_multiplayer_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_multiplayer_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_multiplayer_1.blit(police1.render("Multiplayer", False, 0), (27, 32))
        img_multiplayer_2.blit(police2.render("Multiplayer", False, 0), (24, 28))

        self.button_play_2_players = Button(screen, [img_multiplayer_1, img_multiplayer_2], (540, 450))

    #Affiche les éléments du menu
    def draw(self) : 
        self.button_play_solo.apply()
        self.button_play_2_players.apply()


#Menu pour choisir un jeu en mode solo (1 vs IA)
class Menu_Solo(Menu) :
    def __init__(self, screen, police1, police2) -> None:
        
        super().__init__(screen, police1, police2)

        #boutons des parties

        #bouton du premier jeu (tennis)
        img_game1_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_game1_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_game1_1.blit(police1.render("Tennis", False, 0), (60, 32))
        img_game1_2.blit(police2.render("Tennis", False, 0), (56, 28))

        self.button_game1 = Button(screen, [img_game1_1, img_game1_2], (350, 350))

        #bouton du deuxième jeu (shots)
        img_game2_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_game2_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_game2_1.blit(police1.render("Shoots", False, 0), (60, 32))
        img_game2_2.blit(police2.render("Shoots", False, 0), (56, 28))

        self.button_game2 = Button(screen, [img_game2_1, img_game2_2], (720, 350))

    #Affiche les éléments du menu
    def draw(self) :
        self.button_game1.apply()
        self.button_game2.apply()
        self.button_return.apply()


#Menu pour choisir un jeu en mode multijoueur (1 vs 1)
class Menu_2players(Menu) : 
    def __init__(self, screen, police1, police2) -> None:
        
        super().__init__(screen, police1, police2)

        #boutons des parties

        #bouton du premier jeu (tennis)
        img_game1_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_game1_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_game1_1.blit(police1.render("Tennis", False, 0), (60, 32))
        img_game1_2.blit(police2.render("Tennis", False, 0), (56, 28))

        self.button_game1 = Button(screen, [img_game1_1, img_game1_2], (350, 350))

        #bouton du deuxième jeu (shots)
        img_game2_1 = pygame.transform.scale_by(self.img_button.copy(), 1.0)
        img_game2_2 = pygame.transform.scale_by(self.img_button.copy(), 0.90)

        img_game2_1.blit(police1.render("Shoots", False, 0), (60, 32))
        img_game2_2.blit(police2.render("Shoots", False, 0), (56, 28))

        self.button_game2 = Button(screen, [img_game2_1, img_game2_2], (720, 350))

    #Affiche les éléments du menu
    def draw(self) :
        self.button_game1.apply()
        self.button_game2.apply()
        self.button_return.apply()

