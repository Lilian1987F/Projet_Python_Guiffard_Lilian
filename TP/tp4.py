# TP4

# exo1.1
print("exo 1.1")
def transposee(A):
    lignes = len(A)
    colonnes = len(A[0])
    T = []
    for j in range(colonnes):
        nouvelle_ligne = []
        for i in range(lignes):
            nouvelle_ligne.append(A[i][j])
        T.append(nouvelle_ligne)
    return T

print(transposee([[1, 2, 3], [4, 5, 6]]))

print()

# exo2.1
print("exo 2.1")
def produit(A, B):
    n = len(A)
    p = len(A[0])
    if len(B) != p:
        print("dimensions incompatibles")
        return None
    q = len(B[0])

    C = []
    for i in range(n):
        C.append([0] * q)
    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme = somme + A[i][k] * B[k][j]
            C[i][j] = somme
    return C

identite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]

print(produit(A, identite) == A)

print(produit([[1, 2], [3, 4]], [[0, 1], [1, 0]]))
print()

# exo2.2
print("exo 2.2")
import random
import time

def produit(A, B):
    n = len(A)
    p = len(A[0])
    q = len(B[0])
    C = []
    for i in range(n):
        C.append([0] * q)
    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme = somme + A[i][k] * B[k][j]
            C[i][j] = somme
    return C

def matrice_aleatoire(n):
    M = []
    for i in range(n):
        ligne = []
        for j in range(n):
            ligne.append(random.random())
        M.append(ligne)
    return M

random.seed(42)
temps = []
for n in (40, 80, 120):
    A = matrice_aleatoire(n)
    B = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(A, B)
    t = time.perf_counter() - debut
    temps.append(t)
    print("n =", n, ": temps =", round(t, 4), "s")

print("rapport 80/40 :", round(temps[1] / temps[0], 1))
print()

# exo3.1
print("exo 3.1")
import numpy as np

random.seed(42)
n = 120
A = matrice_aleatoire(n)
B = matrice_aleatoire(n)

debut = time.perf_counter()
produit(A, B)
t_python = time.perf_counter() - debut

An = np.array(A)
Bn = np.array(B)
debut = time.perf_counter()
An @ Bn
t_numpy = time.perf_counter() - debut

print("python pur :", round(t_python, 4), "s")
print("numpy      :", round(t_numpy, 6), "s")
print("rapport    :", round(t_python / max(t_numpy, 1e-9)))
print()

# exo4.1
print("exo 4.1")
def resoudre(A, b, tolerance=1e-14):
    n = len(A)

    M = []
    for i in range(n):
        M.append(list(A[i]) + [b[i]])

    for k in range(n):

        meilleure = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")

        M[k], M[meilleure] = M[meilleure], M[k]

        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
    return x

A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
b = [2, -1, 8]
x = resoudre(A, b)
print("solution :", [round(v, 10) for v in x])

verif = []
for i in range(3):
    s = 0
    for j in range(3):
        s = s + A[i][j] * x[j]
    verif.append(round(s, 10))
print("A x      :", verif)
print("b        :", b)
print()

# exo4.2
print("exo 4.2")
def resoudre(A, b, tolerance=1e-14):
    n = len(A)
    M = []
    for i in range(n):
        M.append(list(A[i]) + [b[i]])
    for k in range(n):
        meilleure = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")
        M[k], M[meilleure] = M[meilleure], M[k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
    return x

random.seed(7)
n = 50
A = []
for i in range(n):
    A.append([random.random() for j in range(n)])
b = [random.random() for i in range(n)]

mienne = resoudre(A, b)
numpy_x = np.linalg.solve(np.array(A), np.array(b))

ecart = 0
for i in range(n):
    d = abs(mienne[i] - numpy_x[i])
    if d > ecart:
        ecart = d
print("ecart maximal :", ecart)
print("coincident a 1e-9 pres :", ecart < 1e-9)
print()

# exo5.1
print("exo 5.1")
def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

n = 12
H = hilbert(n)
x_vrai = np.ones(n)
b = H @ x_vrai
x_solve = np.linalg.solve(H, b)
x_inverse = np.linalg.inv(H) @ b
print("erreur avec solve   :", float(np.max(np.abs(x_solve - x_vrai))))
print("erreur avec inv @ b :", float(np.max(np.abs(x_inverse - x_vrai))))
print("conditionnement     :", float(np.linalg.cond(H)))

print()
print("solve est plus proche de la vraie solution que inv @ b.")
print("Le conditionnement est enorme (~1e16) : le probleme est mal pose,")
print("plus aucun chiffre du resultat n'est fiable.")
print()

# exo6.1
print("exo 6.1")
def rotation(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s], [s, c]])

gauche = rotation(np.pi / 3) @ rotation(np.pi / 6)
droite = rotation(np.pi / 2)
print(np.allclose(gauche, droite))
print(np.round(droite, 10))

print()

# exo7.1
print("exo 7.1")
def determinant(A):
    n = len(A)
    M = []
    for ligne in A:
        M.append(list(ligne))
    det = 1.0
    for k in range(n):
        meilleure = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det = det * M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] = M[i][j] - facteur * M[k][j]
    return det

A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print("mon determinant :", determinant(A))
print("numpy           :", float(np.linalg.det(np.array(A, dtype=float))))
print(determinant([[1, 2], [2, 4]]))
print()

# exo8.1
print("exo 8.1")
from fractions import Fraction

n = 12
H = []
for i in range(n):
    ligne = []
    for j in range(n):
        ligne.append(Fraction(1, i + j + 1))
    H.append(ligne)

b = []
for ligne in H:
    b.append(sum(ligne))

try:
    resoudre(H, b)
except ValueError as erreur:
    print("premier essai :", erreur)

x = resoudre(H, b, tolerance=0)
print(x)
tout_egal_1 = True
for v in x:
    if v != 1:
        tout_egal_1 = False
print("tout vaut exactement 1 :", tout_egal_1)
print()

# exo9.1
print("exo 9.1")
def translation(tx, ty):
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]])

def rotation_h(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([[c, -s, 0.0],
                     [s, c, 0.0],
                     [0.0, 0.0, 1.0]])

point = np.array([1.0, 0.0, 1.0])
T = translation(3, 1)
R = rotation_h(np.pi / 2)

print("translation puis rotation :", np.round(R @ T @ point, 10))
print("rotation puis translation :", np.round(T @ R @ point, 10))
print()
