import pygame
import random
import math
import tools
from sound import sound

#Objets pour le jeu de raquette

#classe de la balle pour le jeu de raquettes
class Ball(pygame.sprite.Sprite) :
    def __init__(self, screen, image: pygame.Surface, coords) :

        super().__init__()

        self.screen = screen

        #création de la balle
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords

        #vecteur déplacement
        lx = [-x for x in range(2, 6)] + [x for x in range (2, 6)]
        ly = [-y for y in range(2, 6)] + [y for y in range (2, 6)]
        self.vx = lx[random.randint(0, 7)]
        self.vy = ly[random.randint(0, 7)]

        #vitesse et accélération
        self.v = math.sqrt(self.vx**2 + self.vy**2)
        self.a = 1

    #Bouge la balle en x et en y
    def move(self) : 
        self.rect.x += (self.vx*self.a)/int(self.a)
        self.rect.y += (self.vy*self.a)/int(self.a)
        self.v = math.sqrt((self.vx*self.a)**2 + (self.vy*self.a)**2)

    #vérifie les collisions et applique le mouvement de la balle
    def apply(self, walls: list, rackets: list) :

        for f in range(int(self.a)) : 

            #vérifie si la balle touche les bords de l'écran
            self.collisions_bords()
            
            #vérifie si la balle touche un obstacle
            if self.rect.collidelist(walls + rackets) >= 0 :
                self.collisions(walls, rackets) 

            #Applique le mouvement de la balle
            self.move()
    
    def collisions_bords(self) :
        if self.rect.top <= 0 or self.rect.bottom >= 720 or self.rect.left <= 0 or self.rect.right >= 1080 :
            if sound.ball_sound.get_num_channels() == 0 :
                sound.ball_sound.play()

            if self.rect.top <= 0 :
                self.vy = abs(self.vy)
                
            elif self.rect.bottom >= 720: 
                self.vy = -abs(self.vy)

            if self.rect.left <= 0 or self.rect.right >= 1080 :
                self.vx = 0

    def collisions(self, walls:list, rackets:list) : 
        for obstacle in walls + rackets : 

            obstacle_obj = obstacle
            obstacle = obstacle.rect

            original_vx = self.vx
            original_vy = self.vy

            if self.rect.colliderect(obstacle) :

                if sound.ball_sound.get_num_channels() == 0 :
                    sound.ball_sound.play()

                #Touche le haut ou le bas d'un obstacle
                if (self.rect.left > obstacle.left and self.rect.right < obstacle.right):
                    if self.rect.top > obstacle.top and self.rect.top < obstacle.bottom :
                        self.vy = abs(self.vy)
                    elif self.rect.bottom > obstacle.top and self.rect.bottom < obstacle.bottom : 
                        self.vy = -abs(self.vy)
                
                #Touche le côté gauche ou droite d'un obstacle
                if self.rect.top > obstacle.top and self.rect.bottom < obstacle.bottom : 
                    if self.rect.left > obstacle.left and self.rect.left < obstacle.right :
                        self.vx = abs(self.vx)
                    elif self.rect.right > obstacle.left and self.rect.right < obstacle.right : 
                        self.vx = -abs(self.vx)

                #Touche un angle
                if original_vx == self.vx and original_vy == self.vy :

                    if self.rect.collidepoint(obstacle.bottomright) : 
                        dx = obstacle.right - self.rect.left
                        dy = obstacle.bottom - self.rect.top

                        if self.vx < 0 and self.vy < 0 and abs(dx-dy) <= 2 :
                            self.vx = abs(self.vx)
                            self.vy = abs(self.vy)
                        elif self.vx < 0 and self.vy > 0 : 
                            self.vx = abs(self.vx)
                        elif self.vx > 0 and self.vy < 0 : 
                            self.vy = abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]
                    
                    if self.rect.collidepoint(obstacle.topright) : 
                        dx = obstacle.right - self.rect.left
                        dy = abs(obstacle.top - self.rect.bottom)
                        
                        if self.vx < 0 and self.vy > 0 and abs(dx-dy) <= 2 :
                            self.vx = abs(self.vx)
                            self.vy = -abs(self.vy)
                        elif self.vx < 0 and self.vy < 0 : 
                            self.vx = abs(self.vx)
                        elif self.vx > 0 and self.vy > 0 : 
                            self.vy = -abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]

                    if self.rect.collidepoint(obstacle.topleft) : 
                        dx = abs(obstacle.left - self.rect.right)
                        dy = abs(obstacle.top - self.rect.bottom)

                        if self.vx > 0 and self.vy > 0 and abs(dx-dy) <= 2 :
                            self.vx = -abs(self.vx)
                            self.vy = -abs(self.vy)
                        elif self.vx > 0 and self.vy < 0 : 
                            self.vx = -abs(self.vx)
                        elif self.vx < 0 and self.vy > 0 : 
                            self.vy = -abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]

                    if self.rect.collidepoint(obstacle.bottomleft) : 
                        dx = abs(obstacle.left - self.rect.right)
                        dy = obstacle.bottom - self.rect.top
                        
                        if self.vx > 0 and self.vy < 0 and abs(dx-dy) <= 2 :
                            self.vx = -abs(self.vx)
                            self.vy = abs(self.vy)
                        elif self.vx > 0 and self.vy > 0 : 
                            self.vx = -abs(self.vx)
                        elif self.vx < 0 and self.vy < 0 : 
                            self.vy = abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.svy = comparaison[0], comparaison[1]
                
                #obstacles avec rebond aléatoire ou téléportation
                if type(obstacle_obj) == ObstacleRebond or type(obstacle_obj) == ObstacleTeleportation :
                    obstacle_obj.effect(self)

                #pour éviter que la balle reste coincée dans un obstacle en mouvement
                elif type(obstacle_obj) == ObstacleMouvant : 
                    for i in range(3) : 
                        self.move()

    #Affiche la balle sur la fenêtre de jeu
    def draw(self) : 
        self.screen.blit(self.image, self.rect)

