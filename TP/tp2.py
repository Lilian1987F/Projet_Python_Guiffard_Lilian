# TP2

# exo1.1
print("exo 1.1")
def diviseurs(n):
    liste = []
    for d in range(1, n + 1):
        if n % d == 0:
            liste.append(d)
    return liste

print(diviseurs(28))
print()

# exo2.1
print("exo 2.1")
def pgcd_naif(a, b):

    meilleur = 1
    for d in range(1, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            meilleur = d
    return meilleur

def pgcd(a, b):

    while b != 0:
        a, b = b, a % b
    return a

print("naif :", pgcd_naif(1071, 462))
print("euclide :", pgcd(1071, 462))
print("meme resultat ?", pgcd_naif(1071, 462) == pgcd(1071, 462))
print()

# exo3.1 correction utilisé
print("exo 3.1")
import time

def est_premier_naif(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 2
    return True

def duree(fonction, argument):
    debut = time.perf_counter()
    fonction(argument)
    fin = time.perf_counter()
    return fin - debut

print("        n |   naif (s)  | racine (s)")
print("----------+-------------+-----------")

anciens = None
for n in (10007, 100003, 1000003):
    t_naif = duree(est_premier_naif, n)
    t_rac = duree(est_premier, n)
    print(f"{n:>9} | {t_naif:.6f} s | {t_rac:.6f} s")
    if anciens is not None:
        print("   -> temps multiplie par", round(t_naif / anciens[0], 1),
              "(naif) et par", round(t_rac / anciens[1], 1), "(racine)")
    anciens = (t_naif, t_rac)

print()
print("Quand n est multiplie par 10, la version naive prend environ 10 fois")
print("plus de temps (elle fait n tours), alors que la version avec la racine")
print("prend environ 3 fois plus de temps (elle fait racine de n tours).")

print()

# exo4.1
print("exo 4.1")
def crible(limite):
    tab = [True] * (limite + 1)
    tab[0] = False
    if limite >= 1:
        tab[1] = False
    d = 2
    while d * d <= limite:
        if tab[d]:
            for multiple in range(d * d, limite + 1, d):
                tab[multiple] = False
        d = d + 1
    premiers = []
    for n in range(limite + 1):
        if tab[n]:
            premiers.append(n)
    return premiers

debut = time.perf_counter()
p = crible(100000)
t_crible = time.perf_counter() - debut

debut = time.perf_counter()
for n in range(100001):
    est_premier(n)
t_un_par_un = time.perf_counter() - debut

print("nombre de premiers (crible) :", len(p))
print(f"temps crible : {t_crible:.4f} s")
print(f"temps un par un : {t_un_par_un:.4f} s")
print()

# exo5.1
print("exo 5.1")
def facteurs(n):
    liste = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            liste.append(d)
            n = n // d
        d = d + 1

    if n > 1:
        liste.append(n)
    return liste

f = facteurs(360)
print(f)

produit = 1
for x in f:
    produit = produit * x
print(produit)

print()

# exo6.1 correction utilisé
print("exo 6.1")
def fibonacci_recursif(n):
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)

precedent = None
for n in (20, 25, 30):
    t = duree(fibonacci_recursif, n)
    print(f"F({n}) : {t:.4f} s")
    if precedent is not None:
        print("   -> temps multiplie par", round(t / precedent, 1))
    precedent = t

print()
print("Quand n augmente de 5, le temps est multiplie par une dizaine.")
print("C'est une croissance exponentielle.")
print()

# exo6.2
print("exo 6.2")
appels = {}

def fibonacci_compte(n):

    if n in appels:
        appels[n] = appels[n] + 1
    else:
        appels[n] = 1
    if n < 2:
        return n
    return fibonacci_compte(n - 1) + fibonacci_compte(n - 2)

resultat = fibonacci_compte(30)
print("F(30) =", resultat)
print("F(1) :", appels[1])
print()

# exo6.3
print("exo 6.3")
def fibonacci(n):
    precedent = 0
    courant = 1
    for i in range(n):
        precedent, courant = courant, precedent + courant
    return precedent

ok = True
for n in range(26):
    if fibonacci(n) != fibonacci_recursif(n):
        ok = False
print("memes resultats jusqu'a 25 ?", ok)

debut = time.perf_counter()
grand = fibonacci(10000)
t = time.perf_counter() - debut
print("fibonacci(10000) a", len(str(grand)), "chiffres")
print(f"calcule en {t:.6f} s")
print()

# exo7.1
print("exo 7.1")
def euclide_etendu(a, b):

    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v

print(euclide_etendu(1071, 462))
print()

# exo7.2 correction utilisé
print("exo 7.2")
def puissance_mod_naive(a, e, n):

    resultat = 1
    for i in range(e):
        resultat = resultat * a % n
    return resultat

def puissance_mod(a, e, n):

    resultat = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            resultat = resultat * a % n
        a = a * a % n
        e = e // 2
    return resultat

a = 7
e = 10 ** 7
n = 1000003

print("rapide :", puissance_mod(a, e, n))
print("pow de python :", pow(a, e, n))

debut = time.perf_counter()
r_naive = puissance_mod_naive(a, e, n)
t_naive = time.perf_counter() - debut

debut = time.perf_counter()
r_rapide = puissance_mod(a, e, n)
t_rapide = time.perf_counter() - debut

print("naive :", r_naive)
print("meme resultat ?", r_naive == r_rapide == pow(a, e, n))
print(f"temps naive : {t_naive:.3f} s")
print(f"temps rapide : {t_rapide:.6f} s")
print()
