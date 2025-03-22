import pygame
from sound import sound
from tools import vecteur_rayon
from data import change_image_speed
from weapon import Gun, Bow

class Player(pygame.sprite.Sprite) : 
    def __init__(self, screen, coords, image, images, properties, tables) :

        super().__init__()

        self.screen = screen

        #caractéristiques
        self.pv = properties["pv"]
        self.max_pv = properties["pv"]
        self.speed = properties["speed"]
        self.coef_damage = properties["coef_damage"]

        #coordonnées mouvements
        self.v_x = 0
        self.v_y = 0

        #IMAGES

        #images pour chaque actions (sprite sheets)
        self.images_death = pygame.image.load(images+"Death/Death-Sheet.png")
        self.images_idle = pygame.image.load(images+"Idle/Idle-Sheet.png")
        self.images_run = pygame.image.load(images+"Run/Run-Sheet.png")

        #tableaux
        self.images_death_table = tables["death"]
        self.images_idle_table = tables["idle"]
        self.images_run_table = tables["run"]

        ##état : mort ou en mouvement (ou inactif si aucun des deux)
        self.death = False
        self.run = False

        #index de l'image
        self.image_index = 1

        #image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = coords
        self.mask = pygame.mask.from_surface(self.image)

        #image event
        self.CHANGE_IMAGE = pygame.USEREVENT
        pygame.time.set_timer(self.CHANGE_IMAGE, change_image_speed[str(self.speed)])

        #arme
        self.current_weapon = None

        #côté
        self.left = False

        #fin de l'animation de mort
        self.end_death = False

        #pieds pour les collisions
        self.feet = pygame.Rect((0, 0), (round(self.rect.width*0.8), round(self.rect.height/3)))
        self.feet.midbottom = self.rect.midbottom
        self.old_position = self.feet.copy()

        #barre de vie 
        self.health_bar_max = pygame.Rect((0, 0), (round(self.rect.width*0.75), 4))
        self.health_bar_max.midbottom = self.rect.midtop

        self.health_bar = pygame.Rect((0, 0), (self.health_bar_max.width, self.health_bar_max.height))
        self.health_bar.topleft = self.health_bar_max.topleft

        # Variable pour suivre si le joueur était en train de courir lors du dernier frame
        self.prev_run = False
    
    #affiche le joueur à l'écran
    def draw(self) :
        #dessine le personnage
        self.screen.blit(self.image, self.rect)
    
    #affiche la barre de vie du joueur
    def draw_health_bar(self) :
        if not(self.death) : 
            pygame.draw.rect(self.screen, (255, 255, 255), self.health_bar_max, border_radius=2)
            pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar, border_radius=2)

    #actualise la longueur de la barre de vie du joueur
    def actualise_health_bar(self) :
        #nouvelle barre de vie
        t = round(self.pv/self.max_pv, 2)
        self.health_bar = pygame.Rect((0, 0), (self.health_bar_max.width*t, self.health_bar_max.height))
        self.health_bar.topleft = self.health_bar_max.topleft

    #bouge la barre de vie du joueur au dessus de l'image du joueur
    def move_health_bar(self) :
        self.health_bar_max.midbottom = self.rect.midtop
        self.health_bar.topleft = self.health_bar_max.topleft
    
    def life_pv(self): 
        self.pv = self.max_pv

    #permet de créer une nouvelle image
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

    #permet de changer d'animation/image en fonction de l'état du joueur (run, death, etc)
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

    #bouge le joueur aux coordonnées données en paramètres
    def move_at(self, coords) :
        self.rect.midbottom = coords
        #bouge ses pieds
        self.move_feet()
        #bouge l'arme
        self.move_weapon()
        #bouge la barre de vie
        self.move_health_bar()

    #gère les déplacements du joueur
    def move(self) :

        #si le personnage meurt, il ne bouge plus
        if self.death :
            self.v_x = 0
            self.v_y = 0
        else :
            vector = vecteur_rayon(self.v_x, self.v_y, self.speed)
            self.v_x = vector[0]
            self.v_y = vector[1]

        #bouge le personnage
        self.rect.x += self.v_x
        self.rect.y += self.v_y

        #bouge ses pieds
        self.move_feet()

        #bouge l'arme
        self.move_weapon()

        #bouge la barre de vie
        self.move_health_bar()

        #vérifie s'il va à gauche ou à droite
        if self.v_x < 0 :
            if self.left == False :
                self.image = pygame.transform.flip(self.image, True, False)
            self.left = True
        elif self.v_x > 0 :
            if self.left == True :
                self.image = pygame.transform.flip(self.image, True, False)
            self.left = False

        #vérifie s'il court
        if self.v_x == 0 and self.v_y == 0 :
            self.run = False
        else :
            self.run = True

        #met les coordonnées de mouvement à 0
        self.v_x = 0
        self.v_y = 0

        # Si l'état de course a changé depuis le dernier frame
        if self.run != self.prev_run:
            if self.run:
                sound.mvmt_sound.play(loops=-1)  # Jouer le son si le joueur commence à courir
            else:
                sound.mvmt_sound.stop()  # Arrêter le son si le joueur arrête de courir
                
            # Mettre à jour l'état précédent de course
            self.prev_run = self.run
    
    #bouge les pieds et sauvegarde l'ancienne position du joueur
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
        self.move_weapon()

    def move_right(self) :
        self.v_x += self.speed
    def move_left(self) :
        self.v_x -= self.speed
    def move_up(self) :
        self.v_y -= self.speed
    def move_down(self) :
        self.v_y += self.speed
    
    #initie la mort du joueur
    def player_death(self) :
        if not(self.death) :
            self.pv = 0
            self.death = True
            self.image_index = 0
            self.weapon.move_at(self.rect.midbottom)
            sound.mvmt_sound.stop()
    
    def respawn(self) :
        self.pv = self.max_pv
        self.death = False
        self.end_death = False

    def change_weapon(self, weapon) :
        #changer d'arme
        self.weapon = weapon

    #gère les attaques du joueur
    def attack(self, collisions) :
        objectif = pygame.mouse.get_pos()
        if type(self.weapon) == Gun :
            self.weapon.attack(objectif, collisions)
        elif type(self.weapon) == Bow :
            self.weapon.attack(objectif, True)
    
    #bouge l'arme du joueur
    def move_weapon(self) :
        self.weapon.move_at(self.rect.center)