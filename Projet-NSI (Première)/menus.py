import pygame
import sys
import time
import random
from button import Button
from sound import sound
from player import Player

#menu principal
class Menu :
    def __init__(self, dimensions, police, screen) :
        self.screen = screen

        #arrière plan
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, dimensions)
        self.background_coords = (0,0)

        #affichage ou non
        self.etat = True

        #création des boutons
        self.img_buttons = pygame.image.load("assets/buttons.png")

        #bouton play
        self.image_button_play = police.render("Play", True, (255, 255, 255))
        self.button_play = Button(self.image_button_play, (180, 190), self.screen)

        #bouton levels
        self.image_button_levels = police.render("Levels", True, (255, 255, 255))
        self.button_levels = Button(self.image_button_levels, (180, 310), self.screen)

        #bouton changement de joueur et d'arme
        self.image_button_arsenal = police.render("Players", True, (255, 255, 255))
        self.button_arsenal = Button(self.image_button_arsenal, (180, 430), self.screen)

        #bouton paramètres
        self.image_button_settings = police.render("Settings", True, (255, 255, 255))
        self.button_settings = Button(self.image_button_settings, (180, 550), self.screen)
    
    #met en place le menu principal
    def set(self) :
        self.etat = True
        self.background_coords = (0,0)
        self.button_play.move((180, 190))
        self.button_levels.move((180, 310))
        self.button_arsenal.move((180, 430))
        self.button_settings.move((180, 550))
    
    #affiche tous les éléments du menu principal
    def draw(self) :
        self.screen.blit(self.background, self.background_coords)
        self.button_play.draw()
        self.button_levels.draw()
        self.button_arsenal.draw()
        self.button_settings.draw()
    
    def erase(self) :
        self.etat = False

#menu pour choisir le niveau
class Menu_levels :
    def __init__(self, dimensions, police, screen) :
        self.screen = screen

        #arrière plan
        self.background = pygame.image.load("assets/background_wall.jpeg")
        self.background = pygame.transform.scale(self.background, dimensions)
        self.background_coords = (0,0)

        #affichage ou non
        self.etat = False

        #création des boutons
        self.img_buttons1 = pygame.image.load("assets/buttons.png")
        self.img_buttons2 = pygame.image.load("assets/buttons.png")
        self.img_buttons3 = pygame.image.load("assets/buttons.png")
        self.img_buttons4 = pygame.image.load("assets/buttons.png")

        self.img_cadenas = pygame.image.load("assets/cadenas.png")
        self.img_cadenas = pygame.transform.scale_by(self.img_cadenas, 0.233)
        self.cadenas_rect = self.img_cadenas.get_rect()

        #bouton level 1
        self.text_button_level1 = police.render("LEVEL 1", True, (255, 255, 255))
        self.image_button_level1 = self.img_buttons1.subsurface(500, 150, 150, 75)
        self.image_button_level1.blit(self.text_button_level1, (37, 27))
        self.button_level1 = Button(self.image_button_level1, (540, 240), self.screen)
        
        #bouton level 2
        self.text_button_level2 = police.render("LEVEL 2", True, (255, 255, 255))
        self.image_button_level2 = self.img_buttons2.subsurface(500, 150, 150, 75)
        self.image_button_level2.blit(self.text_button_level2, (37, 27))
        self.button_level2 = Button(self.image_button_level2, (540, 360), self.screen)
        
        #bouton level 3
        self.text_button_level3 = police.render("LEVEL 3", True, (255, 255, 255))
        self.image_button_level3 = self.img_buttons3.subsurface(500, 150, 150, 75)
        self.image_button_level3.blit(self.text_button_level3, (37, 27))
        self.button_level3 = Button(self.image_button_level3, (540, 480), self.screen)
        
        #bouton retour vers le menu
        self.text_button_return = police.render("Back", True, (255, 255, 255))
        self.image_button_return = self.img_buttons4.subsurface(500, 20, 150, 75)
        self.image_button_return.blit(self.text_button_return, (50, 30))
        self.button_return = Button(self.image_button_return, (200, 600), self.screen) 

        #états de chaque level :
        self.level1 = {"unlock" : True,
                       "achieve" : False}
        
        self.level2 = {"lock" : True,
                       "unlock" : False,
                       "achieve" : False}
        
        self.level3 = {"lock" : True,
                       "unlock" : False,
                       "achieve" : False}
    
    #met en place le menu pour choisir un level
    def set(self) :
        self.etat = True
        self.background_coords = (0,0)
        self.button_level1.move((540, 240))
        self.button_level2.move((540, 360))
        self.button_level3.move((540, 480))
        self.button_return.move((200, 600))
    
    #affiche tous les éléments du menu
    def draw(self) :
        #afficher le fond d'écran
        self.screen.blit(self.background, self.background_coords)

        #afficher les boutons des levels
        self.button_level1.draw()
        self.button_level2.draw()
        self.button_level3.draw()

        self.lock() #afficher un cadenas sur les boutons des levels bloqués

        #affichage du bouton de retour
        self.button_return.draw()
    
    def erase(self) :
        self.etat = False

    #affiche un cadenas sur les levels bloqués
    def lock(self) :
        if self.level2["lock"] == True :
            self.cadenas_rect.center = self.button_level2.rect.center
            self.screen.blit(self.img_cadenas, self.cadenas_rect)

        if self.level3["lock"] == True :
            self.cadenas_rect.center = self.button_level3.rect.center
            self.screen.blit(self.img_cadenas, self.cadenas_rect)
    
    #actualise les états de chaque level en fonction de si un level a été réussi ou non
    def update(self) :
        if self.level1["achieve"] == True :
            self.level2["lock"] = False
            self.level2["unlock"] = True

        if self.level2["achieve"] == True :
            self.level3["lock"] = False
            self.level3["unlock"] = True
            

