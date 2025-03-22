import pygame

#classe qui contrôle tous les sons utilisés dans le jeu
class Sound:
    def __init__(self):
        #son activé
        self.sound_on = True

        #musique de fond
        self.music = pygame.mixer.Sound("assets/sound/bgsound.mp3")

        #son d'explosion et de tirs
        self.fireball_sound = pygame.mixer.Sound("assets/sound/fireball.mp3")
        self.explose_sound = pygame.mixer.Sound("assets/sound/fireball_explosion.mp3")
        self.shoot_sound = pygame.mixer.Sound("assets/sound/hit.mp3")
        self.bow_sound = pygame.mixer.Sound("assets/sound/bow.mp3")
        self.sword_sound = pygame.mixer.Sound("assets/sound/epee_boss.mp3")

        #portail
        self.portal_apparition_sound = pygame.mixer.Sound("assets/sound/portal_apparition.mp3")
        self.teleportation_sound = pygame.mixer.Sound("assets/sound/teleportation.mp3")

        #bruits de pas
        self.mvmt_sound = pygame.mixer.Sound("assets/sound/pas.mp3")

        #mort du boss
        self.boss_death_sound = pygame.mixer.Sound("assets/sound/mort_boss.mp3")

        #musique game over et de victoire
        self.game_over_sound = pygame.mixer.Sound("assets/sound/gameover3sec.mp3")
        self.win_sound = pygame.mixer.Sound("assets/sound/win_sound.mp3")

        #son de boutons
        self.select_sound = pygame.mixer.Sound("assets/sound/select_sound.mp3")

    #définit le volume de chaque son
    def sound_volume_on(self):
        self.music.set_volume(0.25)

        self.fireball_sound.set_volume(0.8)
        self.explose_sound.set_volume(0.8)
        self.shoot_sound.set_volume(0.05)
        self.bow_sound.set_volume(0.3)
        self.sword_sound.set_volume(0.9)

        self.portal_apparition_sound.set_volume(1.0)
        self.teleportation_sound.set_volume(1.0)

        self.mvmt_sound.set_volume(1.0)

        self.boss_death_sound.set_volume(0.85)

        self.game_over_sound.set_volume(0.4)
        self.win_sound.set_volume(0.5)

        self.select_sound.set_volume(0.5)

    #met le volume de tous les sons à 0
    def sound_volume_off(self) :
        self.music.set_volume(0)
        self.fireball_sound.set_volume(0)
        self.explose_sound.set_volume(0)
        self.shoot_sound.set_volume(0)
        self.bow_sound.set_volume(0)
        self.sword_sound.set_volume(0)
        self.portal_apparition_sound.set_volume(0)
        self.teleportation_sound.set_volume(0)
        self.mvmt_sound.set_volume(0)
        self.boss_death_sound.set_volume(0)
        self.game_over_sound.set_volume(0)
        self.win_sound.set_volume(0)
        self.select_sound.set_volume(0)

    #actualise le volume des sons : activé ou desactivé
    def change_volume(self) :
        self.sound_on = not(self.sound_on)

        if self.sound_on == True :
            self.sound_volume_on()
        else :
            self.sound_volume_off()

pygame.mixer.init()

sound = Sound() #variable qui permet d'utiliser tous les sons et les fonctions de la classe