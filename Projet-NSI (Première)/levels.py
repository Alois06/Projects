import pygame
import pytmx
import pyscroll
import random
from button import Button
from weapon import *
from enemy import *
import data
from sound import sound
from boss import Boss

#classe mère Level qui regroupe toutes les fonctions et attributs qui ne changent pas d'un level à l'autre

class Level :
    def __init__(self, screen, police, settings, maps) :
        self.etat = False
        self.screen = screen
        self.police1 = police
        self.portal = None 

        #cheats
        self.Time_shield = None
        self.cheat_counter = 3

        #contrôles
        self.pressed = {}

        #maps
        self.maps = maps
        self.map_size = (1080, 700)
        self.current_map = 1
        
        #settings
        self.settings = settings

        #player
        self.player = None
        #weapon
        self.weapon = None

        self.boss = None

        self.t_attack_wait = 0 #sert à éviter que le joueur tire en même temps qu'un appui de bouton

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

        self.types_skeleton = [SkeletonBase, SkeletonRogue, SkeletonShaman, SkeletonWarrior]
        self.types_orc = [OrcBase, OrcRogue, OrcShaman, OrcWarrior]
        self.types_monsters = self.types_orc + self.types_skeleton

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

        #affiche tous les éléments de la partie
    def draw(self) :
        #affiche la map
        self.group_map.draw(self.screen)

        #affiche les potions
        self.potions.draw(self.screen)
        
        #affichage des monstres
        for dead_enemy in self.dead_enemies :
            dead_enemy.draw()
            dead_enemy.weapon.draw_attack()
            dead_enemy.weapon.draw()
        
        for enemy in self.enemies :
            enemy.draw()
            enemy.weapon.draw_attack()
            enemy.weapon.draw()

        if type(self.boss) == Boss :
            self.boss.draw()
            self.boss.draw_health_bar()
            self.boss.draw_attack()

        #affichage du joueur
        self.player.draw()
        self.player.draw_health_bar()
        #dessine les attaques
        self.player.weapon.draw_attack()
        #arme
        self.player.weapon.draw()

        #bouton pause
        self.button_pause.draw()

        #portail
        if self.portal != None :
            self.portal.draw()

        #affichage de l'animation de fin
        if self.game_over :
            self.screen.blit(self.image_gameoverbg, (0, 0))
            if self.win :
                self.screen.blit(self.image_win, (400, 250))
            else :
                self.screen.blit(self.image_game_over, (350, 250))

    #réinitialise les groupes et "efface" la partie
    def erase(self) :
        self.etat = False

        #potions
        self.potions.empty()
        #ennemis
        self.enemies.empty()
        self.dead_enemies.empty()
        self.boss = None

    #crée une map à partir d'un fichier .tmx
    def set_new_map(self, room_number) :

        self.tmx_data = pytmx.util_pygame.load_pygame(self.maps[room_number])
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        #groupe pour dessiner la map
        self.group_map = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        #liste des murs
        self.walls = []

        #zone d'apparition des monstres
        self.enemies_spawnareas = []

        #point de spawn
        self.spawnpoint = None

        #point d'apparition du portail
        self.portal_coords = None

        #dans les objets contenus dans le fichier, on récupère les murs, les "zones de monstre" et le point d'apparition
        for obj in self.tmx_data.objects : 
            if obj.type == "collision" :
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "monster spawnarea" : 
                self.enemies_spawnareas.append(pygame.Rect((obj.x, obj.y), (obj.width, obj.height)))
            elif obj.type == "spawnpoint" :
                self.spawnpoint = (obj.x, obj.y)
            elif obj.type == "portal spawnpoint" :
                self.portal_coords = (obj.x, obj.y)

    #vérifie si le sprite peut se déplacer en x et en y (vérifie s'il entre en collision avec un mur)
    def verification(self, sprite, x, y) :
        #on fait avancer le sprite
        sprite.rect.x += x
        sprite.rect.y += y
        sprite.move_feet()
        
        #on vérifie si le sprite entre en collision avec un mur
        verification = True
        for wall in self.walls : 
            if sprite.feet.colliderect(wall) : 
                verification =  False
                break

        #on renvient en arrière et on renvoie si le sprite peut avancer ou non
        sprite.move_back(True, True)
        return verification 
    
    #vérifie si le joueur entre en contact avec une potion : si c'est le cas, alors il est régénéré
    def potions_heal(self) :
        for potion in self.potions :
            if potion.rect.colliderect(self.player.rect) and self.player.pv < self.player.max_pv :
                potion.heal(self.player)
                self.potions.remove(potion) 

    #gère les cheat
    def cheat(self) :
        #régènere le joueur
        if self.pressed.get(self.settings["jouabilité"][1]["life"]): 
            self.player.life_pv()

        #tue tous les ennemis
        if self.pressed.get(self.settings["jouabilité"][1]["bomb"]): 
            for enemy in self.enemies:
                enemy.pv = 0 
            if type(self.boss) == Boss :
                self.boss.boss_death()

        #shield
        if self.pressed.get(self.settings["jouabilité"][1]["sh"]) and self.counter > 0: 
           self.Time_shield = pygame.USEREVENT + 8
           pygame.time.set_timer(self.Time_shield, 10000)
           self.counter -= 1 
        if self.Time_shield == False :  
           self.player.life_pv()

    #gère les mouvements et les attaques du joueur
    def apply_player(self) :
        #vérifie si le joueur est mort
        if self.player.pv <= 0 and not(self.player.death) :
            self.player.player_death()

        if not(self.player.death) :
            #mouvements du joueur
            self.move_player()
            
            #attaques du joueur
            if pygame.mouse.get_pressed()[0] and self.return_player_attack_delay() :
                self.player.attack(self.walls)

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

    #gère les déplacements et les attaques de chaque ennemi
    def apply_enemies(self) :
        for enemy in self.enemies :
            
            #vérifie si l'ennemi est mort
            if enemy.pv <= 0 and not(enemy.death) :
                enemy.enemy_death()
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

            #fait bouger le joueur
            enemy.move(x, y)

    def enemy_attacks(self, enemy) :

        if not(self.player.death) :
            enemy.attack(self.player, self.walls)

    #applique les mouvements et les attaques du boss
    def apply_boss(self) :
        self.boss.apply(self.walls, self.verification)

    #applique les attaques, les mouvements de projectiles et les interactions entre eux et les sprites
    def apply_attacks(self) :

        #applique les attaque du joueur
        if type(self.player.weapon) == Gun or type(self.player.weapon) == Bow :
            self.player.weapon.apply_attacks(self.walls)

            list_enemies = list(self.enemies)
            if type(self.boss) == Boss :
                list_enemies += [self.boss]
            self.interactions(self.player,  list_enemies)
        
        #applique les attaques des ennemis
        for enemy in self.enemies :
            if type(enemy.weapon) == Gun or type(enemy.weapon) == Bow :
                enemy.weapon.apply_attacks(self.walls)
                self.interactions(enemy, [self.player])
        
        for dead_enemy in self.dead_enemies : 
            if type(dead_enemy.weapon) == Gun or type(dead_enemy.weapon) == Bow :
                dead_enemy.weapon.apply_attacks(self.walls)
                self.interactions(dead_enemy, [self.player])

        #applique les attaques du boss
        if type(self.boss) == Boss :
            self.boss.apply_attacks()
            self.boss_interactions()
            self.boss.actualise_health_bar()

        #actualisation de la barre de vie du joueur
        self.player.actualise_health_bar()

    #gère les interactions entre les projectiles et les sprites
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

    #gère les interactions en relation avec le boss final
    def boss_interactions(self) :
        for fireball in self.boss.all_fireballs : 
            if fireball.rect.colliderect(self.player.rect) and self.player.pv > 0 :
                self.boss.all_fireballs.remove(fireball)
                sound.explose_sound.play()
                self.player.pv -= self.boss.fireball_damage
            elif fireball.rect.collidelist(self.walls) > -1 :
                self.boss.all_fireballs.remove(fireball)
                sound.explose_sound.play() 

    #gère les portails
    def apply_portal(self) :
        if self.portal != None : #si un portail a été créé (n'est pas inexistant)
            if self.player.rect.colliderect(self.portal.rect): #si le joueur entre en collision avec ce portail
                #si la pièce actuelle était la 1 : on met en place la pièce 2
                if self.current_map == 1 : 
                    self.erase()
                    self.etat = True
                    self.set_room_2()
                    sound.teleportation_sound.play()

                #si la pièce actuelle était la 2 : on met en place la pièce 3
                elif self.current_map == 2 :
                    self.erase()
                    self.etat = True
                    self.set_room_3()
                    sound.teleportation_sound.play()

                #sinon, c'est la pièce 3 : la partie se termine
                else : 
                    if not(self.game_over) :
                        self.over()  

                #suppression du portail
                self.portal = None

    #fonction qui gère l'ensembe de la partie
    def apply(self) : 
        if not(self.game_over) :
            if not(self.player.death) : #si le joueur est en vie et que la partie est en cours : appliquer toute ces fonctions
                self.apply_player()
                self.apply_enemies()
                if type(self.boss) == Boss :
                    self.apply_boss()
                self.potions_heal()
                self.cheat()
            self.apply_attacks()
            self.apply_portal()

            #si tous les ennemis sont morts et qu'aucun portail n'a encore été crée : alors on crée un portail
            if len(self.enemies) == 0 and self.portal == None and not(self.game_over):
                if type(self.boss) == Boss :
                    if self.boss.end_death :
                        self.portal = Portal(self.screen, self.portal_coords)
                else :
                    self.portal = Portal(self.screen, self.portal_coords)
                
            #vérifie si le joueur est mort avant de lancer l'animation de game over
            if self.player.end_death == True :
                self.over()

        #si la partie est finie et que l'animation de fin de partie est en cours
        else :
            self.game_over_t1 = pygame.time.get_ticks()
            if (self.game_over_t1 - self.game_over_t0) >= self.game_over_tfinal : 
                self.end_game_over = True #met fin à la partie et à l'animation : permet le retour au menu

    def spawn (self):
        for area in self.enemies_spawnareas :
            enemy_per_area = self.dif
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
        if self.player.death : #si le joueur est mort, alors on joue le son game over
            sound.game_over_sound.play()
        else : #sinon, le joueur est en vie donc on joue le son de victoire
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

                if type(self.boss) == Boss :
                    if event.type == self.boss.CHANGE_IMAGE :
                        self.boss.change_animation()
                
                for enemy in self.enemies :
                    if event.type == enemy.CHANGE_IMAGE :
                        enemy.change_animation()

                for dead_enemy in self.dead_enemies :
                    if event.type == dead_enemy.CHANGE_IMAGE :
                        dead_enemy.change_animation()
    
    #permet d'éviter que le joueur tire en même temps qu'un bouton est appuyé (dans les deux cas, c'est un clic gauche)
    def return_player_attack_delay(self) :
        return (pygame.time.get_ticks() - self.t_attack_wait) >= 300