#menu pour changer de personnage et d'arme
class Armuererie :
    def __init__(self, dimensions, police, screen, players, weapons) :
        self.screen = screen
        
        #arrière plan
        self.background = pygame.image.load("assets/background_wall.jpeg")
        self.background = pygame.transform.scale(self.background, dimensions)
        self.background_coords = (0,0)
        
        #affichage ou non
        self.etat = False
        
        #création des boutons
        self.img_buttons = pygame.image.load("assets/buttons.png")
        self.img_buttons_left = self.img_buttons.subsurface(660, 10, 70, 90)
        self.img_buttons_right = self.img_buttons.subsurface(730, 10, 70, 90)
        
        #bouton retour vers le menu principal
        self.text_button_return = police.render("Back", True, (255, 255, 255))
        self.image_button_return = self.img_buttons.subsurface(500, 20, 150, 75)
        self.image_button_return.blit(self.text_button_return, (50, 30))
        self.button_return = Button(self.image_button_return, (200, 600), self.screen)
        
        #bouton player
        self.button_player_0 = Button(self.img_buttons_left, (300, 200), self.screen)
        self.button_player_1 = Button(self.img_buttons_right, (780, 200), self.screen)
        
        #bouton weapon
        self.button_weapon_0 = Button(self.img_buttons_left, (300, 520), self.screen)
        self.button_weapon_1 = Button(self.img_buttons_right, (780, 520), self.screen)
        
        #players et weapons
        self.weapons = weapons
        self.players = players
        self.current_weapon = weapons[0]
        self.current_player = players[0]
        self.current_player_coords = (500, 150)
        self.current_weapon_coords = (500, 500)

        self.player_index = 0
        self.weapon_index = 0
    
    #met en place le menu pour changer de personnage et d'arme
    def set(self) :
        self.etat = True
        self.background_coords = (0,0)
        self.current_player_coords = (500, 150)
        self.current_weapon_coords = (500, 500)
        #met les boutons aux bonnes positions
        self.button_return.move((200, 600))
        self.button_player_0.move((300, 200))
        self.button_player_1.move((780, 200))
        self.button_weapon_0.move((300, 520))
        self.button_weapon_1.move((780, 520))
    
    #affiche tous les éléments du menu
    def draw(self) :
        #afficher le fond d'écran
        self.screen.blit(self.background, self.background_coords)
        #afficher les boutons
        self.button_return.draw()
        self.button_player_0.draw()
        self.button_player_1.draw()
        self.button_weapon_0.draw()
        self.button_weapon_1.draw()
        #afficher l'image du personnage et de l'arme actuel
        img_player = self.current_player["img"]
        img_player = pygame.transform.scale(img_player, (78, 96))
        img_weapon = self.current_weapon["img"]
        img_weapon = pygame.transform.scale_by(img_weapon, 3.0)
        self.screen.blit(img_player, self.current_player_coords)
        self.screen.blit(img_weapon, self.current_weapon_coords)
    
    def erase(self) :
        self.etat = False
    
    #permet de changer de personnage en ajoutant +1 ou -1 à l'index du personnage
    def change_player(self, i) :
        self.player_index += i
        index = self.player_index%len(self.players)
        self.current_player = self.players[index]
    
    #permet de changer d'arme en ajoutant +1 ou -1 à l'index de l'arme
    def change_weapon(self, i) :
        self.weapon_index += i
        index = self.weapon_index%len(self.weapons)
        self.current_weapon = self.weapons[index]

    #retourne un objet de type Player à partir du personnage actuel
    def return_current_player(self) :
        img_player = self.current_player["img"]
        img_player = pygame.transform.scale_by(img_player, 1.5)
        player = Player(self.screen, (0, 0), img_player, self.current_player["images"], self.current_player["properties"], self.current_player["tables"])
        return player

    #retourne un objet Weapon (Gun, Bow ou Sword) à partir de l'arme actuelle
    def return_current_weapon(self) :  
        weapon = self.current_weapon["type"](self.screen, (590, 370), self.current_weapon["properties"])
        return weapon

