import pyxel

def fall(sprite, walls, speed, collide) -> float : 
    if collide(walls, sprite, 0, speed) : 
        return speed
    else :  
        return 0

def jump_gravity(y, ground, jump_height, speed:float, collide, walls, sprite) -> float :  
    if y > ground - jump_height and collide(walls, sprite, 0, -speed) and sprite.y >= 0: 
        return -speed
    else : 
        return 0
            
#classe du joueur
class Player() : 
    def __init__(self, x: int, y: int, walls: list) : 
        # pos x, y 
        self.x = x   
        self.y = y

        self.width = 10
        self.height = 14

        self.walls = walls

        #vitesse sprite
        self.speed = 2

        self.pv = 3

        self.direction = 0

        self.jump = True
        self.fall = False

        self.ground = y

        pyxel.load("2.pyxres")
        
    #bouge vers la gauche
    def move_left(self) :
        self.x = (self.x - self.speed)%256
    
    #bouge vers la droite
    def move_right(self) :
        self.x = (self.x + self.speed)%256

    #saute
    def move_up(self) :
        #self.y = (self.y - self.speed)%256
        if self.jump == False and self.fall == False : 
            self.jump = True
            self.ground = self.y

    #bouge vers le bas
    def move_down(self) : 
        #self.y = (self.y + self.speed)%256
        pass
    
    def collide_down(self):
        if pyxel.pget(self.x , self.y + 17) or pyxel.pget(self.x + 6, self.y + 17) or pyxel.pget(self.x + 12, self.y + 17) == 0:
            return True
        return False
    
    def collide_up(self):
        if pyxel.pget(self.x , self.y - 1) or pyxel.pget(self.x + 6, self.y - 1) or pyxel.pget(self.x + 12, self.y - 1) == 0:
            return True
        return False
    
    def collide_right(self):
        if pyxel.pget(self.x + 13, self.y) or pyxel.pget(self.x + 13, self.y + 8) or pyxel.pget(self.x + 13, self.y + 16) == 0:
            return True
        return False

    def collide_left(self):
        if pyxel.pget(self.x -1, self.y) or pyxel.pget(self.x -1, self.y + 8) or pyxel.pget(self.x - 1, self.y + 16) == 0:
            return True
        return False

    def update(self, collision) : 

        if pyxel.btn(pyxel.KEY_Z) == True and collision(self.walls, self, 0, -self.speed):
            self.move_up()
        if pyxel.btn(pyxel.KEY_Q)== True and collision(self.walls, self, -self.speed, 0):
            self.move_left()
            self.direction = 1
        if pyxel.btn(pyxel.KEY_D)== True and collision(self.walls, self, self.speed, 0):
            self.move_right()   
            self.direction = 0
        if pyxel.btn(pyxel.KEY_S) == True and collision(self.walls, self, 0, self.speed):
            self.move_down()

        if self.jump == True : 
            dy = jump_gravity(self.y, self.ground, 30, self.speed, collision, self.walls, self)
            if dy == 0 : 
                self.jump = False
                self.fall = True
            else : 
                if collision(self.walls, self, 0, -self.speed) : 
                    self.y += dy
                else: 
                    self.fall = True
                    self.jump = False

        elif self.fall == True :
            dy = fall(self, self.walls, self.speed, collision)
            if dy == 0 : 
                self.fall = False
                self.jump = False
            else : 
                self.y += dy
        elif collision(self.walls, self, 0, 0) :
            self.fall = True

    
    #affiche le joueur
    def draw(self):
        if self .direction == 0:
            pyxel.blt(self.x, self.y, 0,3,9,self.width,self.height, 0)
        else:
            pyxel.blt(self.x, self.y, 0,67,9,self.width,self.height, 0)     

class Monstre():

    def __init__(self,x, y ,player):
        # pos x, y 
        self.x = x   
        self.y = y
        # vitesse sprite
        self.speed = 2 
        pyxel.load("2.pyxres")
        self.player = player
        

    def collide(self):
        if pyxel.pget(self.x + 6, self.y + 17) == 0:
            return True
        return False
    
    def deplacement(self) :
        self.mort = False
        while self.mort == False :
            self.dir= 2
            self.x += 5 
            self.dir = 0 
            self.x -= 5 
        self.y = 1000
            
    def draw_monstre(self) : 
        pyxel.blt(self.x, self.y, 0,3,152,16,16, 5)
       