#classe pour les projectiles
class Projectile(Ball) : 
    def __init__(self, screen, image, coords):
        super().__init__(screen, image, coords)

        #mask du projectile
        self.mask = pygame.mask.from_surface(self.image)

        #sert pour la rotation de l'image
        self.image_origine = image
        self.angle = 0

    def apply(self, walls:list) : 

        #vérifie si la balle touche les bords de l'écran
        self.collisions_bords()
        
        #vérifie si la balle touche un obstacle
        if pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_mask) :
            self.collisions(walls, []) 

        #Applique le mouvement de la balle
        self.move()

        #modification de l'orientation de l'image
        self.angle = tools.return_angle(self.vx, self.vy)
        img = self.image_origine.copy()
        img = pygame.transform.rotate(img, self.angle*(-1))
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)

        #nouveau rectangle
        coords = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = coords

#classe mère pour les sprites bougeant de haut en bas (raquettes, joueurs tirs, etc)
class SpriteY(pygame.sprite.Sprite) :
    def __init__(self, screen, image: pygame.Surface, coords) :
        super().__init__()

        self.screen = screen

        #création du sprite
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords

        self.mask = pygame.mask.from_surface(self.image)

        #vecteur déplacement
        self.vy = -5

    def draw(self) : 
        self.screen.blit(self.image, self.rect)

    def move(self) :
        self.rect.y += self.vy
    
    def apply(self) : 
        if self.rect.bottom >= 720 :
            self.vy = -abs(self.vy)
        elif self.rect.top <= 0 :
            self.vy = abs(self.vy)

        self.move()    

#classe de la raquette pour le jeu de tennis
class Racket(SpriteY) : 
    def __init__(self, screen, image: pygame.Surface, coords):
        super().__init__(screen, image, coords)

        #accélération
        self.a = 1

    def move(self) :
        self.rect.y += self.vy*self.a

#classe du joueur pour le jeu de tir
class PlayerShooter(SpriteY) : 
    def __init__(self, screen, image: pygame.Surface, coords):
        super().__init__(screen, image, coords)

        #vie du joueur
        self.life = 3

        #projectiles
        self.image_projectile = pygame.image.load("assets/bullet.png")
        self.image_projectile = self.image_projectile.subsurface((256, 90, 152, 64))
        self.image_projectile = pygame.transform.scale(self.image_projectile, (48, 20))
        self.image_projectile.set_colorkey((0,0,0))
        self.projectiles = []
        self.time_last_shot = pygame.time.get_ticks()
        self.max_projectiles = 5

        self.coords_tirs = ()

        #direction de la balle
        self.coeff_directeur = 1
        if coords[0] > 540 : 
            self.coeff_directeur = -1

        self.actualize_coords_tirs()

        #accélération
        self.a = 1

    def move(self) :
        self.rect.y += self.vy*self.a

    def apply(self):
        super().apply()

    def actualize_coords_tirs(self) : 
        self.coords_tirs = (self.rect.x + 126, self.rect.y + 60)
        if self.rect.x > 540 : 
            self.coords_tirs = (self.rect.right - 126, self.rect.y + 60)

    def attack(self) : 
        #inverse le sens du mouvement
        self.vy *= -1
        #lance un projectile
        if self.delay() and len(self.projectiles) < self.max_projectiles : 
            self.time_last_shot = pygame.time.get_ticks()
            self.actualize_coords_tirs()
            projectile = Projectile(self.screen, self.image_projectile, self.coords_tirs)
            projectile.vx = 5*self.coeff_directeur
            projectile.vy = 0
            self.projectiles.append(projectile)
            sound.shot_sound.play()

    def delay(self) : 
        return pygame.time.get_ticks() - self.time_last_shot >= 750

