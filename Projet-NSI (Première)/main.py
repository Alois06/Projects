import pygame
import sys

from menus import *
from game import Game
from weapon import *
import data
from sound import sound
from levels import *

pygame.init() 

logo = pygame.image.load("assets/logo.png") #logo de la fenêtre du jeu

#générer la fenetre du jeu
dimensions = (1080, 720)
pygame.display.set_caption("NIGHT HERO")
pygame.display.set_icon(logo)
screen = pygame.display.set_mode(dimensions)

#variables et constantes
timer = pygame.time.Clock() #timer qui permet de gérer le temps
police_path = "assets/police/police.ttf"
police1 = pygame.font.Font(police_path, 20)
police2 = pygame.font.Font(police_path, 16)
pause = False

#paramètres
settings_liste = data.settings_liste

#armes
player_weapons = data.player_weapons

#personnages
players = data.players

#mise en place des menus, de game et des levels (classes)
menu = Menu(dimensions, police1, screen) #menu principal
menu_levels = Menu_levels(dimensions, police2, screen) #menu pour choisir un level
armurerie = Armuererie(dimensions, police2, screen, players, player_weapons) #menu pour changer d'arme et de personnage
settings = Settings(dimensions, police2, screen, settings_liste) #menu pour changer les paramètres du jeu

game = Game(screen, police1, settings.return_settings()) #partie rapide

level1 = Level1(screen, police1, settings.return_settings()) #level 1
level2 = Level2(screen, police1, settings.return_settings()) #level 2
level3 = Level3(screen, police1, settings.return_settings()) #level 3

games = [game, level1, level2, level3]

#mise en place du menu
menu.set()

#lance la musique
sound.sound_volume_on()
sound.music.play(loops=-1)

#boucle du jeu
game_on = True

