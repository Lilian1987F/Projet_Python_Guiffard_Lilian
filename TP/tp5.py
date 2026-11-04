# TP5

# exo1.1
print("exo 1.1")
def lettre_vers_nombre(c):
    return ord(c) - ord("A")

def nombre_vers_lettre(n):

    return chr(n % 26 + ord("A"))

print(lettre_vers_nombre("C"), nombre_vers_lettre(2))
for c in "ABCXYZ":
    print(c, nombre_vers_lettre(lettre_vers_nombre(c)) == c)
print()

# exo1.2
print("exo 1.2")
import unicodedata

def nettoyer(texte):

    texte = unicodedata.normalize("NFD", texte)
    resultat = ""
    for c in texte.upper():
        if "A" <= c <= "Z":
            resultat = resultat + c
    return resultat

print(nettoyer("Été, à Paris !"))
print()

# exo2.1
print("exo 2.1")
def nombre_vers_lettre(n):
    return chr(n % 26 + ord("A"))

def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte)
    resultat = ""
    for c in texte.upper():
        if "A" <= c <= "Z":
            resultat = resultat + c
    return resultat

def chiffrer(texte, a, b):
    resultat = ""
    for c in nettoyer(texte):
        x = lettre_vers_nombre(c)
        resultat = resultat + nombre_vers_lettre((a * x + b) % 26)
    return resultat

message = "ATTAQUEALAUBE"
print(chiffrer(message, 5, 8))
print()

# exo3.1
print("exo 3.1")
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

valides = []
for a in range(1, 26):
    if pgcd(a, 26) == 1:
        valides.append(a)

print(valides)
print(len(valides), "valeurs possibles pour a")

print()

# exo3.2
print("exo 3.2")
def inverse_modulaire(a, n):
    a = a % n

    for candidat in range(1, n):
        if (a * candidat) % n == 1:
            return candidat
    raise ValueError(str(a) + " n est pas inversible modulo " + str(n))

print(inverse_modulaire(5, 26))
try:
    inverse_modulaire(4, 26)
except ValueError as erreur:
    print("erreur attendue :", erreur)
print()

# exo4.1 correction utilisé
print("exo 4.1")
def dechiffrer(texte, a, b):
    """Déchiffrement affine. Lève une erreur si la clé n'est pas inversible."""
    a_inverse = inverse_modulaire(a, 26)
    resultat = []
    for c in nettoyer(texte):
        y = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre(a_inverse * (y - b) % 26))
    return "".join(resultat)

message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 5, 8)
print(secret)
print(dechiffrer(secret, 5, 8))
print(dechiffrer(secret, 5, 8) == message)

# une clé invalide est refusée au lieu de produire un résultat faux
try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("cle refusee :", erreur)

print()

# exo5.1
print("exo 5.1")
def toutes_les_clefs(secret):
    resultats = []
    for a in valides:
        for b in range(26):
            resultats.append((a, b, dechiffrer(secret, a, b)))
    return resultats

message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 5, 8)

essais = toutes_les_clefs(secret)
print(len(essais), "clefs essayees")

for a, b, texte in essais[:5]:
    print(a, b, texte)
print("...")
for a, b, texte in essais:
    if texte == message:
        print("la bonne clef :", a, b, texte)
print()

# exo6.1
print("exo 6.1")
texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)
secret_long = chiffrer(texte_long, 7, 12)

def casser(secret):

    meilleure = "A"
    maxi = 0
    for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        n = secret.count(lettre)
        if n > maxi:
            maxi = n
            meilleure = lettre
    print("lettre la plus frequente du chiffre :", meilleure)

    cible = lettre_vers_nombre(meilleure)
    candidats = []
    for a in valides:
        b = (cible - 4 * a) % 26
        candidats.append((a, b, dechiffrer(secret, a, b)))
    return candidats

candidats = casser(secret_long)
print(len(candidats), "candidats au lieu de 312")
for a, b, texte in candidats:
    if texte == texte_long:
        print("trouve : a =", a, "b =", b)
        print(texte[:60])

print()

# exo7.1
print("exo 7.1")
def indice_coincidence(texte):
    N = len(texte)
    total = 0
    for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        n = texte.count(lettre)
        total = total + n * (n - 1)
    return total / (N * (N - 1))

import random
random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = ""
for i in range(len(texte_long)):
    hasard = hasard + random.choice(alphabet)

print("clair  :", round(indice_coincidence(texte_long), 4))
print("affine :", round(indice_coincidence(secret_long), 4))
print("hasard :", round(indice_coincidence(hasard), 4))
print()

# exo8.1
print("exo 8.1")
def vigenere(texte, cle):
    resultat = ""
    texte = nettoyer(texte)
    for i in range(len(texte)):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        resultat = resultat + nombre_vers_lettre(lettre_vers_nombre(texte[i]) + decalage)
    return resultat

secret_vigenere = vigenere(texte_long, "CLE")
print(secret_vigenere[:40])
print("IC vigenere :", round(indice_coincidence(secret_vigenere), 4))
print()

# exo8.2
print("exo 8.2")
for L in range(1, 8):
    colonnes = [secret_vigenere[i::L] for i in range(L)]
    moyenne = sum(indice_coincidence(col) for col in colonnes) / L
    print(f"L = {L} : indice moyen {moyenne:.4f}")
