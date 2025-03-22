import pygame
from weapon import *

#liste des map
maps = ["tuiles/map1.tmx", "tuiles/map2.tmx", "tuiles/map3.tmx", "tuiles/map4.tmx", "tuiles/map5.tmx", "tuiles/map6.tmx", "tuiles/map7.tmx", "tuiles/map8.tmx", "tuiles/map9.tmx"]

#paramètres
settings_liste = {
    "difficulty" : ["easy", "normal", "hard"],
    "sound" : ["Enabled", "Disabled"],
    "jouabilité" : [
        ["azerty", 
         {"left": pygame.K_q, 
          "right" : pygame.K_d,
          "up" : pygame.K_z,
          "down" : pygame.K_s,
          "life" : pygame.K_p,
          "bomb" : pygame.K_b, 
          "sh" : pygame.K_r,
          }],
        ["qwerty",
         {"left": pygame.K_a, 
          "right" : pygame.K_d,
          "up" : pygame.K_w,
          "down" : pygame.K_s,
          "life" : pygame.K_p,
          "bomb" : pygame.K_b, 
          "sh": pygame.K_r,
          }],
        ["arrows",
         {"left": pygame.K_LEFT, 
          "right" : pygame.K_RIGHT,
          "up" : pygame.K_UP,
          "down" : pygame.K_DOWN,
          "life" : pygame.K_p,
          "bomb" : pygame.K_b,
          "sh": pygame.K_r, 
          }],
    ]
}

#armes
img_weapons = pygame.image.load("assets/weapons.png")
img_weapons2 = pygame.image.load("assets2/Weapons/Wood/Wood.png")
img_weapons3 = pygame.image.load("assets2/Weapons/Bone/Bone.png")
img_red_bullet = pygame.image.load("assets/red_bullet2.png").subsurface(0,0, 13, 4)

projectiles = [
    {
        "img" : img_red_bullet,
        "speed" : 10,
        "type_damage" : "unit"
    },
    {
        "img" : pygame.transform.scale_by(img_weapons.subsurface(83, 68, 21, 8), 2),
        "speed" : 6,
        "type_damage" : "zone"
    },
    {
        "img" : pygame.transform.rotate(pygame.transform.scale_by(img_weapons2.subsurface(20, 0, 8, 16), 1.5), -90),
        "speed" : 7,
        "type_damage" : "unit"
    },
    {
        "img" : pygame.transform.rotate(pygame.transform.scale_by(img_weapons3.subsurface(20, 0, 8, 16), 1.5), -90),
        "speed" : 7,
        "type_damage" : "unit"
    }
]

img_sword = img_weapons.subsurface(96, 16, 32, 16)
img_pistol = img_weapons.subsurface(0, 80, 32, 16)
img_gun = img_weapons.subsurface(0, 118, 12, 10)
img_rocket = img_weapons.subsurface(48, 64, 34, 16)
img_bow = img_weapons2.subsurface(48, 48, 48, 32)
img_bow2 = img_weapons3.subsurface(48, 48, 48, 32)
img_sword2 = pygame.transform.rotate(pygame.transform.flip(img_weapons3.subsurface(0, 0, 16, 48), True, False), -90)
img_pistol2 = img_weapons.subsurface(32, 80, 30, 16)
img_pistolgreen = img_weapons.subsurface(110, 50, 40, 16)
img_club = img_weapons.subsurface(90, 30, 40, 16)
img_pistol3 = img_weapons.subsurface(64, 100, 20, 12)
img_gunred = img_weapons.subsurface(64, 118, 13, 10)
img_sword3 = img_weapons.subsurface(64, 16, 32, 16)
img_axe = pygame.transform.rotate(pygame.transform.flip(img_weapons3.subsurface(48, 16, 16, 32), True, True), 90)