#classe mère obstacle
class Obstacle(pygame.sprite.Sprite) :
    def __init__(self, screen, image:pygame.surface.Surface, coords) :

        super().__init__()

        self.screen = screen

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords

        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self) : 
        self.screen.blit(self.image, self.rect)

    def move(self, coords) : 
        self.rect.center = coords

class ObstacleRebond(Obstacle) :
    def __init__(self, screen, image, coords):
        super().__init__(screen, image, coords)

    def effect(self, ball:Ball) :

        if ball.vx != 0 :
            x_sign = ball.vx/abs(ball.vx)
        else : 
            x_sign = 1

        if ball.vy != 0 :
            y_sign = ball.vy/abs(ball.vy)
        else : 
            y_sign = 1

        ball.vx = random.randint(2, 5)*x_sign
        ball.vy = random.randint(2, 5)*y_sign

class ObstacleTeleportation(Obstacle) :
    def __init__(self, screen, image, coords, coords_tp):
        super().__init__(screen, image, coords)

        self.coords_tp = coords_tp

    def effect(self, ball:Ball) :
        ball.rect.center = self.coords_tp
        ball.vx = random.randint(2, 5)*[-1, 1][random.randint(0, 1)]
        ball.vy = random.randint(2, 5)*[-1, 1][random.randint(0, 1)]

class ObstacleMouvant(Obstacle) :
    def __init__(self, screen, image, coords, cos, sin, v, d_trajectoire):
        super().__init__(screen, image, coords)

        #coordonnées du mouvement
        self.vx = cos*v
        self.vy = sin*v

        if cos != 0 :
            self.sign_cos = cos/abs(cos)
        else : 
            self.sign_cos = 1

        if sin != 0 :
            self.sign_sin = sin/abs(sin)
        else : 
            self.sign_sin = 1
        
        #coordonnées des deux bouts de la trajectoire
        self.coords_max = (int(cos*(d_trajectoire/2) + coords[0]), int(sin*(d_trajectoire/2) + coords[1]))
        self.coords_min = (int(-cos*(d_trajectoire/2) + coords[0]), int(-sin*(d_trajectoire/2) + coords[1]))
        
        xs = [self.coords_max[0], self.coords_min[0]]
        ys = [self.coords_max[1], self.coords_min[1]]
        self.xmax, self.xmin = max(xs), min(xs)
        self.ymax, self.ymin = max(ys), min(ys)

        #rect trajectoire
        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin
        self.rect_trajectoire = pygame.rect.Rect(self.xmin, self.ymin, dx, dy)

        #accélération
        self.a = 1

    def move(self) :
        self.rect.x += self.vx*self.a
        self.rect.y += self.vy*self.a

    def apply(self) :
        if not(self.rect_trajectoire.collidepoint(self.rect.center)) :
            if ((self.rect.center[0] < self.xmin and self.sign_cos < 0) or (self.rect.center[0] > self.xmax and self.sign_cos > 0)) or (self.rect.center[1] < self.ymin and self.sign_sin < 0) or (self.rect.center[1] > self.ymax and self.sign_sin > 0) :
                self.vx = -self.sign_cos*abs(self.vx)
                self.vy = -self.sign_sin*abs(self.vy)
            elif (self.rect.center[0] < self.xmin and self.sign_cos > 0) or (self.rect.center[0] > self.xmax and self.sign_cos < 0) or (self.rect.center[1] < self.ymin and self.sign_sin > 0) or (self.rect.center[1] > self.ymax and self.sign_sin < 0) :
                self.vx = self.sign_cos*abs(self.vx)
                self.vy = self.sign_sin*abs(self.vy)

        self.move()
