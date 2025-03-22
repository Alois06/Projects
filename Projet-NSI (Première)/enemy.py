import pygame
from tools import *
import data

class Enemy(pygame.sprite.Sprite) :
    def __init__(self, screen, coords, image, images, properties, tables, ID, attack_type, weapon) :
        super().__init__()

        self.screen = screen

        #attributs
        self.pv = properties["pv"]
        self.max_pv = properties["pv"]
        self.speed = properties["speed"]
        self.coef_damage = properties["coef_damage"]

        self.attack_type = attack_type

        #IMAGES

        #images pour chaque actions
        self.images_death = pygame.image.load(images+"Death/Death-Sheet.png")
        self.images_idle = pygame.image.load(images+"Idle/Idle-Sheet.png")
        self.images_run = pygame.image.load(images+"Run/Run-Sheet.png")

        #tableaux
        self.images_death_table = tables["death"]
        self.images_idle_table = tables["idle"]
        self.images_run_table = tables["run"]

        #état : mort ou en mouvement (ou inactif si aucun des deux)
        self.death = False
        self.run = False

        #index de l'image
        self.image_index = 1

        #image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = coords
        self.mask = pygame.mask.from_surface(self.image)

        #event pour le changement d'image
        self.CHANGE_IMAGE = pygame.USEREVENT + ID
        pygame.time.set_timer(self.CHANGE_IMAGE, data.change_image_speed[str(self.speed)])

        #arme
        self.weapon = weapon

        #côté
        self.left = False

        #fin de l'animation de mort
        self.end_death = False

        #pieds pour les collisions
        self.feet = pygame.Rect((self.rect.midleft), (self.rect.width, 0.5*self.rect.height))
        self.old_position = self.feet.copy()

        #delai pour l'attaque
        self.t_attack = 0
        self.attack_delay = properties["attack_delay"]
    
    def draw(self) :
        #dessine le monstre
        self.screen.blit(self.image, self.rect)

    #permet de créer une nouvelle image
    def new_image(self, sprite_sheet, table, index) :

        self.image = sprite_sheet.subsurface(table[index])

        #change la taille de l'image
        self.image = pygame.transform.scale_by(self.image, 1.5)

        #si le personnage va vers la gauche
        if self.left:
            self.image = pygame.transform.flip(self.image, True, False)

        #établit son nouveau rectangle
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.feet.midbottom
        self.mask = pygame.mask.from_surface(self.image)

    #permet de changer d'animation/image en fonction de l'état de l'ennemi (run, death, etc)
    def change_animation(self) :
        
        if not(self.end_death) : 

            #s'il meurt
            if self.death :
                if self.image_index > len(self.images_death_table)-1 :
                    self.end_death = True
                else :
                    self.new_image(self.images_death, self.images_death_table, self.image_index)
                    
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

    #gère les déplacements de l'ennemi
    def move(self, x, y) :

        #si il meurt, il ne bouge plus
        if self.death :
            x = 0
            y = 0

        #bouge l'ennemi
        self.rect.x += x
        self.rect.y += y
        
        #bouge ses pieds
        self.move_feet()

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
        if abs(x) < 0.05 and abs(y) < 0.05 :
            self.run = False
        else :
            self.run = True

        self.move_weapon()

    #bouge l'ennemi aux coordonnées données en paramètres
    def move_at(self, coords) :
        self.rect.midbottom = coords
        #bouge ses pieds
        self.move_feet()
        self.move_weapon()
    
    #bouge les pieds de l'ennemi et sauvegarde son ancienne position
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

    #initie la mort de l'ennemi
    def enemy_death(self) :
        if not(self.death) :
            self.death = True
            self.image_index = 0
            #arme
            self.weapon.rect.center = self.rect.midbottom

    #retourne si le délai entre chaque attaque est fini ou non
    def return_attack_delay(self) :
        return (pygame.time.get_ticks() - self.t_attack >= (self.attack_delay + self.weapon.reload_time))
    
    #bouge l'arme de l'ennemi
    def move_weapon(self) :
        if self.attack_type == "mélée" :
            angle = self.weapon.angle
            if angle >= 0 and angle < 30 :
                self.weapon.rect.center = self.rect.midright
            elif angle >= 30 and angle <= 150 : 
                self.weapon.rect.center = self.rect.midtop
            elif angle > 150 :
                self.weapon.rect.center = self.rect.midleft
            elif angle < 0 : 
                self.weapon.rect.center = self.rect.midbottom

        elif self.attack_type == "tireur" :
            self.weapon.rect.center = self.rect.center


#Types de monstres qui héritent de la classe Enemy

class Orc(Enemy) :
    def __init__(self, screen, coords, type) :

        #images
        images = "assets2/Enemy/Orc Crew/Orc - " + type + "/"
        tables = data.tables_orc[type]["images"]

        img = pygame.image.load(images+"Idle/Idle-Sheet.png").subsurface(tables["idle"][0])
        img = pygame.transform.scale_by(img, 1.5)

        #propriétés
        properties = data.tables_orc[type]["properties"]

        #id de l'animation
        ID = properties["id"]

        #arme
        self.weapon = properties["weapon"]["type"](screen, (0,0), properties["weapon"]["properties"])

        super().__init__(screen, coords, img, images, properties, tables, ID, "mélée", self.weapon)

    #gère les attaques des orcs (attaques de corps à corps)
    def attack(self, player, collisions) :
        if (self.rect.colliderect(player.rect) or self.weapon.rect.colliderect(player.rect)) and type(trajectory_movement(collisions, self, player.rect)) == dict :
            if self.return_attack_delay() :
                self.weapon.attack(player.rect.center)
                player.pv -= self.weapon.damage * self.coef_damage
                self.t_attack = pygame.time.get_ticks()
                self.move_weapon()


class Skeleton(Enemy) :
    def __init__(self, screen, coords, type) :

        #images
        images = "assets2/Enemy/Skeleton Crew/Skeleton - " + type + "/"
        tables = data.tables_skeleton[type]["images"]

        img = pygame.image.load(images+"Idle/Idle-Sheet.png").subsurface(tables["idle"][0])
        img = pygame.transform.scale_by(img, 1.5)

        #propriétés
        properties = data.tables_skeleton[type]["properties"]

        #id de l'animation
        ID = properties["id"]

        #arme
        self.weapon = properties["weapon"]["type"](screen, (0,0), properties["weapon"]["properties"])

        super().__init__(screen, coords, img, images, properties, tables, ID, "tireur", self.weapon)
    
    #gère les attaques des squelettes (attaques à distance)
    def attack(self, player, collisions): #longue distance
        if_direction = trajectory_projectile(collisions, self.rect.center, self.weapon.img_projectile.get_rect(), self.weapon.v, player.rect) 
        if if_direction == True and self.return_attack_delay() :
            self.t_attack = pygame.time.get_ticks()
            objectif = player.rect.center
            self.weapon.attack(objectif, False)

        elif self.weapon.attack_on :
            objectif = player.rect.center
            self.weapon.attack(objectif, False)


#classes qui héritent des classes Skeleton et Orc
        
#Orcs
class OrcBase(Orc) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Base")

class OrcRogue(Orc) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Rogue")

class OrcShaman(Orc) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Shaman")

class OrcWarrior(Orc) : 
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Warrior")

#Skeletons
class SkeletonBase(Skeleton) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Base")

class SkeletonRogue(Skeleton) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Rogue")   

class SkeletonShaman(Skeleton) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Shaman")   

class SkeletonWarrior(Skeleton) :
    def __init__(self, screen, coords):
        super().__init__(screen, coords, "Warrior")       