weapons = [
    {   "type" : Sword,
        "img" : img_sword,
        "properties" : {
            "image" : pygame.transform.scale_by(img_sword, 1.5),
            "reload_time" : 250,
            "damage" : 50,
            "range" : 48
        }
    },
    {   "type" : Gun,
        "img" : img_pistol,
        "properties" : {
            "image" :  pygame.transform.scale_by(img_pistol, 1.5),#coords 64;16 96;32
            "reload_time" : 250,
            "damage" : 25,
            "coords_projectile" : (14*1.5, 1*1.5),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Gun,
        "img" : img_gun,
        "properties": {
            "image" :  pygame.transform.scale_by(img_gun, 2),#coords 64;16 96;32
            "reload_time" : 500,
            "damage" : 50,
            "coords_projectile" : (6*2, -2*2),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Gun,
        "img" : img_rocket,
        "properties": {
            "image" :  pygame.transform.scale_by(img_rocket, 1.5),#coords 64;16 96;32
            "reload_time" : 1000,
            "damage" : 150,
            "coords_projectile" : (6*1.5, 0*1.5),
            "projectile" : projectiles[1]
        }
    },
    {   "type" : Bow,
        "img" : img_bow.subsurface(0, 0, 16, 32),
        "properties": {
            "image" :  img_bow,#coords 64;16 96;32
            "tables" : [[0, 0, 16, 31], [16, 0, 16, 32], [32, 0, 16, 32]],
            "reload_time" : 1000,
            "damage" : 100,
            "charging_time" : 450,
            "coords_projectile" : (8*1.5, 0*1.5),
            "projectile" : projectiles[2]
        }
    },
    {
        "type" : Sword,
        "img" : img_sword2,
        "properties" : {
            "image" : pygame.transform.scale_by(img_sword2, 1.15),
            "reload_time" : 600,
            "damage" : 120,
            "range" : 72
        }
    },
    {   "type" : Gun,
        "img" : img_pistol2,
        "properties" : {
            "image" :  pygame.transform.scale_by(img_pistol2, 1.5),
            "reload_time" : 100,
            "damage" : 10,
            "coords_projectile" : (14*1.5, 1*1.5),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Gun,
        "img" : img_pistolgreen,
        "properties" : {
            "image" :  pygame.transform.scale_by(img_pistolgreen, 1.5),
            "reload_time" : 300,
            "damage" : 30,
            "coords_projectile" : (18*1.5, -1*1.5),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Sword,
        "img" : img_club,
        "properties" : {
            "image" : pygame.transform.scale_by(img_club, 2),
            "reload_time" : 250,
            "damage" : 50,
            "range" : 48
        }
    },
    {   "type" : Gun,
        "img" : img_pistol3,
        "properties" : {
            "image" :  pygame.transform.scale_by(img_pistol3, 1.5),
            "reload_time" : 400,
            "damage" : 40,
            "coords_projectile" : (9*1.5, 0*1.5),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Gun,
        "img" : img_gunred,
        "properties" : {
            "image" :  pygame.transform.scale_by(img_gunred, 2),#coords 64;16 96;32
            "reload_time" : 750,
            "damage" : 75,
            "coords_projectile" : (6*2, -3*2),
            "projectile" : projectiles[0]
        }
    },
    {   "type" : Sword,
        "img" : img_sword3,
        "properties" : {
            "image" : pygame.transform.scale_by(img_sword3, 2),
            "reload_time" : 500,
            "damage" : 100,
            "range" : 48
        }
    },
    {   "type" : Bow,
        "img" : img_bow2.subsurface(0, 0, 16, 32),
        "properties": {
            "image" :  img_bow2,#coords 64;16 96;32
            "tables" : [[0, 0, 16, 31], [16, 0, 16, 32], [32, 0, 16, 32]],
            "reload_time" : 1000,
            "damage" : 100,
            "charging_time" : 450,
            "coords_projectile" : (8*1.5, 0*1.5),
            "projectile" : projectiles[2]
        }
    },
    {   "type" : Sword,
        "img" : img_axe,
        "properties" : {
            "image" : pygame.transform.scale_by(img_axe, 2),
            "reload_time" : 750,
            "damage" : 150,
            "range" : 48
        }
    }
]

player_weapons = [weapons[1], weapons[2], weapons[3], weapons[4], weapons[6], weapons[7], weapons[9], weapons[10]]

#personnages
img_knight = pygame.image.load("assets2/Heroes/Knight/Idle/Idle-Sheet.png").subsurface(0,0,26,32)
img_rogue = pygame.image.load("assets2/Heroes/Rogue/Idle/Idle-Sheet.png").subsurface(0,0,26,32)
img_wizzard = pygame.image.load("assets2/Heroes/Wizzard/Idle/Idle-Sheet.png").subsurface(0,0,26,32)
players = [
    {   "name" : "knight",
        "images" : "assets2/Heroes/Knight/",
        "tables" : {
            "death" : [[0,0,26,32], [48,0,26,32], [96,0,32,32], [144,0,40,32], [192,0,40,32], [240,0,40,32]],
            "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
            "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
        },
        "img" : img_knight,
        "properties" : {
            "pv" : 2250,
            "speed" : 4,
            "coef_damage" : 1.5
            }
    },
    {   "name" : "rogue",
        "images" : "assets2/Heroes/Rogue/",
        "tables" : {
            "death" : [[16,0,32,32], [88,0,24,32], [152,0,32,32], [216,0,40,32], [280,0,40,32], [344,0,40,32]],
            "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
            "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
        },
        "img" : img_rogue,
        "properties" : {
            "pv" : 2000,
            "speed" : 6,
            "coef_damage" : 1.25
        }
    },
    {   "name" : "wizzard",
        "images" : "assets2/Heroes/Wizzard/",
        "tables" : {
            "death" : [[0,0,32,32], [72,0,24,32], [136,0,40,32], [200,0,48,32], [264,0,48,32], [328,0,48,32]],
            "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
            "run" : [[16,29,32,35], [80, 29, 32, 35], [144, 29, 32, 35], [208, 29, 32, 35], [272, 29, 32, 35], [336, 29, 32, 35]]
        },
        "img" : img_wizzard,
        "properties" : {
            "pv" : 1750,
            "speed" : 5,
            "coef_damage" : 1.75
        }
    }
]

#tables orc
table_orc_base = {
    "images" : {
        "death" : [[16,40,24,24], [82,24,25,40], [156,39,25,25], [216,48,32,16], [278,48,35,16], [340,48,35,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
    },
    "properties" : {
        "pv" : 150,
        "speed" : 2,
        "coef_damage" : 0.2,
        "weapon" : weapons[11],
        "attack_delay" : 2000,
        "id" : 2
    }
}

table_orc_rogue = {
    "images" : {
        "death" : [[16,36,24,28], [82,24,25,40], [156,39,25,25], [216,48,32,16], [278,48,35,16], [340,48,35,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
    },
    "properties" : {
        "pv" : 200,
        "speed" : 3,
        "coef_damage" : 0.3,
        "weapon" : weapons[8],
        "attack_delay" : 1500,
        "id" : 3
    }
}

table_orc_shaman = {
    "images" : {
        "death" : [[16,40,32,24], [80,32,32,32], [154,48,24,16], [216,40,25,24], [278,48,35,16], [342,48,35,16], [406, 48, 35, 16]],
        "idle" : [[0,0,30,32], [32, 0, 30, 32], [64, 0, 30, 32], [96, 0, 30, 32]],
        "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
    },
    "properties" : {
        "pv" : 100,
        "speed" : 2,
        "coef_damage" : 0.5,
        "weapon" : weapons[5],
        "attack_delay" : 500,
        "id" : 2
    }
}

table_orc_warrior = {
    "images" : {
        "death" : [[32,52,24,28], [128,40,25,40], [232,56,20,24], [328,48,32,32], [424,64,40,16], [520,64,40,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,30,32,34], [80, 30, 32, 34], [144, 30, 32, 34], [208, 30, 32, 34], [272, 30, 32, 34], [336, 30, 32, 34]]
    },
    "properties" : {
        "pv" : 250,
        "speed" : 3,
        "coef_damage" : 0.6,
        "weapon" : weapons[13],
        "attack_delay" : 1000,
        "id" : 3
    }
}

tables_orc = {
    "Base" : table_orc_base,
    "Rogue" : table_orc_rogue,
    "Shaman" : table_orc_shaman,
    "Warrior" : table_orc_warrior
}


#tables skeleton

table_skeleton_base = {
    "images" : {
        "death" : [[32,32,24,32], [128,32,24,32], [224,24,24,40], [320,16,24,48], [416,24,24,40], [512,32,24,32],  [608,48,24,16], [704,48,24,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
    },
    "properties" : {
        "pv" : 150,
        "speed" : 2,
        "coef_damage" : 0.2,
        "weapon" : weapons[12],
        "attack_delay" : 250,
        "id" : 2
    }
}

table_skeleton_rogue = {
    "images" : {
        "death" : [[16,24,24,40], [72,24,32,40], [136,32,32,32], [192,40,40,24], [256,48,40,16], [320,48,40,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,32,32,32], [80, 32, 32, 32], [144, 32, 32, 32], [208, 32, 32, 32], [272, 32, 32, 32], [336, 32, 32, 32]]
    },
    "properties" : {
        "pv" : 200,
        "speed" : 3,
        "coef_damage" : 0.3,
        "weapon" : weapons[4],
        "attack_delay" : 200,
        "id" : 3
    }
}

table_skeleton_shaman = {
    "images" : {
        "death" : [[16,36,26,28], [80,8,32,56], [144,16,32,48], [208,40,32,24], [272,56,32,8], [336,48,32,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,30,32,34], [80, 30, 32, 34], [144, 30, 32, 34], [208, 30, 32, 34], [272, 30, 32, 34], [336, 30, 32, 34]]
    },
    "properties" : {
        "pv" : 100,
        "speed" : 2,
        "coef_damage" : 0.5,
        "weapon" : weapons[12],
        "attack_delay" : 100,
        "id" : 2
    }
}

table_skeleton_warrior = {
    "images" : {
        "death" : [[16,8,32,40], [79,0,25,48], [136,8,32,40], [200,16,32,32], [256,32,40,16], [320,32,40,16]],
        "idle" : [[0,0,26,32], [32, 0, 26, 32], [64, 0, 26, 32], [96, 0, 26, 32]],
        "run" : [[16,30,32,34], [80, 30, 32, 34], [144, 30, 32, 34], [208, 30, 32, 34], [272, 30, 32, 34], [336, 30, 32, 34]]
    },
    "properties" : {
        "pv" : 250,
        "speed" : 3,
        "coef_damage" : 0.6,
        "weapon" : weapons[4],
        "attack_delay" : 150,
        "id" : 3
    }
}

tables_skeleton = {
    "Base" : table_skeleton_base,
    "Rogue" : table_skeleton_rogue,
    "Shaman" : table_skeleton_shaman,
    "Warrior" : table_skeleton_warrior
}

#vitesse de changement d'image en fonction de la vitesse du sprite
change_image_speed = {
    "1" : 250,
    "2" : 225,
    "3" : 200,
    "4" : 175,
    "5" : 150,
    "6" : 125,
    "7" : 100,
    "8" : 75,
}