import tkinter
import time
import random
from tkinter import *

def jeu() :
    #setup
    tk = Tk()
    tk.title("Partie")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    #création de la balle, des raquettes et des obstacles
    liste_départs_x = [-0.75, -0.5, 0.5, 0.75]
    liste_départs_y = [-0.75, -0.5, 0.5, 0.75]
    raquette1 = Raquette(canvas, "blue", '<KeyPress-Left>', 50, 150)
    raquette2 = Raquette(canvas, "blue", '<KeyPress-Right>', 440, 150)
    obstacle1 = Obstacle(canvas, "yellow")
    obstacle2 = Obstacle(canvas, "yellow")
    obstacle3 = Obstacle(canvas, "yellow")
    obstacle4 = Obstacle(canvas, "yellow")
    obstacle5 = Obstacle(canvas, "yellow")
    obstacles =  [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]
    balle = Balle(canvas, raquette1, raquette2, "red", liste_départs_x, liste_départs_y, obstacles)
    tk.update()
    #compte à rebours
    for i in range(0, 3) :
        début = canvas.create_text(250, 200, text=str(3-i), fill="green", font=('Courier', 60))
        tk.update()
        time.sleep(1)
        canvas.delete(tk, début)
        tk.update()
    #mise en place de certaines variables
    temps = 0
    temps_max = 5
    #jeu
    while 1 :
        #bouger les raquettes et la balle
        balle.dessiner()
        raquette1.dessiner()
        raquette2.dessiner()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
        #augmenter la vitesse de la balle en fonction du temps
        if temps >= temps_max :
            if balle.x > 0 :
                balle.x = balle.x + 0.25
            elif balle.x < 0 :
                balle.x = balle.x - 0.25
            if balle.y > 0 :
                balle.y = balle.y + 0.25
            elif balle.y < 0 :
                balle.y = balle.y - 0.25
            temps_max = temps_max + 5
        #fin de partie
        if balle.dessiner() == True :
            canvas.create_text(250, 200, text='GAME OVER !', fill="green", font=('Courier', 20))
            pos_balle = canvas.coords(balle.id)
            largeur_canvas = canvas.winfo_width()
            if pos_balle[0] <= 0 :
                canvas.create_text(250, 300, text="Félicitations au Joueur 2 qui remporte la partie !", fill="green", font=("Courier", 9))
            elif pos_balle[2] >= largeur_canvas :
                canvas.create_text(250, 300, text="Félicitations au Joueur 1 qui remporte la partie !", fill="green", font=("Courier", 9))
            break
        temps = temps + 0.01