class Wall() : 
    def __init__(self, x, y, width, height, color) : 
        # pos x, y 
        self.x = x 
        self.y = y

        self.color = color

        # dimentions sprite
        self.width = width
        self.height = height

        if self.x + self.width > 256 : 
            self.width = 256 - self.x
            
        if self.y + self.height > 256 : 
            self.height = 256 - self.y

        pyxel.load("2.pyxres")

    #affiche le mur
    def draw(self) :
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

    def collide(self, x, y, width, height) : 
        on_x = False
        on_y = False

        if self.x >= x and self.x + self.width <= x + width : 
            on_x = True
        elif self.x <= x and self.x + self.width >= x + width : 
            on_x = True
        elif x >= self.x and x <= self.x + self.width : 
            on_x = True
        elif x + width >= self.x and x + width <= self.x + self.width : 
            on_x = True
        
        if self.y >= y and self.y + self.height <= y + height : 
            on_y = True
        elif self.y <= y and self.y + self.height >= y + height : 
            on_y = True
        elif y >= self.y and y <= self.y + self.height : 
            on_y = True
        elif y + height >= self.y and y + height <= self.y + self.height : 
            on_y = True

        if on_x == True and on_y == True :
            return True
        else : 
            return False

class App() : 

    def __init__(self) : 
        #initialisation de la fenêtre
        pyxel.init(256, 256, title="Jumping Warrior !!!!", fps=30, quit_key=pyxel.KEY_ESCAPE)

        #création de murs
        self.walls = self.init_walls()

        #création du joueur
        self.player = Player(0, 180, self.walls)
        self.monstre = Monstre(0, 0, self.player)

        #variable direction 
        self.direction = 0

        self.win = False
        
        pyxel.play(0, 0, loop=True)

        pyxel.run(self.update, self.draw)

    def update(self) : 
        self.player.update(self.collision)

        if self.walls[1].collide(self.player.x, self.player.y, self.player.width, self.player.height) : 
            self.win = True
        """
        if self.player.y <= 1 : 
            self.win = True
        """
            
    def draw(self) :
       
        pyxel.cls(0)
        self.monstre.draw_monstre()
        pyxel.bltm(0,0,0,0,0,1000,256)
        self.player.draw()

        for wall in self.walls[2:] : 
            wall.draw()

        if self.win == True : 
            pyxel.text(100, 75, "You Won", 0)

    def init_walls(self) -> list : 
        walls = []

        walls.append(Wall(0, 194, 256, 71, 0))
        walls.append(Wall(5, 0, 5, 20, 0))

        walls.append(Wall(10, 150, 15, 5, 10))
        walls.append(Wall(30, 175, 30, 5, 10))
        walls.append(Wall(50, 130, 25, 10, 10))
        walls.append(Wall(90, 100, 40, 25, 10))
        walls.append(Wall(150, 80, 20, 30, 10))
        walls.append(Wall(180, 50, 40, 25, 10))
        walls.append(Wall(145, 25, 20, 10, 10))
        walls.append(Wall(100, 35, 20, 7, 10))
        walls.append(Wall(70, 30, 10, 20, 10))
        walls.append(Wall(40, 28, 5, 50, 10))

        walls.append(Wall(5, 20, 5, 5, 9))

        return walls
    
    def init_monstre(self):
        self.monstres = []
        self.dif = 0 
        for wall in self.walls :
            x = pyxel.rndi(10,250)
            y = pyxel.rndi(180,180)
            self.monstres.append(Monstre(wall.x + int(wall.width/2), wall.y - 17, self.player))

    def collision(self, walls, sprite, x, y) : 
        for wall in walls :
            if wall != walls[1] : 
                if wall.collide(sprite.x + x, sprite.y + y, sprite.width, sprite.height) : 
                    return False
            
        return True

App()

#Pour edit le pyxres : & "c:/Program Files/python/python.exe" -m pyxel edit 2.pyxres
#Pour exécuter le programme : & "c:/Program Files/python/python.exe" "//0641-SRV-FILES/perso/ELEVES_LYC/1ERE07/ZARZOSO/Documents/Nuit du code/main.py"