#menu pour changer les paramètres
class Settings :
    def __init__(self, dimensions, police, screen, settings_liste) :
        self.screen = screen
        self.settings = settings_liste
        
        #arrière plan
        self.background = pygame.image.load("assets/background_wall.jpeg")
        self.background = pygame.transform.scale(self.background, dimensions)
        self.background_coords = (0,0)
        
        #affichage ou non
        self.etat = False

        self.police = police
        
        #création des boutons
        self.img_buttons = pygame.image.load("assets/buttons.png")
        self.img_buttons2 = pygame.image.load("assets/buttons.png")
        self.img_buttons3 = pygame.image.load("assets/buttons.png")
        self.img_buttons4 = pygame.image.load("assets/buttons.png")
        self.img_buttons_left = self.img_buttons.subsurface(660, 10, 70, 90)
        self.img_buttons_right = self.img_buttons.subsurface(730, 10, 70, 90)

        #bouton retour vers le menu principal
        self.text_button_return = police.render("Back", True, (255, 255, 255))
        self.image_button_return = self.img_buttons.subsurface(500, 20, 150, 75)
        self.image_button_return.blit(self.text_button_return, (50, 30))
        self.button_return = Button(self.image_button_return, (200, 600), self.screen)

        #bouton difficulté
        self.text_button_difficulty = police.render("Difficulty", True, (255, 255, 255))
        self.image_button_difficulty = self.img_buttons2.subsurface(500, 150, 150, 75)
        self.image_button_difficulty.blit(self.text_button_difficulty, (20, 25))
        self.button_difficulty = Button(self.image_button_difficulty, (540, 55), self.screen)
        #bouton < difficulté
        self.image_button_inferior = police.render("<", True, (255, 255, 255))
        self.button_inferior = Button(self.img_buttons_left, (380, 155), self.screen)
        #bouton > difficulté
        self.image_button_superior = police.render(">", True, (255, 255, 255))
        self.button_superior = Button(self.img_buttons_right, (700, 155), self.screen)
        #3 types of difficulty
        self.difficulty = self.settings["difficulty"]
        self.current_difficulty = self.settings["difficulty"][0]
        self.image_difficulty = police.render(self.current_difficulty, True, (255, 255, 255))

        #bouton son
        self.text_button_sound = police.render("Sound", True, (255, 255, 255))
        self.image_button_sound = self.img_buttons3.subsurface(500, 150, 150, 75)
        self.image_button_sound.blit(self.text_button_sound, (40, 25))
        self.button_sound = Button(self.image_button_sound, (540, 255), self.screen)
        #bouton < son
        self.image_button_inferior_son = police.render("<", True, (255, 255, 255))
        self.button_inferior_son = Button(self.img_buttons_left, (380, 355), self.screen)
        #bouton > son
        self.image_button_superior_son = police.render(">", True, (255, 255, 255))
        self.button_superior_son = Button(self.img_buttons_right, (700, 355), self.screen)
        #2 types of sound
        self.sound = self.settings["sound"]
        self.current_sound = self.settings["sound"][0]
        self.image_sound = police.render(self.current_sound, True, (255, 255, 255))
       
        #bouton gameplay
        self.text_button_gp = police.render("Gameplay", True, (255, 255, 255))
        self.image_button_gp = self.img_buttons4.subsurface(500, 150, 150, 75)
        self.image_button_gp.blit(self.text_button_gp, (23, 25))
        self.button_gp = Button(self.image_button_gp, (540, 355), self.screen)
        #bouton < gameplay
        self.image_button_inferior_gp = police.render("<", True, (255, 255, 255))
        self.button_inferior_gp = Button(self.img_buttons_left, (380, 555), self.screen)
        #bouton > gameplay
        self.image_button_superior_gp = police.render(">", True, (255, 255, 255))
        self.button_superior_gp = Button(self.img_buttons_right, (700, 555), self.screen)
        #3 types of gameplay
        self.gp = self.settings["jouabilité"]
        self.current_gp = self.settings["jouabilité"][0]
        self.image_gp = police.render(self.current_gp[0], True, (255, 255, 255))
       
        #index
        self.liste_index_difficulty = 0
        self.liste_index_sound = 0 
        self.liste_index_gp = 0  

    #met en place le menu des paramètres
    def set(self) :
        self.etat = True
        self.background_coords = (0,0)
        self.button_return.move((200, 600))
        self.button_difficulty.move((540, 55))
        self.button_inferior.move((380, 155))
        self.button_superior.move((700, 155))
        self.button_sound.move((540, 255))
        self.button_inferior_son.move((380, 355))
        self.button_superior_son.move((700, 355))
        self.button_gp.move((540, 455))
        self.button_inferior_gp.move((380, 555))
        self.button_superior_gp.move((700, 555))
    
    #affiche tous les éléments du menu des paramètres
    def draw(self) :
        self.screen.blit(self.background, self.background_coords)
        self.image_difficulty = self.police.render(self.current_difficulty, True, (255, 255, 255))
        self.image_sound = self.police.render(self.current_sound, True, (255, 255, 255))
        self.image_gp = self.police.render(self.current_gp[0], True, (255, 255, 255))
        self.screen.blit(self.image_difficulty, (515,145))
        self.screen.blit(self.image_sound, (498,345))
        self.screen.blit(self.image_gp, (505,545))
        self.button_return.draw()
        self.button_difficulty.draw()
        self.button_inferior.draw()
        self.button_superior.draw()
        self.button_sound.draw()
        self.button_inferior_son.draw()
        self.button_superior_son.draw()
        self.button_gp.draw()
        self.button_inferior_gp.draw()
        self.button_superior_gp.draw()
    
    def erase(self) :
        self.etat = False

    #permet de changer la difficulté
    def change_difficulty(self, i) :
        self.liste_index_difficulty += i
        index = self.liste_index_difficulty%len(self.difficulty)
        self.current_difficulty = self.difficulty[index]

    #permet d'activer ou désactiver le son
    def change_sound(self, i) :
        self.liste_index_sound += i
        index = self.liste_index_sound%len(self.sound)
        self.current_sound = self.sound[index]
        sound.change_volume()

    #permet de changer les commandes de jeu (zqsd pour azerty, wasd pour qwerty ou les flèches directionnelles)
    def change_gp(self, i) :
        self.liste_index_gp += i
        index = self.liste_index_gp%len(self.gp)
        self.current_gp = self.gp[index]
    
    #retourne un dictionnaire dans lequel chaque clé renvoie à son paramètre actuel
    def return_settings(self) :
        return {
            "difficulty" : self.current_difficulty,
            "sound" : self.current_sound,
            "jouabilité" : self.current_gp
        }