def match() :
    #setup
    tk = Tk()
    tk.title("Match")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    #mise en place de certaines variables
    score_j1 = 0
    score_j2 = 0
    score = str(score_j1) + " - " + str(score_j2)
    pts_victoire = 5
    while score_j1 < pts_victoire and score_j2 < pts_victoire :
        #création de la balle, des raquettes et des obstacles
        liste_départs_x = [-0.75, -0.5, 0.5, 0.75]
        liste_départs_y = [-0.75, -0.5, 0.5, 0.75]
        raquette1 = Raquette(canvas, "blue", '<KeyPress-Left>', 50, 150)
        raquette2 = Raquette(canvas, "blue", '<KeyPress-Right>', 440, 150)
        obstacle1 = Obstacle(canvas, "yellow")
        obstacle2 = Obstacle(canvas, "yellow")
        obstacle3 = Obstacle(canvas, "yellow")
        obstacle4 = Obstacle(canvas, "yellow")
        obstacle5 = Obstacle(canvas, "yellow")
        obstacles =  [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]
        balle = Balle(canvas, raquette1, raquette2, "red", liste_départs_x, liste_départs_y, obstacles)
        tk.update()
        #affichage du score
        score_texte = canvas.create_text(250, 15, text=str(score), fill="green", font=('Courier', 10))
        #compte à rebours
        for i in range(0, 3) :
            début = canvas.create_text(250, 200, text=str(3-i), fill="green", font=('Courier', 60))
            tk.update()
            time.sleep(1)
            canvas.delete(tk, début)
            tk.update()
        #mise en place de certaines variables
        temps = 0
        temps_max = 5
        #jeu
        while True :
            #bouger les raquettes et la balle
            balle.dessiner()
            raquette1.dessiner()
            raquette2.dessiner()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
            #augmenter la vitesse de la balle en fonction du temps
            if temps >= temps_max :
                if balle.x > 0 :
                    balle.x = balle.x + 0.25
                elif balle.x < 0 :
                    balle.x = balle.x - 0.25
                if balle.y > 0 :
                    balle.y = balle.y + 0.25
                elif balle.y < 0 :
                    balle.y = balle.y - 0.25
                temps_max = temps_max + 5
            temps = temps + 0.01
            #fin du point
            if balle.dessiner() == True :
                pos_balle = canvas.coords(balle.id)
                largeur_canvas = canvas.winfo_width()
                #mise à jour des scores
                if pos_balle[0] <= 0 :
                    score_j2 = score_j2 + 1
                    texte = canvas.create_text(250, 300, text="But pour le joueur 2 !", fill="green", font=("Courier", 9))
                elif pos_balle[2] >= largeur_canvas :
                    score_j1 = score_j1 + 1
                    texte = canvas.create_text(250, 300, text="But pour le joueur 1 !", fill="green", font=("Courier", 9))
                score = str(score_j1) + " - " + str(score_j2)
                texte2 = canvas.create_text(250, 325, text=str(score), fill="green", font=("Courier", 9))
                tk.update()
                time.sleep(3)
                canvas.delete(tk, texte)
                canvas.delete(tk, texte2)
                break
        #suppression et réinitialisation
        canvas.delete(tk, balle.id)
        del(balle)
        canvas.delete(tk, raquette1.id)
        del(raquette1)
        canvas.delete(tk, raquette2.id)
        del(raquette2)
        nbr_obstacles = len(obstacles)
        for i in range(0, nbr_obstacles) :
            obs = obstacles[i]
            canvas.delete(tk, obs.id)
            del(obs)
        canvas.delete(tk, score_texte)
        del(score_texte)
        tk.update()
    #fin de partie
    canvas.create_text(250, 100, text=str(score), fill="green", font=("Courier", 9))
    canvas.create_text(250, 200, text='GAME OVER !', fill="green", font=('Courier', 20))
    if score_j1 == pts_victoire :
        canvas.create_text(250, 300, text="Félicitations au Joueur 1 qui remporte le match !", fill="green", font=("Courier", 9))
    elif score_j2 == pts_victoire :
        canvas.create_text(250, 300, text="Félicitations au Joueur 2 qui remporte le match !", fill="green", font=("Courier", 9))