while game_on :

    #boucle qui gère les events
    for event in pygame.event.get() :

        #si le joueur ferme la fenetre
        if event.type == pygame.QUIT :
            game_on = False

        #bouton pause
        if event.type == pygame.MOUSEBUTTONDOWN :
            for g in games : #pour chaque partie dans l'ensembe de parties possibles (game, level 1, level2 et level 3)
                if g.etat : #si cette partie est en cours
                    if g.button_pause.click() : #si le bouton pause de cette partie a été cliqué
                        pause = not(pause) #changer la valeur de pause
                        g.pause(pause) #met en pause la partie
                        if pause == True : #si le jeu est mis en pause
                            sound.mvmt_sound.stop() #arrêter le son de marche du joueur
                        break

        if not(pause) :
            #si le joueur appuie sur un bouton
            if event.type == pygame.MOUSEBUTTONDOWN : #si l'event est l'appui d'un des boutons de la souris
                #menu principal
                if menu.etat :
                    if menu.button_play.click() :
                        sound.music.stop()
                        sound.music.play(loops=-1)

                        #efface le menu principal
                        menu.erase()

                        #met en place la partie
                        game = Game(screen, police1, settings.return_settings())
                        games[0] = game
                        game.set(armurerie.return_current_player(), armurerie.return_current_weapon())
 
                    elif menu.button_levels.click() :
                        #efface le menu principal et met en place le menu pour choisir les levels
                        menu.erase()
                        menu_levels.set()
                    
                    elif menu.button_arsenal.click() :
                        #efface le menu principal et met en place le menu pour changer de personnage et d'arme
                        menu.erase()
                        armurerie.set()
                    
                    elif menu.button_settings.click() :
                        #efface le menu principal et met en place le menu pour changer les paramètres
                        menu.erase()
                        settings.set()

                #menu des levels
                if menu_levels.etat :

                    if menu_levels.button_return.click() :
                        #retour au menu
                        menu_levels.erase()
                        menu.set()

                    elif menu_levels.button_level1.click() :

                        #relance la musique
                        sound.music.stop()
                        sound.music.play(loops=-1)

                        #efface le menu
                        menu_levels.erase()

                        #met en place la partie
                        level1 = Level1(screen, police1, settings.return_settings())
                        games[1] = level1
                        level1.set_room_1(armurerie.return_current_player(), armurerie.return_current_weapon())

                    elif menu_levels.button_level2.click() :
                        if not menu_levels.level2["lock"] :

                            #relance la musique
                            sound.music.stop()
                            sound.music.play(loops=-1)

                            #efface le menu 
                            menu_levels.erase()

                            #met en place la partie
                            level2 = Level2(screen, police1, settings.return_settings())
                            games[2] = level2
                            level2.set_room_1(armurerie.return_current_player(), armurerie.return_current_weapon())

                    elif menu_levels.button_level3.click() :
                        if not menu_levels.level3["lock"] :

                            #relance la musique
                            sound.music.stop()
                            sound.music.play(loops=-1)

                            #efface le menu
                            menu_levels.erase()

                            #met en place la partie
                            level3 = Level3(screen, police1, settings.return_settings())
                            games[3] = level3
                            level3.set_room_1(armurerie.return_current_player(), armurerie.return_current_weapon())

                #menu pour le changement d'arme et de personnage
                if armurerie.etat :

                    if armurerie.button_return.click() :
                        #retour au menu
                        armurerie.erase()
                        menu.set()

                    #boutons pour changer de joueur
                    elif armurerie.button_player_0.click() :
                        armurerie.change_player(-1) 

                    elif armurerie.button_player_1.click() :
                        armurerie.change_player(1)

                    #boutons pour changer d'arme
                    elif armurerie.button_weapon_0.click() :
                        armurerie.change_weapon(-1)

                    elif armurerie.button_weapon_1.click() :
                        armurerie.change_weapon(1)

                #menu pour les paramètres
                if settings.etat :

                    if settings.button_return.click() : 
                        #retour au menu
                        settings.erase()
                        menu.set()
                    
                    #boutons pour changer la difficulté
                    elif settings.button_inferior.click() :
                        settings.change_difficulty(-1)

                    elif settings.button_superior.click() :
                        settings.change_difficulty(1)

                    #boutons pour activer ou désactiver le son
                    elif settings.button_inferior_son.click() :
                        settings.change_sound(-1)

                    elif settings.button_superior_son.click() :
                        settings.change_sound(1)

                    #boutons pour changer les commandes de jeu
                    elif settings.button_inferior_gp.click() :
                        settings.change_gp(-1)

                    elif settings.button_superior_gp.click() :
                        settings.change_gp(1)

            #commandes de jeu : si le joueur appuie sur une touche
            if game.etat :
                game.manage_events(event)

            elif level1.etat :
                level1.manage_events(event)

            elif level2.etat :
                level2.manage_events(event)

            elif level3.etat :
                level3.manage_events(event)

    #affichage
    if not(pause) : 

        #efface l'écran
        screen.fill(0)

        if menu.etat :
            menu.draw() #affiche tous les éléments du menu principal

        elif menu_levels.etat :
            menu_levels.draw() #affiche tous les éléments du menu des levels

        elif armurerie.etat :
            armurerie.draw() #affiche tous les éléments du menu pour changer d'arme et de personnage

        elif settings.etat :
            settings.draw() #affiche tous les éléments du menu des paramètres

        elif game.etat :
            #applique les mouvements du personnage et des ennemis
            game.apply()
            
            #affiche tous les éléments de la partie
            game.draw() 

            #revient au menu
            if game.end_game_over :
                game.erase()
                menu.set()

        elif level1.etat :
            #applique les mouvements du personnage et des ennemis
            level1.apply()
            
            #affiche tous les éléments du level
            level1.draw() 

            #revient au menu
            if level1.end_game_over :
                if level1.win :
                    menu_levels.level1["achieve"] = True
                    menu_levels.update() #actualiser l'état des levels
                level1.erase()
                menu.set()

        elif level2.etat :
            #applique les mouvements du personnage et des ennemis
            level2.apply()
            
            #affiche tous les éléments du level
            level2.draw() 

            #revient au menu
            if level2.end_game_over :
                if level2.win :
                    menu_levels.level2["achieve"] = True
                    menu_levels.update() #actualiser l'état des levels
                level2.erase()
                menu.set()

        elif level3.etat :
            #applique les mouvements du personnage et des ennemis
            level3.apply()
            
            #affiche tous les éléments du level
            level3.draw() 

            #revient au menu
            if level3.end_game_over :
                if level3.win :
                    menu_levels.level3["achieve"] = True
                level3.erase()
                menu.set()

    pygame.display.flip() #met à jour l'écran
    timer.tick(30) #30 fps

#ferme la fenêtre et quitte le jeu
pygame.quit()
sys.exit()