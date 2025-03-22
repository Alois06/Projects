import pygame
import random
from tools import *
from projectile import Projectile
from data import change_image_speed
from sound import sound
from enemy import *

class Boss(pygame.sprite.Sprite) :
    def __init__(self, screen, coords, player, enemies):
        super().__init__()

        self.screen = screen

        self.coords = coords

        #attributs
        self.pv = 5000
        self.max_pv = 5000
        self.speed = 3

        #joueur
        self.player = player

        #groupe de monstres
        self.enemies = enemies
        self.types_monsters = [SkeletonBase, SkeletonRogue, SkeletonShaman, SkeletonWarrior, OrcBase, OrcRogue, OrcShaman, OrcWarrior]

        #IMAGES

        #images pour chaque actions
        self.images_death = pygame.image.load("assets2/Boss/Sprites/Death.png")
        self.images_idle = pygame.image.load("assets2/Boss/Sprites/Idle.png")
        self.images_run = pygame.image.load("assets2/Boss/Sprites/Run.png")
        self.images_attack1 = pygame.image.load("assets2/Boss/Sprites/Attack1.png")
        self.images_attack2 = pygame.image.load("assets2/Boss/Sprites/Attack2.png")

        #tableaux
        self.images_death_table = [[104, 80, 50, 88], [352, 72, 60, 96], [608, 72, 72, 96], [856, 64, 104, 104], [1104, 56, 112, 112], [1360, 135, 104, 32], [1608, 152, 108, 16]]
        self.images_idle_table = [[104, 72, 64, 96], [354, 64, 64, 104], [604, 64, 64, 104], [854, 72, 64, 96], [1104, 64, 64, 104], [1354, 71, 64, 97], [1604, 80, 64, 88], [1854, 80, 64, 88]]
        self.images_run_table = [[88, 104, 72, 64], [352, 104, 72, 64], [604, 96, 72, 72], [848, 104, 72, 64], [1096, 104, 72, 64], [1354, 104, 66, 64], [1600, 106, 68, 62], [1848, 104, 64, 64]]
        self.images_attack1_table = [[72, 104, 64, 64], [328, 96, 64, 72], [584, 88, 64, 80], [1864, 64, 88, 104]]
        self.images_attack2_table = [[104, 56, 80, 112], [328, 56, 80, 112], [580, 52, 80, 116], [832, 40, 80, 128], [1080, 39, 168, 129], [1336, 50, 152, 118], [1604, 64, 128, 104], [1852, 80, 112, 88]]

        #état : mort ou en mouvement (ou inactif si aucun des quatre)
        self.death = False
        self.run = False
        self.attack1 = False
        self.attack2 = False

        #index de l'image
        self.image_index = 1

        #image
        self.image = self.images_idle.subsurface([104, 72, 64, 96])
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect()
        self.rect.midbottom = coords
        self.mask = pygame.mask.from_surface(self.image)

        #event pour le changement d'image
        self.CHANGE_IMAGE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.CHANGE_IMAGE, change_image_speed[str(self.speed)])

        #côté
        self.left = False

        #fin de l'animation de mort
        self.end_death = False

        #pieds pour les collisions
        self.feet = pygame.Rect((0,0), (self.rect.width*0.8, 0.75*self.rect.height))
        self.feet.midbottom = self.rect.midbottom
        self.old_position = self.feet.copy()

        #delai pour l'attaque
        self.t_attack_1 = 0
        self.t_attack_2 = 0
        self.attack_delay_1 = 250 #attaques à distance (boules de feu)
        self.attack_delay_2 = 15000 #attaque de corps à corps

        #pour l'attaque de corps à corps
        self.range_activation_attack_2 = 200
        self.range_damage_attack_2 = 250
        self.damage = 300
        #pour l'onde de choc
        self.onde = False
        self.onde_images = [] #liste qui regroupe chaque image de l'animation
        for i in range(1, 14) : 
            img = pygame.image.load("assets/effets mêlées 2/img" + str(i) + ".png")
            img.set_colorkey(img.get_at([0, 0]))
            self.onde_images.append(img)
        self.onde_images_index = 0 
        self.onde_image = self.onde_images[self.onde_images_index]
        self.onde_animation_time = 50
        self.onde_last_image_time = 0

        #boule de feu pour l'attaque
        self.fireball = pygame.image.load("assets2/Boss/Fire Ball/Move.png").subsurface(152, 16, 17, 20)
        self.fireball = pygame.transform.scale_by(self.fireball, 1.5)
        self.all_fireballs = pygame.sprite.Group()
        self.v_fireball = 7
        self.fireball_damage = 200
        self.coords_tir = (24*1.5, -12*1.5)

        #attaque à distance possible
        self.trajectory_projectile = False

        #mouvement possible
        self.trajectory_movement = False

        #teleportation counter
        self.player_teleportation_counter = 1

        #barre de vie 
        self.health_bar_max = pygame.Rect((0, 0), (round(self.rect.width*0.75), 4))
        self.health_bar_max.midbottom = self.rect.midtop

        self.health_bar = pygame.Rect((0, 0), (self.health_bar_max.width, self.health_bar_max.height))
        self.health_bar.topleft = self.health_bar_max.topleft

    #affiche le boss à l'écran
    def draw(self) : 
        #dessiner l'image du boss
        self.screen.blit(self.image, self.rect)

    #affiche la barre de vie du boss
    def draw_health_bar(self) :
        if not(self.death) : 
            pygame.draw.rect(self.screen, (255, 255, 255), self.health_bar_max, border_radius=2)
            pygame.draw.rect(self.screen, (255, 0, 255), self.health_bar, border_radius=2)

    #actualise la longueur de la barre de vie du boss
    def actualise_health_bar(self) :
        #nouvelle barre de vie
        t = round(self.pv/self.max_pv, 2)
        self.health_bar = pygame.Rect((0, 0), (self.health_bar_max.width*t, self.health_bar_max.height))
        self.health_bar.topleft = self.health_bar_max.topleft

    #bouge la barre de vie au dessus de l'image du boss
    def move_health_bar(self) :
        self.health_bar_max.midbottom = self.rect.midtop
        self.health_bar.topleft = self.health_bar_max.topleft

    #crée une nouvelle image
    def new_image(self, sprite_sheet, table, index) :

        self.image = sprite_sheet.subsurface(table[index])

        #change la taille de l'image
        self.image = pygame.transform.scale_by(self.image, 1.5)

        #si le personnage va vers la gauche
        if self.left:
            self.image = pygame.transform.flip(self.image, True, False)

        #établit son nouveau rectangle et son nouveau mask
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.feet.midbottom
        self.mask = pygame.mask.from_surface(self.image)

    #permet de changer d'animation/image en fonction de l'état du boss (run, death, etc)
    def change_animation(self) :

        if not(self.end_death) : 

            #s'il meurt
            if self.death :
                if self.image_index > len(self.images_death_table)-1 :
                    self.end_death = True
                else :
                    self.new_image(self.images_death, self.images_death_table, self.image_index)

            #s'il lance sa première attaque 
            elif self.attack1 : 
                if self.image_index > len(self.images_attack1_table)-1 :
                    self.image_index = 0
                    self.attack1 = False
                else :
                    self.new_image(self.images_attack1, self.images_attack1_table, self.image_index)

            #s'il lance sa deuxième attaque
            elif self.attack2 : 
                if self.image_index > len(self.images_attack2_table)-1 :
                    self.image_index = 0
                    self.attack2 = False
                else :
                    self.new_image(self.images_attack2, self.images_attack2_table, self.image_index)

            #si il court
            elif self.run :
                if self.image_index > len(self.images_run_table)-1 :
                    self.image_index = 0
                self.new_image(self.images_run, self.images_run_table, self.image_index)
                    
            #si il est inactif
            else :
                if self.image_index > len(self.images_idle_table)-1 :
                    self.image_index = 0
                self.new_image(self.images_idle, self.images_idle_table, self.image_index)

            self.image_index += 1
       
            self.change_image = False
            self.run = False

    #gère les déplacements du boss
    def move(self, x, y) :

        #si il meurt ou s'il est en train d'attaquer il ne bouge plus
        if self.death or self.attack1 or self.attack2:
            x = 0
            y = 0

        #bouge l'ennemi
        self.rect.x += x
        self.rect.y += y
        
        #bouge ses pieds
        self.move_feet()

        #bouge la barre de vie
        self.move_health_bar()

        #vérifie s'il va à gauche ou à droite
        if x < 0 :
            if self.left == False :
                self.image = pygame.transform.flip(self.image, True, False)
            self.left = True
        elif x > 0 :
            if self.left == True :
                self.image = pygame.transform.flip(self.image, True, False)
            self.left = False

        #vérifie s'il court
        if abs(x) < 0.25 and abs(y) < 0.25 :
            self.run = False
        else :
            self.run = True
    
    def move_at(self, coords) : 
        self.rect.midbottom = coords
        self.move_feet()
        self.move_health_bar()

    #bouge les pieds et sauvegarde l'ancienne position du boss
    def move_feet(self) : 
        self.old_position = self.feet.copy()
        self.feet.midbottom = self.rect.midbottom
    
    #permet de revenir à l'ancienne position (en x ou en y)
    def move_back(self, on_x, on_y) :
        if on_x : 
            self.rect.center = (self.old_position.midbottom[0], self.rect.center[1])
        if on_y : 
            self.rect.bottom = self.old_position.bottom
        self.feet.midbottom = self.rect.midbottom
    
    #permet de lancer l'attaque 1 ou 2 si possible et de gérer le déroulement d'une des deux attaques s'il y en a une en cours
    def attack(self, collisions) :
        #si aucune attaque n'a encore été lancée
        if not(self.attack1 or self.attack2) :
            if self.return_attack_delay_1() and self.trajectory_projectile :
                self.attack1 = True
                self.image_index = 0
            elif self.return_attack_delay_2() and get_distance(self.rect.center, self.player.rect.center) <= self.range_activation_attack_2 :
                self.attack2 = True
                self.image_index = 0
                if self.rect.x > self.player.rect.x :
                    self.left = True

            else : 
                self.invocation()
                self.player_teleportation()

        #si l'attaque 1 est déjà en cours
        elif self.attack1 : 
            self.attack_1(collisions)

        #si l'attaque 2 est déjà en cours
        elif self.attack2 :
            self.attack_2()

    #attaque 1 : envoie une boule de feu 
    def attack_1(self, collisions) :
        if self.image_index == 3 :
            if self.rect.x > self.player.rect.x :
                self.left = True
            else : 
                self.left = False
        elif self.image_index == 4 :
            #création du projectile
            angle = 0
            if self.left == True :
                angle = 180
            coords_tir = get_position(self.rect.center[0], self.rect.center[1], self.coords_tir[0], self.coords_tir[1], angle, True)
            direction = vecteur(coords_tir, self.player.rect.center, self.v_fireball)
            self.all_fireballs.add(Projectile(self.fireball, coords_tir, direction, collisions)) #création de la boule de feu
            sound.fireball_sound.play() #joue le son de la boule de feu

            self.t_attack_1 = pygame.time.get_ticks()
            self.attack1 = False

    #attaque 2 : attaque de corps à corps (onde de choc)
    def attack_2(self) :
        if self.image_index == 6 :
            sound.sword_sound.play()
            self.onde = True
            self.onde_last_image_time = pygame.time.get_ticks()
        elif self.image_index == 8 :
            self.t_attack_2 = pygame.time.get_ticks()
            self.attack2 = False
            #if onde de choc touche le joueur : enlever des pv au joueur
            if get_distance(self.rect.center, self.player.rect.center) <= self.range_damage_attack_2 :
                self.player.pv -= self.damage

    #applique le mouvement des boules de feu et l'animation de l'onde de choc
    def apply_attacks(self) :
        #applique le mouvement des boules de feu et les supprime si elles sortent de la fenêtre
        for fireball in self.all_fireballs :
            fireball.move()

            if fireball.rect.x > 1080 or fireball.rect.x < 0 or fireball.rect.y > 720 or fireball.rect.y < 0 :
                self.all_fireballs.remove(fireball)

        #applique l'animation de l'onde de choc 
        if self.onde : 
            if self.onde_time_animation() : 
                self.onde_images_index += 1
                self.onde_last_image_time = pygame.time.get_ticks()

            if self.onde_images_index >= len(self.onde_images) :
                self.onde = False
                self.onde_images_index = 0
            else : 
                self.onde_image = self.onde_images[self.onde_images_index]
                self.onde_image = pygame.transform.scale(self.onde_image, (500, 500))
                if self.left :
                    self.onde_image = pygame.transform.flip(self.onde_image, False, True)

    #dessine les boules de feu et les images de l'attaque de corps à corps
    def draw_attack(self) :
        #affiche les projectiles
        self.all_fireballs.draw(self.screen)

        #onde de choc
        if self.onde :
            self.screen.blit(self.onde_image, (self.rect.center[0] - 250, self.rect.center[1] - 250))

    #invoque des monstres
    def invocation(self) :
        if self.run == False and len(self.enemies) == 0 :
            for i in range(random.randint(1, 2)) :
                self.enemies.add(random.choice(self.types_monsters)(self.screen, self.rect.center))

    #dans un cas spécial, le boss téléporte le joueur à son point d'apparition et fait apparaître des monstres autour du joueur
    def player_teleportation(self) :
        if self.run == False and self.pv/self.max_pv <= 0.25 and self.trajectory_projectile == False and self.trajectory_movement == True and self.player_teleportation_counter > 0 :
            self.player_teleportation_counter -= 1
            self.player.rect.midbottom = self.coords
            self.player.move_feet()
            self.player.move_weapon()
            self.player.move_health_bar()
            rect = pygame.rect.Rect(0, 0, 50, 50)
            rect.center = self.coords
            for point in [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft] :
                self.enemies.add(random.choice(self.types_monsters)(self.screen, point))

    #fonction indépendante de la classe game ou level et qui permet d'appliquer une partie des mouvements et actions du boss final
    def apply(self, collisions, verification) :
        if self.pv <= 0 and not(self.death):
            self.boss_death()

        if not(self.death) :
            angle = 0
            if self.player.rect.centerx < self.rect.centerx or self.left == True:
                angle = 180
            coords_tir = get_position(self.rect.center[0], self.rect.center[1], self.coords_tir[0], self.coords_tir[1], angle, True)
            direction_attaque = trajectory_projectile(collisions, coords_tir, self.fireball.get_rect(), self.v_fireball, self.player.rect)
            
            if direction_attaque and not(self.attack1 or self.attack2):
                self.trajectory_projectile = True
            elif not(self.rect.colliderect(self.player.rect)) :
                self.trajectory_projectile = False
                direction_movement = trajectory_movement(collisions, self, self.player.rect)

                if direction_movement != None :
                    self.trajectory_movement = True
                    move = vecteur(self.rect.center, self.player.rect.center, self.speed)
                    x = move[0]
                    y = move[1]

                    if not(verification(self, x, 0)) :
                        x = 0
                    if not(verification(self, 0, y)) :
                        y = 0

                    if x == 0 and abs(y) > 0.05 :
                        y = self.speed*(y/abs(y)) #y/abs(y) : sert à garder le signe
                    elif y == 0 and abs(x) > 0.05 :
                        x = self.speed*(x/abs(x)) 

                    self.move(x, y)

                else : 
                    self.trajectory_movement = False

            self.attack(collisions)

    #mort du boss
    def boss_death(self) : 
        if not(self.death) :
            self.death = True
            self.image_index = 0
            sound.boss_death_sound.play()

    #retourne True si le délai de l'attaque 1 est passé
    def return_attack_delay_1(self) :
        return ((pygame.time.get_ticks() - self.t_attack_1) >= self.attack_delay_1)
    
    #retourne True si le délai de l'attaque 2 est passé
    def return_attack_delay_2(self) :
        return ((pygame.time.get_ticks() - self.t_attack_2) >= self.attack_delay_2)
    
    #retourne True si le délai de changement d'image de l'onde de choc est passé
    def onde_time_animation(self) : 
        return (pygame.time.get_ticks() - self.onde_last_image_time >= self.onde_animation_time)
        

