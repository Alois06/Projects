import pygame
from tools import *
from projectile import Projectile
from sound import sound

# Classe Weapon qui contient les attributs communs à toutes les armes (classe mère)
class Weapon(pygame.sprite.Sprite) :
    def __init__(self, screen, coords, image) :
        super().__init__()
        self.screen = screen
        self.origin_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.mask = pygame.mask.from_surface(self.image)
        self.rect_size = ((self.rect.right - self.rect.x), (self.rect.bottom - self.rect.y))
        self.angle = 0

    #dessine l'image de l'arme sur la fenêtre
    def draw(self) :
        self.screen.blit(self.image, self.rect)

    #bouge l'armes aux coordonnées
    def move_at(self, coords) :
        self.rect.center = coords

    #tourne l'arme
    def turn(self, angle) :
        self.image = self.origin_image
        self.angle = angle

        if angle > 90 or angle < -90 :
            self.image = pygame.transform.flip(self.image, False, True)

        self.image = pygame.transform.rotate(self.image, self.angle)
        coords = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.mask = pygame.mask.from_surface(self.image)

# Classes des armes : pistolet, arc, épée, potions et portail

class Gun(Weapon) :

    def __init__(self, screen, coords, properties) : 
        self.image = properties["image"] #image
        self.reload_time = properties["reload_time"] #temps de recharge
        self.damage = properties["damage"] #dégâts
        
        super().__init__(screen, coords, self.image) 

        #coordonnées de la sortie du projectile
        self.coords_tir = properties["coords_projectile"]

        #projectile
        self.v = properties["projectile"]["speed"] #vitesse du projectile
        self.img_projectile = properties["projectile"]["img"] #image du projectile
        self.type_damage = properties["projectile"]["type_damage"] #type de dégâts (unité ou de zone)
        self.all_projectiles = pygame.sprite.Group() #groupe de sprites contenant tous les projectiles

        #reload
        self.t_attack = 0

    #fonction qui déclenche une attaque en créant un projectile
    def attack(self, objectif, collisions) :
        if self.reload() :
            #son du tir
            sound.shoot_sound.play()

            #définir la direction de la balle
            pos = self.rect.center #à revoir
            direction = vecteur(pos, objectif, self.v)
            angle = get_angle(direction[0], direction[1])

            #tourner l'arme
            self.turn(angle)

            #défini les coordonnées du tir

            coords_tir = get_position(self.rect.center[0], self.rect.center[1], self.coords_tir[0], self.coords_tir[1], self.angle, True)
            direction = vecteur(coords_tir, objectif, self.v)

            #création du projectile
            self.all_projectiles.add(Projectile(self.img_projectile, coords_tir, direction, collisions))

            #reload
            self.t_attack = pygame.time.get_ticks()

    #affiche les projectiles
    def draw_attack(self) :
        
        self.all_projectiles.draw(self.screen)

    #applique le déplacement des projectiles
    def apply_attacks(self, collisions) :
        #mouvement des projectiles
        for projectile in self.all_projectiles : 
            projectile.move()

            #si un projectile se retrouve hors de la fenêtre : le supprimer
            if projectile.rect.x > 1080 or projectile.rect.x < 0 or projectile.rect.y > 720 or projectile.rect.y < 0 :
                self.all_projectiles.remove(projectile)

    #retourne si le temps de recharge de l'arme est fini ou non
    def reload(self) :
        return (pygame.time.get_ticks() - self.t_attack >= self.reload_time)