#classes de chaque level héritant de la classe mère Level : Level1, Level2 et Level3

class Level1(Level) :
    def __init__(self, screen, police, settings) :

        super().__init__(screen, police, settings, data.maps[0:3])

    #met en place la pièce 1
    def set_room_1(self, player, weapon): 

        self.etat = True
        self.dif = 1 
        self.t_attack_wait = pygame.time.get_ticks()

        self.current_map = 1
        self.set_new_map(0)

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        #création du joueur
        self.player = player
        self.player.change_weapon(weapon)
        self.player.move_at(self.spawnpoint)
        self.spawn()

        
        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 2
    def set_room_2 (self): 
        
        self.current_map = 2
        self.set_new_map(1)
        self.dif += 1 
        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)

        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 3
    def set_room_3 (self): 

        self.current_map = 3
        self.set_new_map(2)
        self.dif += 1 

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))


class Level2(Level) :
    def __init__(self, screen, police, settings) :

        super().__init__(screen, police, settings, data.maps[3:6])

    #met en place la pièce 1
    def set_room_1(self, player, weapon): 

        self.etat = True
        self.dif = 2

        self.t_attack_wait = pygame.time.get_ticks()

        self.current_map = 1
        self.set_new_map(0)

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        #création du joueur
        self.player = player
        self.player.change_weapon(weapon)
        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 2
    def set_room_2 (self): 
        
        self.current_map = 2
        self.set_new_map(1)
        self.dif += 1 
        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 3
    def set_room_3 (self): 

        self.current_map = 3
        self.set_new_map(2)
        self.dif +=1 

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))


class Level3(Level) :
    def __init__(self, screen, police, settings) :
        
        super().__init__(screen, police, settings, data.maps[6:9])

    #met en place la pièce 1
    def set_room_1(self, player, weapon): 

        self.etat = True

        self.t_attack_wait = pygame.time.get_ticks()

        self.current_map = 1
        self.set_new_map(0)
        self.dif = 2

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        #création du joueur
        self.player = player
        self.player.change_weapon(weapon)
        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 2
    def set_room_2 (self): 
        
        self.current_map = 2
        self.set_new_map(1)
        self.dif += 1 
        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)
        self.spawn()

        #bouton pause
        self.button_pause.move((1030, 50))

    #met en place la pièce 3
    def set_room_3 (self): 

        self.current_map = 3
        self.set_new_map(2)

        #création des groupes contenant : les potions, les ennemis/monstres et les ennemis morts
        self.potions = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()

        self.player.move_at(self.spawnpoint)

        self.boss = Boss(self.screen, self.portal_coords, self.player, self.enemies)

        #bouton pause
        self.button_pause.move((1030, 50))

