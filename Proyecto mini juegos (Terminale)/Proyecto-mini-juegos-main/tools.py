import math
import pygame

def prediction(rect, v_x, v_y, a, x_end, obs, nb_tours) -> tuple :

    obstacles = []
    obstacles_obj = []
    for ob in obs :
        if str(type(ob)) == """<class 'objects.ObstacleMouvant'>""" :
            obstacles.append(ob.rect.copy())
        else : 
            obstacles.append(ob.rect)
        obstacles_obj.append(ob)

    k_stop = 0

    vx = v_x
    vy = v_y

    while k_stop < nb_tours : 

        if rect.right < x_end :

            k_stop += 1

            if rect.top <= 0 :
                vy = abs(vy)
            elif rect.bottom >= 720: 
                vy = -abs(vy)

            if rect.left <= 0 :
                vx = abs(vx)
            elif rect.right >= 1080 :
                vx = -abs(vx)

            if rect.collidelist(obstacles) >= 0 :
                i = 0
                for obstacle in obstacles : 

                    if str(type(ob)) == """<class 'objects.ObstacleMouvant'>""" :
                        obs_mouvant = obstacles_obj[i]
                        obstacle.x += obs_mouvant.vx*obs_mouvant.a
                        obstacle.y += obs_mouvant.vy*obs_mouvant.a

                    if rect.colliderect(obstacle) :

                        original_vx = vx
                        original_vy = vy

                        #Touche le haut ou le bas d'un obstacle
                        if (rect.left > obstacle.left and rect.right < obstacle.right):
                            if rect.top > obstacle.top and rect.top < obstacle.bottom :
                                vy = abs(vy)
                            elif rect.bottom > obstacle.top and rect.bottom < obstacle.bottom : 
                                vy = -abs(vy)
                        
                        #Touche le côté gauche ou droite d'un obstacle
                        if rect.top > obstacle.top and rect.bottom < obstacle.bottom : 
                            if rect.left > obstacle.left and rect.left < obstacle.right :
                                vx = abs(vx)
                            elif rect.right > obstacle.left and rect.right < obstacle.right : 
                                vx = -abs(vx)

                        #Touche un angle
                        if original_vx == vx and original_vy == vy :

                            if rect.collidepoint(obstacle.bottomright) : 
                                dx = obstacle.right - rect.left
                                dy = obstacle.bottom - rect.top

                                if vx < 0 and vy < 0 and abs(dx-dy) <= 2 :
                                    vx = abs(vx)
                                    vy = abs(vy)
                                elif vx < 0 and vy > 0 : 
                                    vx = abs(vx)
                                elif vx > 0 and vy < 0 : 
                                    vy = abs(vy)
                                else : 
                                    comparaison = compare_impact(dx, dy, vx, vy)
                                    vx, vy = comparaison[0], comparaison[1]
                            
                            if rect.collidepoint(obstacle.topright) : 
                                dx = obstacle.right - rect.left
                                dy = abs(obstacle.top - rect.bottom)
                                
                                if vx < 0 and vy > 0 and abs(dx-dy) <= 2 :
                                    vx = abs(vx)
                                    vy = -abs(vy)
                                elif vx < 0 and vy < 0 : 
                                    vx = abs(vx)
                                elif vx > 0 and vy > 0 : 
                                    vy = -abs(vy)
                                else : 
                                    comparaison = compare_impact(dx, dy, vx, vy)
                                    vx, vy = comparaison[0], comparaison[1]

                            if rect.collidepoint(obstacle.topleft) : 
                                dx = abs(obstacle.left - rect.right)
                                dy = abs(obstacle.top - rect.bottom)

                                if vx > 0 and vy > 0 and abs(dx-dy) <= 2 :
                                    vx = -abs(vx)
                                    vy = -abs(vy)
                                elif vx > 0 and vy < 0 : 
                                    vx = -abs(vx)
                                elif vx < 0 and vy > 0 : 
                                    vy = -abs(vy)
                                else : 
                                    comparaison = compare_impact(dx, dy, vx, vy)
                                    vx, vy = comparaison[0], comparaison[1]

                            if rect.collidepoint(obstacle.bottomleft) : 
                                dx = abs(obstacle.left - rect.right)
                                dy = obstacle.bottom - rect.top
                                
                                if vx > 0 and vy < 0 and abs(dx-dy) <= 2 :
                                    vx = -abs(vx)
                                    vy = abs(vy)
                                elif vx > 0 and vy > 0 : 
                                    vx = -abs(vx)
                                elif vx < 0 and vy < 0 : 
                                    vy = abs(vy)
                                else : 
                                    comparaison = compare_impact(dx, dy, vx, vy)
                                    vx, vy = comparaison[0], comparaison[1]

                    i += 1

            rect.x += vx*a
            rect.y += vy*a

        else : 
            break

    return (rect.center, vx, vy)

#fonction qui permet de trouver la coordonnée y future
def find_y(point, abs_x, vx, vy) -> float :
    coeff_a = vy/vx
    ord_y = coeff_a*(abs_x - point[0]) + point[1]
    return ord_y

#compare la différence d'abscisse et la différence d'ordonnée pour établir dans quel sens se fait la déviation 
#(dans le cas d'un angle notamment)
def compare_impact(dx, dy, vx, vy) :
    if dx > dy : 
        vy *= -1
    elif dy > dx :
        vx *= -1

    return  [vx, vy]

#permet de renvoyer l'angle en fonction des coordonnées du vecteur directeur
def return_angle(vx, vy) : 
    v = math.sqrt(vx**2 + vy**2)
    if v != 0 :
        cos = vx/v
        sin = vy/v
        angle = 180*math.acos(cos)/math.pi
        if sin < 0 : 
            angle *= -1
        return angle
    else : 
        return 0

#renvoie la distance entre deux points
def norme(A:tuple, B:tuple) :
    vx = B[0] - A[0]
    vy = B[1] - A[1]
    return math.sqrt(vx**2 + vy**2) 

#vérifie si un projectile va toucher un obstacle sur sa trajectoire
def verification(obstacles:list, coords, rect:pygame.rect.Rect, vx, x_objectif) : 
    rect.center = coords
    while rect.left > x_objectif :
        if rect.collidelist(obstacles) >= 0 :
            return False
        else : 
            rect.x += vx
    
    return True