class Bow(Weapon) :
    def __init__(self, screen, coords, properties):
        self.images = properties["image"] 
        self.images_table = properties["tables"]

        self.reload_time = properties["reload_time"]
        self.charging_time = properties["charging_time"]
        self.damage = properties["damage"]

        #coordonnées de la sortie du projectile
        self.coords_tir = properties["coords_projectile"]

        #projectile
        self.v = properties["projectile"]["speed"]
        self.img_projectile = properties["projectile"]["img"]
        self.type_damage = properties["projectile"]["type_damage"]
        self.all_projectiles = pygame.sprite.Group()

        #recharge de l'arc
        self.t_attack = 0
        self.attack_on = False
        self.objectif = None

        super().__init__(screen, coords, pygame.transform.scale_by(self.images.subsurface(self.images_table[0]), 1.5))

    def new_image(self, index) :
        self.image = self.images.subsurface(self.images_table[index])
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.origin_image = self.image
        self.image = pygame.transform.rotate(self.image, self.angle)
    
    #change l'image de l'arc en fonction du temps de chargement
    def change_image(self) :
        if self.charging() < self.charging_time/3 or self.charging() >= self.charging_time :
            self.new_image(0)

        elif self.charging() >= self.charging_time*2/3 :
            self.new_image(2)

        elif self.charging() >= self.charging_time/3  :
            self.new_image(1)
    
    #fonction qui lance une attaque ou actualise la cible
    def attack(self, objectif, son) :
        self.objectif = objectif

        if not(self.attack_on) and self.reload() :
            self.t_attack = pygame.time.get_ticks()
            self.attack_on = True
            if son == True :
                sound.bow_sound.play()

    #affiche les projectiles
    def draw_attack(self) :
        
        self.all_projectiles.draw(self.screen)

    #fonction qui applique les déplacements des flèches et l'arc en cas d'attaque en cours
    def apply_attacks(self, collisions) :

        #si une attaque est en cours : tourne l'arc en fonction de l'objectif (qui peut changer), qui actualise le changement d'images et qui lance la flèche lorsque le temps de chargement est terminé
        if self.attack_on : 
            #définir la direction de la balle
            pos = self.rect.center #à revoir
            direction = vecteur(pos, self.objectif, self.v)
            angle = get_angle(direction[0], direction[1])

            #tourner l'arme
            self.turn(angle)

            #si l'arc a fini de se charger
            if self.charging() >= self.charging_time :

                coords_tir = get_position(self.rect.center[0], self.rect.center[1], self.coords_tir[0], self.coords_tir[1], self.angle, True)
                direction = vecteur(coords_tir, self.objectif, self.v)

                #création du projectile
                self.all_projectiles.add(Projectile(self.img_projectile, coords_tir, direction, collisions))

                self.attack_on = False

            self.change_image()

        #mouvement des projectiles
        for projectile in self.all_projectiles : 
            projectile.move()

            if projectile.rect.x > 1080 or projectile.rect.x < 0 or projectile.rect.y > 720 or projectile.rect.y < 0 :
                self.all_projectiles.remove(projectile)
    
    #retourne si le temps de recharge de l'arme est fini ou non
    def reload(self) :
        return pygame.time.get_ticks() - self.t_attack >= self.reload_time
    
    #renvoie le temps depuis lequel l'arc est en train de charger son tir
    def charging(self) :
        return float(pygame.time.get_ticks() - self.t_attack)
    
class Sword(Weapon) :
    def __init__(self, screen, coords, properties) : 
        self.image = properties["image"]
        self.reload_time = properties["reload_time"]
        self.damage = properties["damage"]
        self.range = properties["range"]
        super().__init__(screen, coords, self.image)
        #reload
        self.t_attack = 0

        #image effet d'attaque
        self.effects_images = [] 
        for i in range(1, 11) : 
            self.effects_images.append(pygame.image.load("assets/effets mêlées/img" + str(i) + ".png"))
        self.effects_images_index = 0
        self.animation_time = 50
        self.last_image_time = 0

        self.attack_on = False

    #lance un coup d'épée
    def attack(self, objectif) :
        if self.reload() :
            #définir la direction de l'attaque
            pos = (self.rect.right, self.rect.center[1])
            direction = vecteur(pos, objectif, 1)
            angle = get_angle(direction[0], direction[1])
            #tourner l'arme
            self.turn(angle)
            #reload
            self.t_attack = pygame.time.get_ticks()
            self.attack_on = True
            self.last_image_time = pygame.time.get_ticks()
    
    #affiche l'animation du coup d'épée
    def draw_attack(self) :
        if self.attack_on : 
            if self.time_animation() : 
                self.effects_images_index += 1
                self.last_image_time = pygame.time.get_ticks()

            if self.effects_images_index >= len(self.effects_images) :
                self.attack_on = False
                self.effects_images_index = 0
            else : 
                image = self.effects_images[self.effects_images_index]
                image = pygame.transform.scale(image, (50, 50))
                if self.angle > 90 or self.angle < -90 :
                    image = pygame.transform.flip(image, False, True)
                self.screen.blit(image, self.rect)

    #retourne si le temps de recharge de l'arme est fini ou non
    def reload(self) :
        return (pygame.time.get_ticks() - self.t_attack >= self.reload_time)
    
    #renvoie si le délai entre chaque changement d'image de l'animation du coup d'épée est écoulé
    def time_animation(self) : 
        return (pygame.time.get_ticks() - self.last_image_time >= self.animation_time)

class Potion(Weapon) :
    def __init__(self, screen, coords):
        self.image = pygame.image.load("assets2/Environment/Dungeon Prison/Assets/Props.png").subsurface(0,229,16,11)
        self.image = pygame.transform.scale_by(self.image,2)
        self.healplayer = False
        super().__init__(screen, coords, self.image)
        self.rect.midbottom = coords

    #régénère le joueur
    def heal(self,player) :
        player.pv += 100
        if player.pv > player.max_pv :
            player.pv = player.max_pv
        self.healplayer = True
   
class Portal(Weapon) :
    def __init__(self, screen, coords):
        #création de l'image du portail
        self.image = pygame.image.load("assets/portals.png").subsurface(24,32,160,312)
        self.image = pygame.transform.scale_by(self.image,0.25)

        super().__init__(screen, coords, self.image) #init de la classe mère Weapon
        self.rect.midbottom = coords
        
        sound.portal_apparition_sound.play()

    def move_at(self, coords) :
        self.rect.midbottom = coords
   

