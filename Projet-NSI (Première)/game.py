import pygame
import sys
import time
import random
import pytmx
import pyscroll
from player import Player
from button import Button
from menus import Menu
from weapon import *
from enemy import *
import data
from sound import sound

class Game :
    def __init__(self, screen, police, settings) :
        self.etat = False
        self.screen = screen
        self.police = police

        self.settings = settings

        self.Time_shield = None
        self.counter = 2

        self.map_size = (1080, 700)

        #map
        self.tmx_data = pytmx.util_pygame.load_pygame(random.choice(data.maps))
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        #groupe pour dessiner la carte
        self.group_map = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)

        #liste des murs
        self.walls = []

        #zone de spawn des monstres
        self.enemies_spawnareas = []

        #point de spawn
        self.spawnpoint = None

        for obj in self.tmx_data.objects :
            if obj.type == "collision" :
                self.walls.append(pygame.Rect((obj.x, obj.y), (obj.width, obj.height)))
            elif obj.type == "monster spawnarea" : 
                self.enemies_spawnareas.append(pygame.Rect((obj.x, obj.y), (obj.width, obj.height)))
            elif obj.type == "spawnpoint" :
                self.spawnpoint = (obj.x, obj.y)

        #player
        self.player = None
        #weapon
        self.current_weapon = None

        #contrôles
        self.pressed = {}

        self.t_attack_wait = 0 #sert à éviter que le joueur tire en même temps qu'un appui de bouton

        #victoire ou défaite
        self.win = False

        #images boutons
        self.buttons = pygame.image.load("assets/buttons.png")

        #bouton pause
        self.image_button_pause = self.buttons.subsurface(670, 100, 100, 100)
        self.image_button_play = pygame.transform.scale_by(self.image_button_pause, 0.5)
        self.image_button_pause = pygame.transform.scale_by(self.image_button_pause, 0.5)

        self.image_pause = pygame.image.load("assets/button_pause_play.png").subsurface(428, 80, 80, 100)
        self.image_pause = pygame.transform.scale_by(self.image_pause, 0.2)
        self.image_play = pygame.image.load("assets/button_pause_play.png").subsurface(340, 80, 80, 100)
        self.image_play = pygame.transform.scale_by(self.image_play, 0.2)

        self.image_button_pause.blit(self.image_pause, (18, 14))
        self.image_button_play.blit(self.image_play, (20, 14))

        self.button_pause = Button(self.image_button_pause, (1030, 50), self.screen)
        
        #nombre d'ennemis morts
        self.number_dead_enemies = 0

        #image tues
        self.buttons2 = pygame.image.load("assets/buttons.png")

        #bouton tues
        self.image_button_tues = self.buttons2.subsurface(670, 100, 100, 100)
        self.image_button_tues = pygame.transform.scale_by(self.image_button_tues, 0.5)
        self.number_dead_enemies = self.number_dead_enemies
        nbr_morts = str(self.number_dead_enemies)
        self.image_button_tues_2 = police.render(nbr_morts, True, (0, 0, 0))
        self.image_button_tues.blit(self.image_button_tues_2, (16, 10))
        self.button_tues = Button(self.image_button_tues, (1030, 100), self.screen)


        #animation de fin
        self.game_over = False
        self.end_game_over = False
        self.game_over_t0 = 0
        self.game_over_t1 = 0
        self.game_over_tfinal = 3000
        police_path = "assets/police/police.ttf"
        self.police2 = pygame.font.Font(police_path, 50)
        self.image_game_over = self.police2.render("Game Over !", True, (255, 255, 255))
        self.image_win = self.police2.render("You win !", True, (255, 255, 255))
        self.image_gameoverbg = pygame.image.load("assets/game over.jpg")

        #types de monstre
        self.types_skeleton = [SkeletonBase, SkeletonRogue, SkeletonShaman, SkeletonWarrior]
        self.types_orc = [OrcBase, OrcRogue, OrcShaman, OrcWarrior]
        self.types_monsters = self.types_orc + self.types_skeleton

        #niveau de difficulté
        self.difficulty = None
        if self.settings["difficulty"] == "easy" :
            self.difficulty = 0
        elif self.settings["difficulty"] == "normal" :
            self.difficulty = 1
        elif self.settings["difficulty"] == "hard" :
            self.difficulty = 2

        #nombre de vagues
        self.max_waves = 3
        self.wave_number = 0

    def set(self, player, weapon) :
        self.etat = True

        self.t_attack_wait = pygame.time.get_ticks()

        #bouton pause
        self.button_pause.move((1030, 50))

        #bouton tues
        self.button_tues.move((1030, 100))

        #création du joueur
        self.player = player

        #création de l'arme
        self.current_weapon = weapon
        self.player.change_weapon(self.current_weapon)

        #bouge le joueur au point d'apparition
        self.player.move_at(self.spawnpoint)

        #création des monstres
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()
        self.potions = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)

        self.set_new_wave()

    def draw(self) :

        #dessiner les tuiles     
        self.group_map.draw(self.screen)
        
        self.potions.draw(self.screen)

        #ennemis
        for dead_enemy in self.dead_enemies :
            dead_enemy.draw()
            if dead_enemy.weapon != None :
                dead_enemy.weapon.draw_attack()
                dead_enemy.weapon.draw()

        for enemy in self.enemies :
            enemy.draw()
            if enemy.weapon != None :
                enemy.weapon.draw_attack()
                enemy.weapon.draw()

        #personnage
        self.player.draw()
        self.player.draw_health_bar()
        #dessine les attaques
        self.player.weapon.draw_attack()
        #arme
        self.player.weapon.draw()

        #bouton pause
        self.button_pause.draw()

        #bouton tues
        self.image_button_tues = self.buttons2.subsurface(670, 100, 100, 100)
        self.image_button_tues = pygame.transform.scale_by(self.image_button_tues, 0.5)
        self.number_dead_enemies = self.number_dead_enemies
        nbr_morts = str(self.number_dead_enemies)
        self.image_button_tues_2 = self.police.render(nbr_morts, True, (0, 0, 0))
        self.image_button_tues.blit(self.image_button_tues_2, (16, 10))
        self.button_tues = Button(self.image_button_tues, (1030, 100), self.screen)
        self.button_tues.draw()

        #affichage de game over
        if self.game_over :
            self.screen.blit(self.image_gameoverbg, (0, 0))
            if self.win :
                self.screen.blit(self.image_win, (400, 250))
            else :
                self.screen.blit(self.image_game_over, (350, 250))
            nbr_morts = str(self.number_dead_enemies)
            nbr_morts_affichage = self.police2.render("Vous avez tue " + nbr_morts + " monstres !", True, (255, 255, 255))
            self.screen.blit(nbr_morts_affichage, (120, 400))

    def erase(self) :
        self.etat = False

        #ennemis
        self.enemies.empty()
        self.dead_enemies.empty()  

    def set_new_wave(self) : 

        self.dead_enemies.empty()

        self.wave_number += 1

        for area in self.enemies_spawnareas :
            enemy_per_area = self.difficulty + self.wave_number 
            for i in range(enemy_per_area) :

                #établi aléatoirement les coordonnées du monstre 
                x_area = int(area.x) + 1
                y_area = int(area.y) + 1
                area_xmax = int(x_area + area.width) -1
                area_ymax = int(y_area + area.height) -1

                coords = (random.randint(x_area, area_xmax), random.randint(y_area, area_ymax))

                #choisi aléatoirement les type de monstre
                enemy_type = self.types_monsters[random.randint(0, len(self.types_monsters)-1)]

                enemy = enemy_type(self.screen, coords)

                self.enemies.add(enemy)

            if_potion = random.randint(0,1) #une chance sur deux de faire apparaître une potion
            if if_potion == 0 :
                x_area = int(area.x) + 1
                y_area = int(area.y) + 1
                area_xmax = int(x_area + area.width) -1
                area_ymax = int(y_area + area.height) -1

                coords = (random.randint(x_area, area_xmax), random.randint(y_area, area_ymax)) #coordonnées aléatoires de la potion
                self.potions.add(Potion(self.screen,coords))

    def verification(self, sprite, x, y) :
        sprite.rect.x += x
        sprite.rect.y += y
        sprite.move_feet()
        verification = True
        if sprite.feet.collidelist(self.walls) > -1 : 
            verification =  False
        sprite.move_back(True, True)
        return verification
                
    def potions_heal(self) :
        for potion in self.potions :
            if potion.rect.colliderect(self.player.rect) and self.player.pv < self.player.max_pv :
                potion.heal(self.player)
                self.potions.remove(potion)

    #gère les mouvements et les attaques du joueur
    def apply_player(self) : 
        #mort du joueur
        if self.player.pv <= 0 and not(self.player.death):
            self.player.player_death()

        if not(self.player.death) :
            #bouge le joueur
            self.move_player()

            #attaques du joueur
            if pygame.mouse.get_pressed()[0] and self.return_player_attack_delay() :
                self.player.attack(self.walls)

    #gère les déplacements et les attaques de chaque ennemi
    def apply_enemies(self) :
        for enemy in self.enemies :
            
            #vérifie si l'ennemi est mort
            if enemy.pv <= 0 and not(enemy.death) :
                enemy.enemy_death()
                self.number_dead_enemies += 1
                #s'il reste encore un autre ennemi en vie
                if len(self.enemies) > 1 :
                    self.dead_enemies.add(enemy)
                    self.enemies.remove(enemy)

            #s'il est le dernier ennemi dans le groupe ennemi et qu'il a fini de mourir
            if len(self.enemies) == 1 and enemy in self.enemies and enemy.end_death :
                self.dead_enemies.add(enemy)
                self.enemies.remove(enemy)

            #applique le mouvement de l'ennemi
            if not(enemy.death) :
                self.move_enemy(enemy)
                self.enemy_attacks(enemy)

    #gère les déplacements du joueur
    def move_player(self) : 

        #vérifie si les touches sont pressés; si oui bouger le joueur
        if self.pressed.get(self.settings["jouabilité"][1]["left"]) and self.player.rect.left > 0:
            if self.verification(self.player, -self.player.speed, 0) : 
                self.player.move_left()
        if self.pressed.get(self.settings["jouabilité"][1]["right"]) and self.player.rect.right < self.map_size[0] :
            if self.verification(self.player, self.player.speed, 0) : 
                self.player.move_right()
        if self.pressed.get(self.settings["jouabilité"][1]["up"]) and self.player.rect.top > 0:
            if self.verification(self.player, 0, -self.player.speed) : 
                self.player.move_up()
        if self.pressed.get(self.settings["jouabilité"][1]["down"]) and self.player.rect.bottom < self.map_size[1]:
            if self.verification(self.player, 0, self.player.speed) :
                self.player.move_down()
        
        #applique les mouvement du personnage
        self.player.move()
    
    #gère les déplacement d'un ennemi
    def move_enemy(self, enemy) :

        #vérifie s'il n'est pas déjà sur le joueur
        if not(enemy.rect.colliderect(self.player.rect)):

            #établit la direction de l'ennemi
            direction = trajectory_movement(self.walls, enemy, self.player.rect)
            if type(direction) == dict :
                #direction = [vector for vector in direction.values()][0]
                direction = vecteur(enemy.rect.center, self.player.rect.center, enemy.speed)
                x = direction[0]
                y = direction[1]

            else :
                x = 0
                y = 0

            #vérifie s'il n'entre pas en collisions avec des murs
            if not(self.verification(enemy, x, 0)) :
                x = 0
            if not(self.verification(enemy, 0, y)) :
                y = 0

            if x == 0 and abs(y) >= 0.05  :
                y = y*(enemy.speed/abs(y))
            elif abs(x) >= 0.05 and y == 0 :
                x = x*(enemy.speed/abs(x))

            enemy.move(x, y)

    def enemy_attacks(self, enemy) :

        if not(self.player.death) :
            if type(enemy.weapon) == Bow or type(enemy.weapon) == Gun :
                enemy.attack(self.player, self.walls)
            elif type(enemy.weapon) == Sword :
                enemy.attack(self.player, self.walls)
    
    #applique les attaques des sprites, les mouvements des projectiles et les interactions entre eux et les sprites
    def apply_attacks(self) :

        #applique les attaque du joueur
        if type(self.player.weapon) == Gun or type(self.player.weapon) == Bow :
            self.player.weapon.apply_attacks(self.walls)
            self.interactions(self.player, self.enemies)
        
        #applique les attaques des ennemis
        for enemy in self.enemies :
            if type(enemy.weapon) == Gun or type(enemy.weapon) == Bow :
                enemy.weapon.apply_attacks(self.walls)
                self.interactions(enemy, self.player_group)
        
        for dead_enemy in self.dead_enemies : 
            if type(dead_enemy.weapon) == Gun or type(dead_enemy.weapon) == Bow :
                dead_enemy.weapon.apply_attacks(self.walls)
                self.interactions(dead_enemy, self.player_group)

        #actualisation de la barre de vie du joueur
        self.player.actualise_health_bar()

    #gère les collisions des projectiles avec les sprites et les murs
    def interactions(self, sprite, list_enemies) :
        if type(sprite.weapon) == Gun or type(sprite.weapon) == Bow : #ne marche que si l'arme du sprite est un arc ou un pistolet

            for projectile in sprite.weapon.all_projectiles : #vérifie pour chaque projectile dans le groupe de projectiles de l'arme du sprite si il est en contact avec un ennemi ou avec un mur
                    
                    remove = False

                    #vérifie si le projectile est en collision avec un des sprite de la liste d'ennemis (peut être le joueur et les monstres)
                    for enemy in list_enemies : 
                        if projectile.rect.colliderect(enemy.rect) and enemy.pv > 0 :
                            if pygame.sprite.spritecollide(projectile, list_enemies, False, pygame.sprite.collide_mask) :
                                enemy.pv -= sprite.weapon.damage*sprite.coef_damage #fait des dégâts à l'ennemi avec lequel le projectile est entré en collision
                                remove = True
                                if not(sprite.weapon.type_damage == "zone") : #si ce n'est pas une arme qui fait des dégâts de zone, alors on la supprime
                                    sprite.weapon.all_projectiles.remove(projectile)
                                    break
                    
                    if remove :
                        #si l'arme fait des dégâts de zone et qu'il faut supprimer le projectile (remove = True si un projectile est entré en collision avec un ennemi)
                        if sprite.weapon.type_damage == "zone" :
                            sprite.weapon.all_projectiles.remove(projectile)

                    #vérifie si le projectile est entré en collision avec un mur
                    elif projectile.rect.collidelist(self.walls) > -1 :
                        sprite.weapon.all_projectiles.remove(projectile)

    #applique les cheat code
    def cheat(self) :
        #régénère le joueur
        if self.pressed.get(self.settings["jouabilité"][1]["life"]): 
            self.player.pv = self.player.max_pv

        #tue tous les ennemis
        if self.pressed.get(self.settings["jouabilité"][1]["bomb"]): 
            for enemy in self.enemies:
                enemy.pv =0 
    
        #shield
        if self.pressed.get(self.settings["jouabilité"][1]["sh"]) and self.counter > 0: 
           self.Time_shield = pygame.USEREVENT + 7
           pygame.time.set_timer(self.Time_shield, 10000)
           self.counter -= 1 
        if self.Time_shield == False :  
           self.player.pv = self.player.max_pv
    
    #applique toutes les actions
    def apply(self) : 
        #exécute tout le code de la partie tant qu'elle ne se termine pas
        if not(self.game_over) :
            if not(self.player.death):
                self.apply_player() #actions du joueur 
                self.apply_enemies() #actions de chaque ennemi
                self.potions_heal() #vérifie si un joueur a consommer une potion
                self.cheat() 
            self.apply_attacks() #applique les mouvements des attaques (coups, mouvements des balles) et vérifie si les projectiles entrent en collision avec un ennemi

            #si tous les ennemis sont morts et qu'il reste encore des vagues
            if len(self.enemies) == 0 and self.wave_number < self.max_waves :
                self.set_new_wave() 
            
            #vérifie si le joueur est mort ou si tous les ennemis sont morts (et qu'il ne reste plus de vagues) avant de lancer l'animation de fin de partie
            if (self.player.end_death == True or (len(self.enemies) == 0 and self.wave_number >= self.max_waves)):
                self.over() #applique le début de l'animation de fin de partie

        #si l'animation de fin de partie est en cours
        else :
            self.game_over_t1 = pygame.time.get_ticks()
            if (self.game_over_t1 - self.game_over_t0) >= self.game_over_tfinal : #si trois secondes se sont écoulées depuis le début de l'animation
                self.end_game_over = True #met fin à la partie --> permet de revenir au Menu principal dans main

    #gère le pause/play
    def pause(self, pause) : 
        #mettre toutes les touches à false
        for key in self.pressed.keys() :
            self.pressed[key] = False
        
        #changer l'image du bouton pause avec le signe play ou pause
        if pause == True : 
            self.button_pause.img = self.image_button_play
        elif pause == False :
            self.button_pause.img = self.image_button_pause

        self.t_attack_wait = pygame.time.get_ticks()

        self.draw()
    
    #commence l'animation de fin de partie
    def over(self) :
        self.game_over = True
        self.game_over_t0 = pygame.time.get_ticks()
        if self.player.death :
            sound.game_over_sound.play()
            self.win = False
        else :
            sound.win_sound.play()
            self.win = True
        sound.mvmt_sound.stop()
    
    #gère tous les évènements
    def manage_events(self, event) :

        if event.type == pygame.KEYDOWN : #si l'event est l'appui d'un bouton
            self.pressed[event.key] = True
            
            if event.key == pygame.K_0 and not(self.player.death):
                self.player.player_death() #se tuer manuellement

        elif event.type == pygame.KEYUP :
            self.pressed[event.key] = False

        #si l'évènement est un nombre (un pygame.USEREVENT)
        elif type(event.type) == int :

            #animations du joueur
            if event.type == self.player.CHANGE_IMAGE :
                self.player.change_animation()

            #animations des ennemis
            else :
        
                for enemy in self.enemies :
                    if event.type == enemy.CHANGE_IMAGE :
                        enemy.change_animation()

                for dead_enemy in self.dead_enemies :
                    if event.type == dead_enemy.CHANGE_IMAGE :
                        dead_enemy.change_animation()

    #permet d'éviter que le joueur tire en même temps qu'un bouton est appuyé (dans les deux cas, c'est un clic gauche)
    def return_player_attack_delay(self) :
        return (pygame.time.get_ticks() - self.t_attack_wait) >= 300
