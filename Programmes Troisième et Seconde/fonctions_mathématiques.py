import math

def coefficient_directeur(xA, yA, xB, yB) :
    m = (yB - yA)/(xB -xA)
    return m

def equation_droite(xA, yA, xB, yB) :
    m = coefficient_directeur(xA, yA, xB, yB)
    p = yA - m*xA
    if p < 0 :
        signe = "-"
        p = abs(p)
    else :
        signe = "+"
    equation = str(m) + "x " + signe + str(p)
    return equation

def milieu(xA, yA, xB, yB) :
    x = (xA + xB)/2
    y = (yA + yB)/2
    milieu = [x, y]
    return milieu

def déterminant(xU, yU, xV, yV) :
    det = xU*yV - yU*xV
    return det

def vecteurs_colinéaires(xU, yU, xV, yV) :
    det = déterminant(xU, yU, xV, yV)
    if det == 0 :
        colinéarité = True
    else :
        colinéarité = False
    return colinéarité

def parallélogramme(xA, yA, xB, yB, xC, yC, xD, yD) :
    xAB = xB - xA
    yAB = yB - yA
    xDC = xC - xD
    yDC = yC - yD
    if xAB == xDC and yAB == yDC :
        parallélogramme = True
    else :
        parallélogramme = False
    return parallélogramme

def losange(xA, yA, xB, yB, xC, yC, xD, yD) :
    if parallélogramme(xA, yA, xB, yB, xC, yC, xD, yD) == True :
        xAB = xB - xA
        yAB = yB - yA
        xBC = xC - xB
        yBC = yC - yB
        if abs(xAB) == abs(xBC) and abs(yAB) == abs(yBC) :
            losange = True
        else :
            losange = False
    else :
        losange = False
    return losange

def nombre_premier(x) :
    for i in range(1, x) :
        if x%i == 0 and i != 1 and i != x :
            premier = False
            return premier
    premier = True
    return premier

def valuation_p_adique(n, p) :
    règles = None
    error = "Error"
    
    if n <= 0 :
        return error
    if nombre_premier(p) == False :
        return error

    if n%p == 0 :
        k = 1
        while n%(p**k) == 0 :
            k = k + 1
        k = k - 1
        vpn = k
    else :
        vpn = 0
    return vpn

def somme(a, b) :
    x = a + b
    return x

def soustraction(a, b) :
    x = a - b
    return x

def multiplication(a, b) :
    x = a*b
    return x

def division(a, b) :
    x = a/b
    return x

def évolution(x, p) :
    n = x + x*p/100
    return n

def fonction_affine(m, p, x) :
    f = m*x + p
    return f

def puissances_successives(a, b) :
    puissances = []
    for x in range(1, b+1) :
        p = a**x
        puissances.append(p)
    return puissances

def test_divisibilité(a, b) :
    if a%b == 0 :
        divisibilité = True
    else :
        divisibilité = False
    return divisibilité

def convertisseur_durée_vers_secondes(h, m, s) :
    durée = h*3600 + m*60 + s
    return durée

def convertisseur_durée_vers_hms(durée) :
    h = int(durée/3600)
    m = int((durée-h*3600)/60)
    s = durée-(h*3600)-(m*60)
    d = [h, m, s]
    return d
    
def diviseurs(x) :
    diviseurs = []
    for i in range(1, x+1) :
        if x%i == 0 :
            div = i
            diviseurs.append(div)
    return diviseurs

def parfait(x) :
    div = diviseurs(x)
    del(div[len(div)-1])
    add = 0
    for i in range(0, len(div)) :
        add = add + div[i]
    if add == x :
        nbr_parfait = True
    else :
        nbr_parfait = False
    return nbr_parfait

def décomp_facteurs_premiers(x) :
    a = x
    decomp = []
    while a != 1 :
        for i in range(2, x) :
            if nombre_premier(i) == True :
                if a%i == 0 :
                    nbr = i
                    decomp.append(nbr)
                    a = a/i
    return decomp
