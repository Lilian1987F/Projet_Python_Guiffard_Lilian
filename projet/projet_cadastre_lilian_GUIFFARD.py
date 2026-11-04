import math
import random
from fractions import Fraction
import matplotlib.pyplot as plt


def vecteur(A, B):
    return (B[0] - A[0], B[1] - A[1])

def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]

def norme(u):
    return math.hypot(u[0], u[1])

def orientation(A, B, C, tolerance=1e-9):

    d = determinant(vecteur(A, B), vecteur(A, C))
    if d > tolerance:
        return 1
    if d < -tolerance:
        return -1
    return 0

def distance_point_segment(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    longueur2 = AB[0] ** 2 + AB[1] ** 2
    if longueur2 == 0:
        return norme(AP)
    t = (AP[0] * AB[0] + AP[1] * AB[1]) / longueur2
    t = max(0, min(1, t))
    projete = (A[0] + t * AB[0], A[1] + t * AB[1])
    return norme(vecteur(P, projete))

def se_coupent(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0


def aire(parcelle):

    somme = 0
    n = len(parcelle)
    for i in range(n):
        x1, y1 = parcelle[i]
        x2, y2 = parcelle[(i + 1) % n]
        somme = somme + (x1 * y2 - x2 * y1)
    return abs(somme) / 2

def perimetre(parcelle):
    total = 0
    n = len(parcelle)
    for i in range(n):
        total = total + norme(vecteur(parcelle[i], parcelle[(i + 1) % n]))
    return total

def centre(parcelle):

    n = len(parcelle)
    a = 0
    cx = 0
    cy = 0
    for i in range(n):
        x1, y1 = parcelle[i]
        x2, y2 = parcelle[(i + 1) % n]
        c = x1 * y2 - x2 * y1
        a = a + c
        cx = cx + (x1 + x2) * c
        cy = cy + (y1 + y2) * c
    a = a / 2
    return (cx / (6 * a), cy / (6 * a))

def sur_le_bord(P, parcelle, tolerance=1e-9):
    n = len(parcelle)
    for i in range(n):
        if distance_point_segment(P, parcelle[i], parcelle[(i + 1) % n]) < tolerance:
            return True
    return False

def dedans(P, parcelle):

    x, y = P
    n = len(parcelle)
    interieur = False
    for i in range(n):
        x1, y1 = parcelle[i]
        x2, y2 = parcelle[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur

def strictement_dedans(P, parcelle):
    return dedans(P, parcelle) and not sur_le_bord(P, parcelle)

def points_test(parcelle):

    pts = list(parcelle)
    n = len(parcelle)
    for i in range(n):
        A = parcelle[i]
        B = parcelle[(i + 1) % n]
        pts.append(((A[0] + B[0]) / 2, (A[1] + B[1]) / 2))
    pts.append(centre(parcelle))
    return pts

def se_chevauchent(P, Q):

    for i in range(len(P)):
        for j in range(len(Q)):
            if se_coupent(P[i], P[(i + 1) % len(P)], Q[j], Q[(j + 1) % len(Q)]):
                return True

    for pt in points_test(P):
        if strictement_dedans(pt, Q):
            return True
    for pt in points_test(Q):
        if strictement_dedans(pt, P):
            return True
    return False


def produit(A, B):
    n, p, q = len(A), len(A[0]), len(B[0])
    C = [[0] * q for i in range(n)]
    for i in range(n):
        for j in range(q):
            for k in range(p):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]
    return C

def translation(tx, ty):
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]

def rotation(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]

def transformer(parcelle, M):
    resultat = []
    for (x, y) in parcelle:
        colonne = produit(M, [[x], [y], [1]])
        resultat.append((colonne[0][0], colonne[1][0]))
    return resultat

def tourner_autour_du_centre(parcelle, angle):
    cx, cy = centre(parcelle)

    M = produit(translation(cx, cy), produit(rotation(angle), translation(-cx, -cy)))
    return transformer(parcelle, M)


class Cadastre:
    def __init__(self):
        self.parcelles = {}

    def ajouter(self, nom, sommets):
        if len(sommets) < 3:
            print("une parcelle a au moins 3 sommets :", nom)
            return
        self.parcelles[nom] = sommets

    def surface_totale(self):
        total = 0
        for nom in self.parcelles:
            total = total + aire(self.parcelles[nom])
        return total

    def trouver_parcelle(self, P):
        for nom in self.parcelles:
            if dedans(P, self.parcelles[nom]):
                return nom
        return None

    def conflits(self):
        liste = []
        noms = list(self.parcelles)
        for i in range(len(noms)):
            for j in range(i + 1, len(noms)):
                if se_chevauchent(self.parcelles[noms[i]], self.parcelles[noms[j]]):
                    liste.append((noms[i], noms[j]))
        return liste

    def afficher(self):
        print("nom | aire (m2) | aire (ha) | perimetre (m)")
        for nom in self.parcelles:
            p = self.parcelles[nom]
            print(nom, "|", round(aire(p), 2), "|", round(aire(p) / 10000, 4), "|", round(perimetre(p), 2))

    def tracer(self, points=(), fichier="cadastre.png"):
        plt.figure(figsize=(7, 6))
        for nom in self.parcelles:
            p = self.parcelles[nom]
            xs = [s[0] for s in p] + [p[0][0]]
            ys = [s[1] for s in p] + [p[0][1]]
            plt.fill(xs, ys, alpha=0.3)
            plt.plot(xs, ys, color="black")
            cx, cy = centre(p)
            plt.text(cx, cy, nom, ha="center")
        for P in points:
            nom = self.trouver_parcelle(P)
            couleur = "green" if nom is not None else "red"
            plt.scatter([P[0]], [P[1]], color=couleur, zorder=5)
        plt.axis("equal")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("Plan du cadastre")
        plt.savefig(fichier)
        plt.show()


if __name__ == "__main__":
    cad = Cadastre()
    cad.ajouter("A", [(0, 0), (100, 0), (100, 60), (0, 60)])
    cad.ajouter("B", [(100, 0), (180, 0), (180, 40), (140, 40), (140, 90), (100, 90)])
    cad.ajouter("C", [(90, 50), (130, 50), (130, 80), (90, 80)])
    cad.ajouter("D", [(0, 70), (60, 70), (60, 120), (0, 120)])

    print("=== 1. parcelles ===")
    cad.afficher()
    print("surface totale :", round(cad.surface_totale(), 2), "m2")
    print()

    print("=== 2. de quelle parcelle est ce point ? ===")
    points = [(50, 30), (120, 20), (160, 30), (30, 100), (200, 200), (95, 65)]
    for P in points:
        print(P, "->", cad.trouver_parcelle(P))
    print()

    print("=== 3. parcelles qui se chevauchent ===")
    for (a, b) in cad.conflits():
        print("conflit entre", a, "et", b)
    print("A et D (separees) :", se_chevauchent(cad.parcelles["A"], cad.parcelles["D"]))
    print("A et B (voisines, meme bord) :", se_chevauchent(cad.parcelles["A"], cad.parcelles["B"]))
    print()

    print("=== 4. verification de l'aire par Monte-Carlo ===")
    random.seed(0)
    B = cad.parcelles["B"]
    tirages = 100000
    touches = 0
    for i in range(tirages):
        P = (random.uniform(100, 180), random.uniform(0, 90))
        if dedans(P, B):
            touches = touches + 1
    estimation = 80 * 90 * touches / tirages
    print("aire de B (formule) :", aire(B))
    print("aire de B (Monte-Carlo) :", round(estimation, 1))
    print()

    print("=== 5. la rotation conserve l'aire ===")
    A = cad.parcelles["A"]
    A2 = tourner_autour_du_centre(A, 0.3)
    print("aire avant :", aire(A))
    print("aire apres :", aire(A2))
    print("egales a la tolerance pres ?", math.isclose(aire(A), aire(A2), rel_tol=1e-12))
    print("egales avec == ?", aire(A) == aire(A2))
    print()

    print("=== 6. flottants contre fractions ===")

    mesures = [(0, 0), (0.1, 0), (0.1, 0.3), (0, 0.3)]
    exact = [(Fraction(str(x)), Fraction(str(y))) for (x, y) in mesures]
    print("aire en flottants :", aire(mesures))
    print("aire exacte :", aire(exact), "=", float(aire(exact)))
    print("difference :", aire(mesures) - float(aire(exact)))

    decalage = 100000000.1
    petit = [(decalage + x, decalage + y) for (x, y) in [(0, 0), (10, 0), (10, 10), (0, 10)]]
    print("parcelle 10x10 loin de l'origine :", aire(petit), "(attendu 100)")
    recentre = [(x - petit[0][0], y - petit[0][1]) for (x, y) in petit]
    print("apres recentrage sur un sommet :", aire(recentre))
    print()

    cad.tracer(points)