def solo() :
    #setup
    tk = Tk()
    tk.title("Solo")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1)
    tk.geometry("500x400")
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    #création des obstacles et de la balle
    liste_départs_x = [-0.75, -0.5, 0.5, 0.75]
    liste_départs_y = [-0.75, -0.5, 0.5, 0.75]
    raquette1 = Raquette(canvas, "blue", '<KeyPress-Left>', 50, 150)
    raquette2 = Raquette(canvas, None, '<KeyPress-Right>', 520, 150)
    obstacle1 = Obstacle(canvas, "yellow")
    obstacle2 = Obstacle(canvas, "yellow")
    obstacle3 = Obstacle(canvas, "yellow")
    obstacle4 = Obstacle(canvas, "yellow")
    obstacle5 = Obstacle(canvas, "yellow")
    obstacles =  [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]
    balle = Balle(canvas, raquette1, raquette2, "red", liste_départs_x, liste_départs_y, obstacles)
    tk.update()
    #variables nombre de points et nombre de vies restantes
    vies = 3
    points = 0
    #jeu
    for i in range(0, vies) :
        #mise en place de certaines variables
        temps = 0
        temps_max = 5
        #affichage du nombre de points et du nombre de vies
        pts = "Points : " + str(points)
        pts_texte = canvas.create_text(300, 15, text=str(pts), fill="green", font=('Courier', 10))
        v = "Vies : " + str(vies)
        v_texte = canvas.create_text(200, 15, text=str(v), fill="green", font=('Courier', 10))
        tk.update()
        #compte à rebours
        for i in range(0, 3) :
            début = canvas.create_text(250, 200, text=str(3-i), fill="green", font=('Courier', 60))
            tk.update()
            time.sleep(1)
            canvas.delete(tk, début)
            tk.update()
        while True :
            #augmenter la vitesse de la balle en fonction du temps
            if temps >= temps_max :
                if balle.x > 0 :
                    balle.x = balle.x + 0.25
                elif balle.x < 0 :
                    balle.x = balle.x - 0.25
                if balle.y > 0 :
                    balle.y = balle.y + 0.25
                elif balle.y < 0 :
                    balle.y = balle.y - 0.25
                temps_max = temps_max + 5
            #bouger la raquette et la balle
            balle.dessiner()
            raquette1.dessiner()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
            temps = temps + 0.01
            #position de la balle et de la raquette et la largeur du canvas
            pos_balle = canvas.coords(balle.id)
            pos_raquette = canvas.coords(raquette1.id)
            largeur_canvas = canvas.winfo_width()
            #si la balle touche l'un des côtés du canvas
            if balle.dessiner() == True :
                #côté gauche
                if pos_balle[0] <= 0 :
                    vies = vies - 1
                    #suppression de l'affichage de l'ancien nombre de points et de vies
                    canvas.delete(tk, pts_texte)
                    canvas.delete(tk, v_texte)
                    tk.update()
                    break
                #côté droit
                elif pos_balle[2] >= largeur_canvas :
                    balle.x = -abs(balle.x)
            #si la balle touche la raquette
            touch = False
            if pos_balle[0] <= pos_raquette[2] and pos_balle[2] >= pos_raquette[2] :
                if pos_balle[1] >= pos_raquette[1] and pos_balle[3] <= pos_raquette[3] :
                    touch = True
                elif pos_balle[1] <= pos_raquette[1] and pos_balle[3] >= pos_raquette[1] :
                    touch = True
                elif pos_balle[1] <= pos_raquette[3] and pos_balle[3] >= pos_raquette[3] :
                    touch = True
            if touch == True :
                #ajoute un point
                points = points + 1
                #suppression de l'affichage de l'ancien nombre de points et de vies
                canvas.delete(tk, pts_texte)
                #affichage du nombre de points et du nombre de vies
                pts = "Points : " + str(points)
                pts_texte = canvas.create_text(300, 15, text=str(pts), fill="green", font=('Courier', 10))
                tk.update()
                #bouger la raquette et la balle
                for x in range(0, 3) :
                    balle.dessiner()
                    raquette1.dessiner()
                    tk.update_idletasks()
                    tk.update()
                    time.sleep(0.01)
                    temps = temps + 0.01
        #remise en place de la raquette et de la balle
        canvas.delete(tk, balle.id)
        del(balle)
        canvas.delete(tk, raquette1.id)
        del(raquette1)
        tk.update()
        raquette1 = Raquette(canvas, "blue", '<KeyPress-Left>', 50, 150)
        balle = Balle(canvas, raquette1, raquette2, "red", liste_départs_x, liste_départs_y, obstacles)
        tk.update()
    #fin de partie
        #affichage du nombre de points et du nombre de vies
    pts = "Points : " + str(points)
    pts_texte = canvas.create_text(300, 15, text=str(pts), fill="green", font=('Courier', 10))
    v = "Vies : " + str(vies)
    v_texte = canvas.create_text(200, 15, text=str(v), fill="green", font=('Courier', 10))
    tk.update()
        #fin
    fin = "Score : " + str(points) + " points"
    canvas.create_text(250, 200, text='GAME OVER !', fill="green", font=('Courier', 20))
    canvas.create_text(250, 250, text=str(fin), fill="green", font=("Courier", 10))



