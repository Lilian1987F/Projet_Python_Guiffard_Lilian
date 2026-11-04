# TP1

# exo1.1
print("exo 1.1")
n = 2026
d = 7

q = n // d
r = n % d

print("quotient :", q)
print("reste :", r)

print(q * d + r == n)
print()

# exo1.2
print("exo 1.2")
n = 123456789

dernier = n % 10
print("dernier chiffre :", dernier)

sans_dernier = n // 10
print("sans le dernier chiffre :", sans_dernier)
print()

# exo2.1
print("exo 2.1")
total = 0
for i in range(1000):
    total = total + 0.1

print("resultat :", total)
print("ecart avec 100 :", total - 100)
print()

# exo2.2
print("exo 2.2")
def presque_egaux(a, b, tolerance=1e-9):

    if abs(a - b) <= tolerance:
        return True
    else:
        return False

print(presque_egaux(0.1 + 0.2, 0.3))
print(presque_egaux(1.0, 1.5))
print(0.1 + 0.2 == 0.3)
print()

# exo3.1
print("exo 3.1")
for i in range(1, 11):
    print("7 x", i, "=", 7 * i)
print()

# exo3.2
print("exo 3.2")
n = 100
somme = 0
for i in range(1, n + 1):
    somme = somme + i

print("avec la boucle :", somme)
print("avec la formule :", n * (n + 1) // 2)
print()

# exo4.1
print("exo 4.1")
def nombre_de_chiffres(n):
    compte = 1
    while n >= 10:
        n = n // 10
        compte = compte + 1
    return compte

print(nombre_de_chiffres(2026))
print(nombre_de_chiffres(7))
print(nombre_de_chiffres(10 ** 60))
print()

# exo5.1 Corrigé utilisé
print("exo 5.1")
import math

def heron(a, tolerance=1e-12):
    if a < 0:
        raise ValueError("a est negatif")
    if a == 0:
        return 0.0

    x = float(a)
    tours = 0
    while True:
        suivant = 0.5 * (x + a / x)
        tours = tours + 1

        if abs(suivant - x) <= tolerance * abs(suivant):
            return suivant
        x = suivant

r = heron(2)
print("heron :", r)
print("math.sqrt :", math.sqrt(2))
print("ecart < 1e-12 ?", abs(r - math.sqrt(2)) < 1e-12)
print()

# exo6.1
print("exo 6.1")
def vers_binaire(n):
    if n == 0:
        return "0"
    resultat = ""
    while n > 0:
        resultat = str(n % 2) + resultat
        n = n // 2
    return resultat

print(vers_binaire(37))
print(vers_binaire(0))
print(vers_binaire(1024))

# exo6.2
print("exo 6.2")
import sys

eps = 1.0
while 1.0 + eps / 2 != 1.0:
    eps = eps / 2

print("mon epsilon :", eps)
print("celui de python :", sys.float_info.epsilon)
print("egal a 2**-52 ?", eps == 2 ** -52)
print()

# exo7.1
print("exo 7.1")
def racines_naif(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine reelle")
    r = math.sqrt(delta)
    x1 = (-b - r) / (2 * a)
    x2 = (-b + r) / (2 * a)
    return x1, x2

petite, grande = racines_naif(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande, "(attendu : 1)")
print()

# exo7.2
print("exo 7.2")
def racines(a, b, c):
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("pas de racine reelle")
    r = math.sqrt(delta)

    if b >= 0:
        x1 = (-b - r) / (2 * a)
    else:
        x1 = (-b + r) / (2 * a)

    x2 = c / (a * x1)

    if x1 < x2:
        return x1, x2
    else:
        return x2, x1

petite, grande = racines(1.0, -1e8, 1.0)
print(petite, grande)
print("produit :", petite * grande)

for x in (petite, grande):
    residu = x * x - 1e8 * x + 1
    print("residu :", residu)
print()

# exo7.3
print("exo 7.3")
from fractions import Fraction

total = Fraction(0)
for i in range(1000):
    total = total + Fraction(1, 10)

print(total)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
print()
