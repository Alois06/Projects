import pygame
import random
import math

from objects import Ball, Racket, Obstacle, ObstacleRebond, ObstacleTeleportation, ObstacleMouvant
from sound import sound
import tools

#classe de la partie normale
class Game :
    def __init__(self, screen, police1, police2, police3, police4) :
        self.screen = screen

        self.etat = False

        self.police1 = police1
        self.police2 = police2
        self.police3 = police3
        self.police4 = police4

        #variables de temps
        self.time_init = pygame.time.get_ticks()
        self.timer = 0
        self.timer_save = self.timer
        self.time_up_acceleration = 3
        self.game_duration = 150

        self.start = False

        #game over
        self.game_over = False
        self.game_over_surface = pygame.surface.Surface((1080, 720))
        self.game_over_surface.fill((0, 0, 255))

        #score
        self.player1_score = 0
        self.player2_score = 0

        #création de la balle
        self.ball = None
        self.create_ball()

        #création des raquettes
        self.racket1 = None
        self.racket2 = None
        self.create_rackets()

        #création des obstacles : 
        self.walls = pygame.sprite.Group()
        self.create_walls()

    def create_ball(self) :
        ball_circle = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(ball_circle, (255, 0, 0), (10, 10), 10)
        self.ball = Ball(self.screen, ball_circle, (540, 360))

    def create_rackets(self) :
        #création de la raquette du joueur 1
        racket1_rect = pygame.Surface((15, 100))
        pygame.draw.rect(racket1_rect, (0, 0, 255), (0, 0, 15, 100))
        self.racket1 = Racket(self.screen, racket1_rect, (30, 360))

        #création de la raquette du joueur 2
        racket2 = pygame.Surface((15, 100))
        pygame.draw.rect(racket2, (0, 0, 255), (0, 0, 15, 100))
        self.racket2 = Racket(self.screen, racket2, (1050, 360))

    def create_walls(self) :

        #obstacles normaux
        zones = [[(260, 480), (35, 685)], [(135, 945), (160, 270)], [(135, 945), (450, 560)], [(600, 820), (35, 685)]]
        for zone in zones : 
            for i in range(2) : 
                surface = pygame.surface.Surface((random.randint(50, 75), random.randint(50, 75)))
                surface.fill((200, 200, 0))
                coords = (random.randint(zone[0][0], zone[0][1]), random.randint(zone[1][0], zone[1][1]))
                self.walls.add(Obstacle(self.screen, image=surface, coords=coords))
            
        #obstacles rebonds aléatoire 
        for pos in [(200, 100), (200, 620), (880, 620), (880, 100)] :
            radius = 25
            surface = pygame.surface.Surface((radius*2, radius*2))
            pygame.draw.circle(surface, (255, 100, 10), (radius, radius), radius)
            surface.set_colorkey(0)
            self.walls.add(ObstacleRebond(self.screen, image=surface, coords=pos))

        #obstacles téléportation de la balle
        for pos in [(540, 100), (540, 620)] : 
            radius = 20
            surface = pygame.surface.Surface((radius*2, radius*2))
            pygame.draw.circle(surface, (125, 100, 255), (radius, radius), radius)
            surface.set_colorkey(0)
            self.walls.add(ObstacleTeleportation(self.screen, image=surface, coords=pos, coords_tp=(540, 360)))

        #obstacles en mouvement
        for pos in [(300, 360), (780, 360)] : #(540, 200), (540, 520),
            size = random.randint(75, 125)
            size_angle = random.randint(15, 75)*math.pi/180
            width = math.cos(size_angle)*size
            height = math.sin(size_angle)*size
            surface = pygame.surface.Surface((width, height))
            surface.fill((255, 230, 100))
            angle = random.randint(0, 360)*math.pi/180
            self.walls.add(ObstacleMouvant(self.screen, surface, pos, math.cos(angle), -math.sin(angle), 1.5, 250))

    def set(self) : 
        self.etat = True

        sound.background_music.stop()
        sound.countdown_sound.play()

    def unset(self) :
        self.etat = False

        sound.game_music.stop()
        sound.countdown_sound.stop()
        sound.victory_sound.stop()
        sound.draw_sound.stop()
        sound.defeat_sound.stop()
        sound.background_music.play(loops=-1)

    #affichage des éléments de la partie
    def draw(self) : 

        if not(self.game_over) : 
            #affichage de la balles, des raquettes et des obstacles
            self.ball.draw()
            self.racket1.draw()
            self.racket2.draw()
            self.walls.draw(self.screen)

            #affichage du compte à rebours
            if self.start == False and self.countdown() == False :
                countdown = 3
                if self.return_dt() >= 2200 :
                    countdown = 1
                elif self.return_dt() >= 1100 :
                    countdown = 2
                self.screen.blit(self.police1.render(str(countdown), False, 0), (525, 300))

            #affichage alertes de temps
            if self.start == True :
                temps_restant = self.countdown_end()
                if temps_restant <= 30 and temps_restant >= 27 :
                    self.screen.blit(self.police1.render("30 secondes !", False, 0), (490, 300))
                elif temps_restant <= 4 and temps_restant > 3 :
                    self.screen.blit(self.police1.render("3", False, 0), (525, 300))
                elif temps_restant <= 3 and temps_restant > 2 :
                    self.screen.blit(self.police1.render("2", False, 0), (525, 300))
                elif temps_restant <= 2 and temps_restant > 1 :
                    self.screen.blit(self.police1.render("1", False, 0), (525, 300))
                elif temps_restant <= 1 and temps_restant >= 0 :
                    self.screen.blit(self.police1.render("0", False, 0), (525, 300))

            #affichage du score et du timer
            self.screen.blit(self.police3.render(self.return_str_timer(), False, (255, 255, 255)), (500, 10))
            self.screen.blit(self.police3.render(self.return_str_score(), False, (255, 255, 255)), (485, 45)) 
        
        #affichage de l'écran de fin de partie
        else : 

            #petite animation
            for i in range(13) :
                surface = pygame.surface.Surface((42, 42))
                surface.fill((255, 255, 0))
                #surface.fill(pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                self.game_over_surface.blit(surface, (random.randint(0, 1060), random.randint(0, 700)))
            self.screen.blit(self.game_over_surface, (0, 0))

            #affichage du vainqueur
            if self.player1_score > self.player2_score :
                self.screen.blit(self.police4.render("PLAYER 1 WON !", False, 0), (400, 300))
            elif self.player1_score < self.player2_score :
                self.screen.blit(self.police4.render("PLAYER 2 WON !", False, 0), (400, 300))
            else : 
                self.screen.blit(self.police4.render("DRAW !", False, 0), (450, 300))

            #affichage du score et du timer
            self.screen.blit(self.police3.render(self.return_str_timer(), False, 0), (500, 40))
            self.screen.blit(self.police3.render(self.return_str_score(), False, 0), (485, 100)) 

    #applique les actions de la partie
    def apply(self) :

        if self.countdown() == True and self.start == False and self.game_over == False :
            self.start = True
            self.time_init = pygame.time.get_ticks()
            if self.player1_score == 0 and self.player2_score == 0 :
                sound.game_music.play(loops=-1)

        elif self.start == True and self.game_over == False :  
            #accélération de la partie
            self.acceleration()

            #applique le mouvement de la raquette du joueur 1
            self.racket1.apply()

            #applique le mouvement de la raquette du joueur 2
            self.racket2.apply()

            #applique le mouvement des obstacles en mouvement
            for obstacle in self.walls :
                if type(obstacle) == ObstacleMouvant :
                    obstacle.apply()

            #applique le mouvement de la balle
            self.ball.apply(self.walls.sprites(), [self.racket1, self.racket2])

            #timer du jeu
            self.timer = self.return_dt()//1000 + self.timer_save

            #score
            if self.ball.rect.left <= 0 :
                self.player2_score += 1
                self.new_round()

            elif self.ball.rect.right >= 1080 :
                self.player1_score += 1
                self.new_round() 

            #temps écoulé
            if self.countdown_end() == 30 :
                sound.alert_sound.play()
            elif self.countdown_end() == 4 and sound.countdown_sound.get_num_channels() == 0 :
                sound.countdown_sound.play()
            elif self.countdown_end() <= 0 :
                self.func_game_over()

        elif self.game_over == True :
            if self.game_over_countdown() == True :
                self.unset()
                
    def new_round(self) : 
        #variables de temps
        self.timer_save = self.timer
        self.time_init = pygame.time.get_ticks()

        if self.player1_score == 3 or self.player2_score == 3 :
            self.func_game_over()
        else : 
            self.start = False

            #son du compte à rebours
            sound.countdown_sound.stop()
            sound.countdown_sound.play()

            #remise en place de la balle et des raquettes
            self.create_ball()
            self.create_rackets()

    #active la fin de la partie
    def func_game_over(self) :
        self.game_over = True

        self.time_init = pygame.time.get_ticks()
        
        #sons
        sound.game_music.stop()
        sound.countdown_sound.stop()

        if self.player1_score == self.player2_score : 
            sound.draw_sound.play
        else : 
            sound.victory_sound.play()

    #gère les évènements
    def manage_events(self, event) : 
        #Bouge la raquette du joueur 1 si la touche a est pressée et celle du joueur 2 si la touche p est pressée
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_a:
                self.racket1.vy *= -1
            elif event.key == pygame.K_p:
                self.racket2.vy *= -1

    #renvoie le temps qui s'est écoulé depuis le début de la partie
    def return_dt(self) :
        return pygame.time.get_ticks() - self.time_init
    
    #renvoie le compte à rebours avant le début de la partie
    def countdown(self) : 
        if self.return_dt() >= 3600 :
            return True
        else : 
            return False
    
    #renvoie le compte à rebours avant la fin de la partie
    def countdown_end(self) :
        return self.game_duration - self.timer
    
    #renvoie le compte à rebours avant la fin de l'animation finale
    def game_over_countdown(self) : 
        if self.return_dt() >= 5000 :
            return True
        else : 
            return False
    
    def return_str_timer(self) :
        timer = str(self.timer//60) + ":" 
        if self.timer%60 < 10 : 
            timer += "0" + str(self.timer%60)
        else : 
            timer += str(self.timer%60)
        return timer

    def return_str_score(self) :
        return (str(self.player1_score) + " - " + str(self.player2_score))
    
    #renvoie le coefficient d'accélération de la balle en fonction du temps
    def acceleration(self)  :
        a = 1 + ((self.timer-self.timer_save)//self.time_up_acceleration)/10

        if self.ball.vx*self.ball.a < 12 and self.ball.v < 20 : 
            self.ball.a = a

            if abs(self.racket1.a*self.racket1.vy) < 12.5 :
                self.racket1.a = a
                self.racket2.a = a

        for obstacle in self.walls :
            if type(obstacle) == ObstacleMouvant :
                if obstacle.a < 10 :
                    obstacle.a = a


#classe de la game solo
class GameSolo(Game) : 
    def __init__(self, screen, police1, police2, police3, police4):
        super().__init__(screen, police1, police2, police3, police4)

    #affiche tous les éléments de la partie
    def draw(self) :

        #affichage de la partie
        if not(self.game_over) :
            super().draw()

        #affichage de l'écran de fin de partie
        else : 
            #petite animation
            for i in range(13) :
                surface = pygame.surface.Surface((42, 42))
                surface.fill((255, 255, 0))
                self.game_over_surface.blit(surface, (random.randint(0, 1060), random.randint(0, 700)))
            self.screen.blit(self.game_over_surface, (0, 0))

            #affichage du vainqueur
            if self.player1_score > self.player2_score :
                self.screen.blit(self.police4.render("YOU WON !", False, 0), (430, 300))
            elif self.player1_score < self.player2_score :
                self.screen.blit(self.police4.render("YOU LOSE !", False, 0), (425, 300))
            else : 
                self.screen.blit(self.police4.render("DRAW !", False, 0), (450, 300))

            #affichage du score et du timer
            self.screen.blit(self.police3.render(self.return_str_timer(), False, 0), (500, 40))
            self.screen.blit(self.police3.render(self.return_str_score(), False, 0), (485, 100)) 

    #applique toutes les actions de la partie
    def apply(self) :
        if self.start == True and self.game_over == False :
            self.acceleration()
            self.ia_racket_move()
            
        super().apply()

    #active la fin de la partie
    def func_game_over(self) :
        self.game_over = True

        self.time_init = pygame.time.get_ticks()
        
        #sons
        sound.game_music.stop()
        sound.countdown_sound.stop()

        if self.player1_score > self.player2_score : 
            sound.victory_sound.play

        elif self.player2_score > self.player1_score :
            sound.defeat_sound.play()

        else : 
            sound.draw_sound.play()

    #gère les évènements
    def manage_events(self, event) : 
        #Bouge la raquette du joueur si la touche espace est pressée
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                self.racket1.vy *= -1

    #permet le déplacement automatique de la raquette ennemie (bot)
    def ia_racket_move(self) : 
        #calcule de la future coordonnée y de la balle en x = 1050
        prediction = tools.prediction(self.ball.rect.copy(), self.ball.vx, self.ball.vy, self.ball.a, 1050, self.walls.sprites() + [self.racket1], 50)
        future_ball_coords = prediction[0]
        future_y_coord = tools.find_y(future_ball_coords, 1050, prediction[1], prediction[2])

        #mouvement automatique de la raquette bot en fonction de cette coordonnée y
        if future_y_coord < int((self.racket2.rect.top + 2*self.racket2.rect.center[1])/3) and self.racket2.vy > 0 :
            self.racket2.vy *= -1

        elif future_y_coord > int((self.racket2.rect.bottom + 2*self.racket2.rect.center[1])/3) and self.racket2.vy < 0 :
            self.racket2.vy *= -1

        