class Balle:
    def __init__(self, canvas, raquette1, raquette2, couleur, dx, dy, obstacles) :
        self.canvas = canvas
        self.raquette1 = raquette1
        self.raquette2 = raquette2
        self.obstacles = obstacles
        self.id = canvas.create_oval(10, 10, 25, 25, fill=couleur)
        self.canvas.move(self.id, 245, 100)
        self.liste_départs_x = dx
        random.shuffle(self.liste_départs_x)
        self.liste_départs_y = dy
        random.shuffle(self.liste_départs_y)
        self.x = self.liste_départs_x[0]
        self.y = self.liste_départs_y[0]
        self.hauteur_canvas = self.canvas.winfo_height()
        self.largeur_canvas = self.canvas.winfo_width()
    def dessiner(self):
        pos = self.canvas.coords(self.id)
        pos_raquette1 = self.canvas.coords(self.raquette1.id)
        pos_raquette2 = self.canvas.coords(self.raquette2.id)
        self.canvas.move(self.id, self.x, self.y)
        #canvas
        if pos[1] <= 0 :
            self.y = abs(self.y)
        if pos[3] >= self.hauteur_canvas :
            self.y = -(abs(self.y))
        if pos[0] <= 0 :
            return True
        if pos[2] >= self.largeur_canvas :
            return True
        #raquette 1
        if pos[0] >= pos_raquette1[0] and pos[0] <= pos_raquette1[2] :
            if pos[1] >= pos_raquette1[1] and pos[3] <= pos_raquette1[3] :
                self.x = abs(self.x)
            elif pos[1] <= pos_raquette1[1] and pos[3] >= pos_raquette1[1] :
                self.x = abs(self.x)
            elif pos[1] <= pos_raquette1[3] and pos[3] >= pos_raquette1[3] :
                self.x = abs(self.x)
        #raquette 2
        if pos[2] >= pos_raquette2[0] and pos[2] <= pos_raquette2[2] :
            if pos[3] >= pos_raquette2[1] and pos[1] <= pos_raquette2[3] :
                self.x = -(abs(self.x))
            elif pos[1] <= pos_raquette2[1] and pos[3] >= pos_raquette2[1] :
                self.x = -(abs(self.x))
            elif pos[1] <= pos_raquette2[3] and pos[3] >= pos_raquette2[3] :
                self.x = -(abs(self.x))
        #obstacles
        nbr_obstacles = len(self.obstacles)
        for x in range(0, nbr_obstacles) :
            obs = self.obstacles[x]
            pos_obstacle = self.canvas.coords(obs.id)
            #côté gauche de l'obstacle
            if pos[0] <= pos_obstacle[0] and pos[2] >= pos_obstacle[0] :
                if pos[1] >= pos_obstacle[1] and pos [3] <= pos_obstacle[3] :
                    self.x = -(abs(self.x))
            #côté droit de l'obstacle
            if pos[0] <= pos_obstacle[2] and pos[2] >= pos_obstacle[2] :
                if pos[1] >= pos_obstacle[1] and pos [3] <= pos_obstacle[3] :
                    self.x = abs(self.x)
            #haut de l'obstacle
            if pos[1] <= pos_obstacle[1] and pos[3] >= pos_obstacle[1] :
                if pos[0] >= pos_obstacle[0] and pos [2] <= pos_obstacle[2] :
                    self.y = -(abs(self.y))
            #bas de l'obstacle
            if pos[1] <= pos_obstacle[3] and pos[3] >= pos_obstacle[3] :
                if pos[0] >= pos_obstacle[0] and pos [2] <= pos_obstacle[2] :
                    self.y = abs(self.y)
        return False

class Raquette:
    def __init__(self, canvas, couleur, key, x, y) :
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 10, 100, fill=couleur)
        self.canvas.move(self.id, x, y)
        self.x = 0
        self.y = 3
        self.hauteur_canvas = self.canvas.winfo_height()
        self.canvas.bind_all(key, self.change)
    def dessiner(self) :
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.x, self.y)
        if pos[1] <= 0 :
            self.y = 3
        if pos[3] >= self.hauteur_canvas :
            self.y = -3
    def change(self, evt) :
        self.y = self.y * (-1)

class Obstacle :
    def __init__(self, canvas, couleur) :
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 25, 25, fill=couleur)
        self.x = random.randint(100, 400)
        self.y = random.randint(50, 350,)
        self.canvas.move(self.id, self.x, self.y)

#création de l'interface graphique
tk = Tk()
tk.title("Jeu")
tk.geometry("500x400")
#création du canvas
canvas = Canvas(tk, width=500, height=400, bg="blue", bd=0, highlightthickness=0)
canvas.pack()
canvas.place(x=0, y=0)
#création des boutons servant à lancer les parties
btn1 = Button(tk, width=10, height=2, bg="black", fg="red", highlightcolor="green", text="Jouer", font=("Courier", 10), command=jeu)
btn2 = Button(tk, width=10, height=2, bg="black", fg="red", text="Match", font=("Courier", 10), command=match)
btn3 = Button(tk, width=10, height=2, bg="black", fg="red", text="Solo", font=("Courier", 10), command=solo)
btn1.pack(side=BOTTOM)
btn2.pack(side=LEFT)
btn3.pack(side=RIGHT)
btn2.place(x=0, y=360)
btn3.place(x=410, y=360)
#création du texte qui va apparaître sur l'interface
txt1 = canvas.create_text(250, 200, text="JEU TKINTER", fill="green", font=("Courier", 30))
txt2 = canvas.create_text(250, 250, text="Développé par Aloïs ZARZOSO", fill="green", font=("Courier", 15))

