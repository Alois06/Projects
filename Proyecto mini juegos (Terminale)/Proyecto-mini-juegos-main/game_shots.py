import pygame
import random
import math

from sound import sound
from objects import PlayerShooter, Obstacle, ObstacleMouvant, ObstacleRebond
import tools

#classe de la partie normale
class Game :
    def __init__(self, screen:pygame.surface.Surface, police1:pygame.font.Font, police2:pygame.font.Font, police3:pygame.font.Font, police4:pygame.font.Font) :
        self.screen = screen

        #l'état de la partie -> True : la partie est en cours | False : la partie n'est pas/plus en cours
        self.etat = False

        #indique True si la partie se termine et False si elle ne s'est pas encore terminée
        self.game_over_etat = False

        #polices
        self.police1 = police1
        self.police2 = police2
        self.police3 = police3
        self.police4 = police4

        #variables de temps
        self.time_start = pygame.time.get_ticks()
        self.time_start_game_over = None
        self.end_countdown_delay = 5000

        #acceleration
        self.coeff_acceleration = 0.00001

        #image de fond d'écran
        self.background = pygame.image.load("assets/background_désert.PNG")
        self.background = pygame.transform.scale(self.background, (1080, 720))

        #image du cactus
        self.image_cactus = pygame.image.load("assets/cactus.png").subsurface(80, 52, 376, 420)
        self.image_cactus = pygame.transform.scale(self.image_cactus, (72, 80))

        #joueurs
        self.player1 = None
        self.player2 = None

        self.vainqueur = 0

        #obstacles
        self.walls = []

        #création des joueurs et des obstacles
        self.create_players()
        self.create_obstacles()

    #création des deux joueurs
    def create_players(self) : 
        #image_players = pygame.image.load("assets/cowboy.png").subsurface(32, 32, 176, 264)
        image_players = pygame.image.load("assets/cowboy.png").subsurface(32, 32, 660, 990)

        image1 = image_players.copy()
        image1 = pygame.transform.scale(image_players, (72, 96))
        image1.set_colorkey((255, 255, 255))
        self.player1 = PlayerShooter(self.screen, image1, (80, 360))

        image2 = image1.copy()
        image2 = pygame.transform.flip(image2, True, False)
        image2.set_colorkey((255, 255, 255))
        self.player2 = PlayerShooter(self.screen, image2, (1000, 360))

    #création des obstacles
    def create_obstacles(self) : 

        #obstacles mouvants
        surface = pygame.surface.Surface((25, 125))
        surface.fill((255, 230, 100))
        self.walls.append(ObstacleMouvant(self.screen, surface, (450, 320), 0, -1, 5, 400))
        self.walls.append(ObstacleMouvant(self.screen, surface, (630, 400), 0, 1, 5, 400))

        #obstacles normaux à rebonds
        surfaces = [[225, 120, 150, 480], [705, 120, 150, 480]]
        for s in surfaces : 
            for i in range(random.randint (1, 3)) : 
                x = random.randint(s[0], s[0] + s[2])
                y = random.randint(s[1], s[1] + s[3])
                self.walls.append(ObstacleRebond(self.screen, self.image_cactus, (x,y)))

    #active le début de la partie et change les sons
    def set(self) : 
        #change l'état de la partie à True pour l'activer
        self.etat = True

        #lance la musique de la partie
        sound.background_music.stop()
        sound.game_music4.play(loops=-1)

    #active la fin de la partie et le retour au menu principal et change les sons
    def unset(self) :
        #change l'état de la partie à False pour la quitter et revenir au menu principal
        self.etat = False

        #stop tous les sons et relance le son du menu principal
        sound.game_music4.stop()
        sound.victory_sound.stop()
        sound.defeat_sound.stop()
        sound.background_music.play(loops=-1)

    #affiche les éléments de la partie
    def draw(self) :

        #affiche le fond d'écran
        self.screen.blit(self.background, (0,0))

        #affichage de la partie tant que celle-ci n'est pas finie
        if not(self.game_over_etat) : 

            #affiche les obstacles
            for obstacle in self.walls : 
                obstacle.draw()
            
            #affiche les deux joueurs
            self.player1.draw()
            self.player2.draw()

            #affichage des projectiles
            for bullet in self.player1.projectiles :
                bullet.draw()
            for bullet in self.player2.projectiles :
                bullet.draw()

        else : 
            txt = self.police4.render("PLAYER " + str(self.vainqueur) + " WON !", False, (255, 255, 255))
            self.screen.blit(txt, (360, 300))

    #applique les actions de la partie
    def apply(self) :

        #actions de la partie tant que celle-ci n'est pas finie
        if not(self.game_over_etat) : 

            #accélération
            self.acceleration()

            #applique les actions des obstacles
            for obstacle in self.walls : 
                if type(obstacle) == ObstacleMouvant : 
                    obstacle.apply()

            #applique les actions des joueurs
            self.player1.apply()
            self.player2.apply()

            #mouvement des projectiles
            self.apply_projectiles(self.player1)
            self.apply_projectiles(self.player2)

            #fin de la partie
            if self.player1.life <= 0 : 
                self.game_over(2)
            elif self.player2.life <= 0 : 
                self.game_over(1)

        else : 
            if self.end_countdown() == True : 
                self.unset()

    #applique le déplacement et les collisions des projectiles du joueur donné en paramètre
    def apply_projectiles(self, player:PlayerShooter) : 

        for bullet in player.projectiles : 

            bullet.apply(self.walls)

            if pygame.sprite.collide_mask(bullet, self.player1) : 
                player.projectiles.remove(bullet)
                self.player1.life -= 1
                sound.explosion_sound.play()

            elif pygame.sprite.collide_mask(bullet, self.player2) :
                #bullet.rect.colliderect(self.player2.rect) : 
                player.projectiles.remove(bullet)
                self.player2.life -= 1
                sound.explosion_sound.play()

            elif bullet.rect.left <= 0 or bullet.rect.right >= 1080 :
                player.projectiles.remove(bullet)
                sound.explosion_sound.play()

    #contrôle les évènements en lien avec la partie
    def manage_events(self, event) : 
        if event.type == pygame.KEYDOWN : 
            #bouton du joueur 1
            if event.key == pygame.K_a : 
                self.player1.attack()
            #bouton du joueur 2
            elif event.key == pygame.K_p : 
                self.player2.attack()

    #initie la fin de partie
    def game_over(self, joueur) : 
        #indique que la partie est terminée
        self.game_over_etat = True

        self.time_start_game_over = pygame.time.get_ticks()

        #sons
        sound.game_music4.stop()
        sound.victory_sound.play()

        #enregistre le joueur vainqueur
        self.vainqueur = joueur

    #renvoie True si le délai pour l'affichage de fin de partie s'est achevé
    def end_countdown(self) : 
        return pygame.time.get_ticks() - self.time_start_game_over >= self.end_countdown_delay 
    
    def acceleration(self) : 
        #calcul du coeff d'accélération
        a = 1 + self.coeff_acceleration*(pygame.time.get_ticks() - self.time_start)

        #application du coeff
        if a <= 2 : 

            #aux projectiles
            for bullet in (self.player1.projectiles + self.player2.projectiles) : 
                bullet.a = a

            #aux joueurs
            self.player1.a = a
            self.player2.a = a

            #aux obstacles mouvant
            for obstacle in self.walls : 
                if type(obstacle) == ObstacleMouvant : 
                    obstacle.a = a


