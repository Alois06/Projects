import math

#fonction qui renvoie un tuple contenant les coordonnées x et y d'un vecteur AB de norme v
def vecteur(A, B, v) :
    # vecteur AB
    x = B[0]-A[0]
    y = B[1]-A[1]
    norme = round(math.sqrt(x**2 + y**2), 10)
    if norme == 0 :
        return (0, 0)
    # vecteur en fonction de v
    x = round(x/norme, 10)*v
    y = round(y/norme, 10)*v
    return (x, y)

#fonction qui renvoie la distance entre deux points A et B
def get_distance(A, B) :
    x = B[0] - A[0]
    y = B[1] - A[1]
    distance = math.sqrt(x**2 + y**2)
    return distance

#fonction qui renvoie l'angle associé aux coordonnées d'un vecteur
def get_angle(x, y) :
    norme = math.sqrt(x**2 + y**2)
    if norme == 0 : 
        return 0
    angle = math.degrees(round(math.acos(x/norme), 2))
    if y > 0 :
        angle = -angle
    return angle

#fonction qui renvoie un tuple de coordonnées correspondant à un vecteur de norme "rayon" 
#colinéaire avec le vecteur de coordonnées x et y fourni en entrée
def vecteur_rayon(x, y, rayon) :
    if x != 0 or y != 0 :
        norme = math.sqrt(x**2 + y**2)
        x = (x/norme)*rayon
        y = (y/norme)*rayon
    return (x, y)

#fonction qui renvoie un tuple de coordonnées et qui permet d'obtenir les coordonnées de création d'un projectile
def get_position(x, y, x_w, y_w, angle, flip) :
    if flip : 
        if angle > 90 or angle < -90 :
            y_w = -y_w
    rayon = math.sqrt(x_w**2 + y_w**2)
    angle = get_angle(x_w, y_w) + angle
    x = x + round((math.cos(math.radians(angle))*rayon), 2)
    y = y - round((math.sin(math.radians(angle))*rayon), 2)
    return (x, y)

#fonction qui vérifie si un sprite peut se diriger vers un autre sprite sans entrer en collision avec un mur
def trajectory_movement(collisions, sprite, rect_objectif) :

    coords = rect_objectif.center
    rect = sprite.rect
    points = []
    
    vec = vecteur(rect.center, rect_objectif.center, sprite.speed)
    angle = get_angle(vec[0], vec[1]) 

    if angle >= -22.5 and angle < 22.5 :
        points += [rect.topright, rect.midright, rect.bottomright]
    elif angle >= 22.5 and angle < 67.5 : 
        points += [rect.topleft, rect.topright, rect.bottomright]
    elif angle >= 67.5 and angle < 112.5 : 
        points += [rect.topleft, rect.midtop, rect.topright]
    elif angle >= 112.5 and angle < 157.5 : 
        points += [rect.bottomleft, rect.topleft, rect.topright]
    elif angle >= 157.5 or angle < -157.5  : 
        points += [rect.bottomleft, rect.midleft, rect.topleft] 
    elif angle >= -157.5 and angle < -112.5 : 
        points += [rect.bottomright, rect.bottomleft, rect.topleft]
    elif angle >= -112.5 and angle < -67.5 : 
        points += [rect.bottomright, rect.midbottom, rect.bottomleft]
    elif angle >= -67.5 and angle < -22.5 : 
        points += [rect.topright, rect.bottomright, rect.bottomleft]
    else : 
        points += [rect.center]

    vectors = {}

    for point in points :

        x = point[0]
        y = point[1]
        vector = vecteur(point, coords, sprite.speed)

        verfication = True

        while verfication == True and not(rect_objectif.collidepoint((x, y))) :
            x += vector[0]
            y += vector[1]

            if rect_objectif.colliderect(rect) : 
                verfication = True
                break

            for wall in collisions :
                if wall.collidepoint((x, y)) :
                    verfication = False
                    break

        if verfication : 
            vectors[point] = vector

    #renvoie les vecteurs s'il y en a 
    if len(vectors) > 0 :
        return vectors

#fonction qui vérifie si un projectile peut être tiré d'un sprite vers un sprite ennemi sans entrer en collision avec un mur
def trajectory_projectile(collisions, coords_tir, projectile_rect, projectile_speed, rect_objectif) :
    coords = rect_objectif.center
    rect = projectile_rect
    speed_projectile = projectile_speed
    rect.center = coords_tir

    vector_test = vecteur(rect.center, coords, speed_projectile) 

    verfication = True

    while verfication == True and not(rect_objectif.colliderect(rect)) and rect.colliderect(0, 0, 1080, 720):
        rect.x += vector_test[0]
        rect.y += vector_test[1]

        if rect_objectif.colliderect(rect) : 
            verfication = True
            break
        
        for wall in collisions :
            if wall.colliderect(rect) :
                verfication = False
                break

    return verfication