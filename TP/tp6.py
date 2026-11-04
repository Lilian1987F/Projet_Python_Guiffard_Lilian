# TP6

# exo1.1 correction utilisé
print("exo 1.1")
import math

def vecteur(A, B):
    return (B[0] - A[0], B[1] - A[1])

def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme(u):
    return math.hypot(u[0], u[1])

def angle(u, v):
    cosinus = produit_scalaire(u, v) / (norme(u) * norme(v))

    if cosinus > 1:
        cosinus = 1.0
    if cosinus < -1:
        cosinus = -1.0
    return math.degrees(math.acos(cosinus))

print(norme((3, 4)), produit_scalaire((1, 2), (3, 4)))
print(angle((1, 0), (1, 1)), angle((1, 0), (0, 1)))
print()

# exo1.2
print("exo 1.2")
def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]

def orientation(A, B, C):
    d = determinant(vecteur(A, B), vecteur(A, C))
    if d > 0:
        return 1
    if d < 0:
        return -1
    return 0

def distance_point_droite(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    return abs(determinant(AB, AP)) / norme(AB)

print(distance_point_droite((0, 0), (0, 1), (1, 0)), math.sqrt(2) / 2)
print(distance_point_droite((3, 4), (0, 0), (1, 0)))
print()

# exo2.1
print("exo 2.1")
print(orientation((0, 0), (1, 0), (1, 1)))
print(orientation((0, 0), (1, 0), (1, -1)))
print(orientation((0, 0), (1, 1), (2, 2)))
print()

# exo2.2
print("exo 2.2")
def aire(polygone):
    somme = 0
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        somme = somme + (x1 * y2 - x2 * y1)
    return abs(somme) / 2

carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
triangle = [(0, 0), (4, 0), (0, 3)]
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire(carre), aire(triangle), aire(maison))
print()

# exo3.1
print("exo 3.1")
def se_coupent(A, B, C, D):

    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0

print(se_coupent((0, 0), (1, 1), (0, 1), (1, 0)))
print(se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))
print(se_coupent((0, 0), (1, 1), (2, 2), (3, 3)))
print()

# exo3.2
print("exo 3.2")
def intersection(A, B, C, D):
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    denominateur = determinant(AB, CD)
    if denominateur == 0:
        return None
    AC = vecteur(A, C)
    t = determinant(AC, CD) / denominateur
    u = determinant(AC, AB) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (A[0] + t * AB[0], A[1] + t * AB[1])
    return None

print(intersection((0, 0), (2, 2), (0, 2), (2, 0)))
print(intersection((0, 0), (1, 0), (0, 1), (1, 1)))
print(intersection((0, 0), (1, 1), (2, 2), (3, 3)))
print()

# exo4.1 correction utilisé
print("exo 4.1")
def dedans(P, polygone):
    x, y = P
    n = len(polygone)
    interieur = False
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]

        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur

maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]

for P in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
    print(P, dedans(P, maison))

print()

# exo4.2 correction utilisé
print("exo 4.2")
import random

maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]

random.seed(0)
tirages = 200000
touches = 0
for i in range(tirages):
    P = (random.uniform(0, 2), random.uniform(0, 2.5))
    if dedans(P, maison):
        touches = touches + 1

aire_rectangle = 2 * 2.5
print("estimation :", aire_rectangle * touches / tirages)
print()

# exo5.1 correction utilisé
print("exo 5.1")
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]

import matplotlib.pyplot as plt

def aire(polygone):
    somme = 0
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        somme = somme + (x1 * y2 - x2 * y1)
    return abs(somme) / 2

def tracer_polygone(polygone, points=()):
    xs = []
    ys = []
    for s in polygone:
        xs.append(s[0])
        ys.append(s[1])
    xs.append(polygone[0][0])
    ys.append(polygone[0][1])
    plt.figure(figsize=(5, 5))
    plt.plot(xs, ys, color="black")
    for P in points:
        if dedans(P, polygone):
            couleur = "green"
        else:
            couleur = "red"
        plt.scatter([P[0]], [P[1]], color=couleur)
    plt.axis("equal")
    plt.title("Vert : dedans, rouge : dehors")

etoile = []
for k in range(10):
    if k % 2 == 0:
        rayon = 2
    else:
        rayon = 0.8
    theta = math.pi / 2 + k * math.pi / 5
    etoile.append((rayon * math.cos(theta), rayon * math.sin(theta)))

print(round(aire(etoile), 4))
print(dedans((0, 0), etoile), dedans((0, 1.5), etoile), dedans((1.2, 1.2), etoile))

tracer_polygone(etoile, [(0, 0), (0, 1.5), (1.2, 1.2), (0, 1.9)])
plt.show()
print()

# exo6.1
print("exo 6.1")
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]

def zone_de(P, zones):
    for indice in range(len(zones)):
        if dedans(P, zones[indice]):
            return indice
    return None

zones = [maison, [(3, 0), (4, 0), (4, 1), (3, 1)]]
for P in ((1, 1), (3.5, 0.5), (2.5, 0.5)):
    print(P, zone_de(P, zones))

print()