#classe pour la game en solo contre un bot
class GameSolo(Game) : 
    def __init__(self, screen, police1, police2, police3, police4):
        super().__init__(screen, police1, police2, police3, police4)

        #player 1 est le joueur
        #player 2 est l'ia

    #affiche les éléments de la partie à l'écran
    def draw(self) :
        
        #affiche le fond d'écran
        self.screen.blit(self.background, (0,0))

        #affichage de la partie tant que celle-ci n'est pas finie
        if not(self.game_over_etat) : 
            super().draw()
        else : 
            txt = ""
            if self.vainqueur == 1 : 
                txt = self.police4.render("YOU WON !", False, (255, 255, 255))
            else : 
                txt = self.police4.render("YOU LOSE !", False, (255, 255, 255))
            self.screen.blit(txt, (400, 300))

    #applique les actions de la partie
    def apply(self):

        if not(self.game_over_etat) :
            self.ia_move()

        super().apply()

    #gère les évènements de la partie
    def manage_events(self, event):
        #tir du joueur
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_SPACE : 
                self.player1.attack()

    #fonction de fin de partie
    def game_over(self, joueur):
        self.game_over_etat = True
        self.time_start_game_over = pygame.time.get_ticks()
        
        #enregistre le joueur vainqueur
        self.vainqueur = joueur

        #sons
        sound.game_music4.stop()
        if joueur == 1 : 
            sound.victory_sound.play()
        else : 
            sound.defeat_sound.play()

    #gère les déplacements et actions de l'ia
    def ia_move(self) : 

        #récupération des informations sur les projectiles
        data = self.recup_data()

        #on fait bouger le bot en fonction de ces informations
        self.apply_ia_move(data)

    #récupères les informations sur les projectiles
    def recup_data(self) : 
        #listes récupérant les données des projectiles (distance, différence en y, coefficients de "dangerosité" et future coordonnée y)
        liste_d = []
        liste_dy = []
        coeffs = []
        liste_y = []

        #on étudie la position et autres caractéristiques des projectiles pour les éviter
        for bullet in self.player1.projectiles + self.player2.projectiles : 

            #on calcule la position future du projectile en x = 950
            prediction = tools.prediction(bullet.rect.copy(), bullet.vx, bullet.vy, 1, 950, self.walls, 15)

            if prediction[1] > 0 : 
                future_y_coords = tools.find_y(prediction[0], 950, prediction[1], prediction[2])
                liste_y.append(future_y_coords)

                #on détermine la distance entre la balle et sa future position
                norme = tools.norme(prediction[0], (950, future_y_coords))

                #on détermine l'écart entre l'ordonnée du personnage de l'ia et la future ordonnée du projectile
                dy = future_y_coords - self.player2.rect.centery

                liste_d.append(norme)
                liste_dy.append(dy)
                coeffs.append(norme**2 + dy)
        
        return [liste_d, liste_dy, coeffs, liste_y]

    #déplacement du bot pour soit éviter les projectiles soit attaquer le joueur
    def apply_ia_move(self, data:list) : 

        #on fait bouger le personnage pour éviter les balles
        min_dy = 0 
        min_coeff = 0
        if len(data[2]) > 0 :
            min_coeff = min(data[2])
            min_dy = data[1][data[2].index(min_coeff)]
            min_y = data[3][data[2].index(min_coeff)]

            verfication = tools.verification(self.walls, self.player2.coords_tirs, self.player2.image_projectile.get_rect(), -15, 750)

            if abs(min_dy) <= 250 and not((self.player2.rect.bottom <= 150 or self.player2.rect.top >= 570) and not(verfication)): 
                
                #dans la zone en dessous de y = 570 :
                if min_y >= 570 : 
                    if self.player2.vy > 0 :
                        self.player2.attack()

                #dans la zone au dessus de y = 150 :
                elif min_y <= 150 : 
                    if self.player2.vy < 0 :
                        self.player2.attack()

                #sinon : mouvement pour éviter le projectile le plus dangereux
                else :
                    if min_dy <= 0 and self.player2.vy < 0 :
                        self.player2.attack()
                
                    elif min_dy > 0 and self.player2.vy > 0 :
                        self.player2.attack()
        else : 
            min_dy = 720
            min_coeff = 720

        #déplacement pour tirer
        if self.player2.delay() and min_coeff >= 300 and abs(min_dy) >= 150 and tools.verification(self.walls, self.player2.coords_tirs, self.player2.image_projectile.get_rect(), -15, 500) :
            if self.player1.rect.top > self.player2.rect.bottom and self.player1.vy < 0 :
                self.player2.attack()
            elif self.player1.rect.bottom < self.player2.rect.top and self.player1.vy > 0 : 
                self.player2.attack()