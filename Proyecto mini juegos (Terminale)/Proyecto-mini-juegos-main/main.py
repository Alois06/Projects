import pygame
import sys

import game_tennis
import game_shots
from menu import Menu_Principal, Menu_2players, Menu_Solo
from sound import sound

#initialisation du module pygame
pygame.init()
pygame.font.init()

#création de la fenêtre de jeu
dimensions = (1080, 720)
pygame.display.set_caption("Multi Game")
screen = pygame.display.set_mode(dimensions)

#création de l'objet qui va permettre de gérer le temps
time = pygame.time.Clock()

#création des polices
police1 = pygame.font.Font("assets/polices/good timing bd.ttf", 30)
police2 = pygame.font.Font("assets/polices/good timing bd.ttf", 27)
police3 = pygame.font.Font("assets/polices/DigitalDream.ttf", 30)
police4 = pygame.font.Font("assets/polices/Pixel Digivolve.otf", 50)
police3.bold = True

#image de fond d'écran
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, dimensions)

#son
sound.change_volume()
sound.background_music.play(loops=-1)

#création des classes des différents menus
menu = Menu_Principal(screen, police1, police2)
menu_solo = Menu_Solo(screen, police1, police2)
menu_2players = Menu_2players(screen, police1, police2)

#création des classes des jeux du mode solo
game_tennis_solo = game_tennis.GameSolo(screen, police1, police2, police3, police4)
game_shots_solo = game_shots.GameSolo(screen, police1, police2, police3, police4)

#création des classes des jeux du mode multijoueurs
game_tennis_multiplayer = game_tennis.Game(screen, police1, police2, police3, police4)
game_shots_multiplayer = game_shots.Game(screen, police1, police2, police3, police4)

#DEBUT DE LA BOUCLE DE JEU

game_on = True

while game_on : 

    #efface l'arrière plan
    screen.fill(0)

    #boucle qui gère les évènements (mouvements et clics de souris, appuis de bouton, etc)
    for event in pygame.event.get() :

        #quitte la fenêtre
        if event.type == pygame.QUIT : 
            game_on = False

        #vérifie si un bouton est appuyé
        if event.type == pygame.MOUSEBUTTONDOWN :
            
            #menu principal
            if menu.etat : 
                #bouton solo
                if menu.button_play_solo.click() :
                    menu.unset()
                    menu_solo.set()
                #bouton multijoueur
                elif menu.button_play_2_players.click():
                    menu.unset()
                    menu_2players.set()
            
            #menu solo
            elif menu_solo.etat : 
                #jeu de raquettes
                if menu_solo.button_game1.click() :
                    menu_solo.unset()
                    game_tennis_solo = game_tennis.GameSolo(screen, police1, police2, police3, police4)
                    game_tennis_solo.set()
                #jeu de tirs
                elif menu_solo.button_game2.click() : 
                    menu_solo.unset()
                    game_shots_solo = game_shots.GameSolo(screen, police1, police2, police3, police4)
                    game_shots_solo.set()
                #retour au menu principal
                elif menu_solo.button_return.click() :
                    menu_solo.unset()
                    menu.set()

            #menu multijoueur
            elif menu_2players.etat : 
                #jeu de raquettes
                if menu_2players.button_game1.click() :
                    menu_2players.unset()
                    game_tennis_multiplayer = game_tennis.Game(screen, police1, police2, police3, police4)
                    game_tennis_multiplayer.set()
                #jeu de tirs
                elif menu_2players.button_game2.click() : 
                    menu_2players.unset()
                    game_shots_multiplayer = game_shots.Game(screen, police1, police2, police3, police4)
                    game_shots_multiplayer.set()
                #retour au menu principal
                elif menu_2players.button_return.click() :
                    menu_2players.unset()
                    menu.set()

        #évènements pour les jeux de tennis
        elif game_tennis_solo.etat : 
            game_tennis_solo.manage_events(event)

        elif game_tennis_multiplayer.etat :
            game_tennis_multiplayer.manage_events(event)

        #évènements pour les jeux de tirs
        elif game_shots_solo.etat : 
            game_shots_solo.manage_events(event)

        elif game_shots_multiplayer.etat :
            game_shots_multiplayer.manage_events(event)

    #affichage de l'image d'arrière plan
    screen.blit(background, (0, 0))

    #affichage des éléments du menu/jeu en cours
    if menu.etat :
        menu.draw()

    elif menu_solo.etat :
        menu_solo.draw()

    elif menu_2players.etat : 
        menu_2players.draw()

    elif game_tennis_solo.etat :
        game_tennis_solo.apply() 
        game_tennis_solo.draw()
        if game_tennis_solo.etat == False :
            menu.set()

    elif game_tennis_multiplayer.etat :
        game_tennis_multiplayer.apply() 
        game_tennis_multiplayer.draw()
        if game_tennis_multiplayer.etat == False :
            menu.set()

    elif game_shots_solo.etat : 
        game_shots_solo.apply()
        game_shots_solo.draw()
        if game_shots_solo.etat == False : 
            menu.set()

    elif game_shots_multiplayer.etat : 
        game_shots_multiplayer.apply()
        game_shots_multiplayer.draw()
        if game_shots_multiplayer.etat == False : 
            menu.set()

    #actualisation de l'écran
    pygame.display.flip()
    time.tick(30) #fait trourner le jeu à 30 fps

#quitte la fenêtre de jeu pygame et met fin au programme
pygame.quit()
sys.exit()