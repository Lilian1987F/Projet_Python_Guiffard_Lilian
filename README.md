# Outils fondamentaux : TP et projet

Nom : GUIFFARD Lilian
Groupe : B1

## Organisation du dépôt

- `tp/` : mes solutions aux TP du module (`tp1.py` à `tp6.py`, un fichier par TP).
- `projet/` : mon projet personnel, `projet_cadastre.py`.

## Le projet : un petit outil de cadastre

### Ce qu'il fait

Le programme manipule des parcelles de terrain, décrites par la liste de leurs sommets (coordonnées en mètres), et répond à des questions concrètes :

- **Aire et périmètre** d'une parcelle (formule du lacet), surface en m² et en hectares, centre de gravité.
- **Dans quelle parcelle se trouve un point ?** (lancer de rayon).
- **Quelles parcelles se chevauchent ?** Deux parcelles voisines qui partagent un bord ne comptent pas comme un conflit.
- **Déplacer ou tourner une parcelle** avec des matrices en coordonnées homogènes.
- **Un plan** de l'ensemble, enregistré dans `cadastre.png`.

### Notions du cours utilisées

| Notion | Où dans le projet |
|---|---|
| Flottants (TP1) | tolérances dans `orientation` et `sur_le_bord`, comparaison `==` contre `math.isclose`, parcelle loin de l'origine |
| Matrices (TP4) | produit matriciel écrit à la main, translation et rotation en coordonnées homogènes |
| Géométrie du plan (TP6) | déterminant, orientation, croisement de segments, aire, point dans un polygone |
| Fractions (TP1) | aire exacte d'une parcelle à coordonnées décimales |

Le projet n'utilise ni l'arithmétique ni les polynômes du module.

### Comment le lancer

```
py -m pip install matplotlib
py projet_cadastre.py
```

### Ce qu'on doit en observer

Le programme crée quatre parcelles A, B, C, D, dont C empiète volontairement sur A et B. Les sections affichées sont :

1. **Parcelles** : aires et périmètres (A : 6000 m², B : 5200 m², C : 1200 m², D : 3000 m²).
2. **Recherche d'un point** : chaque point test tombe dans la bonne parcelle, ou dans aucune.
3. **Conflits** : le programme trouve A–C et B–C. A et B, voisines par un bord commun, ne sont pas signalées, et A et D, séparées, non plus.
4. **Vérification de l'aire par Monte-Carlo** : sur la parcelle B, 100 000 tirages donnent environ 5205 m² contre 5200 m² par la formule. L'écart vient du hasard et diminue lentement quand on augmente le nombre de tirages.
5. **Rotation** : tourner une parcelle conserve son aire, mais pas exactement en flottants. L'aire de A passe de 6000 à 5999.999999999998. Le test `==` donne `False` alors que `math.isclose` donne `True`.
6. **Flottants** : une parcelle de 10 m sur 10 m située très loin de l'origine (coordonnées de l'ordre de 10⁸) a une aire calculée de **98** au lieu de 100. La formule du lacet soustrait de très grands nombres presque égaux, et les chiffres significatifs disparaissent. En recentrant les coordonnées sur un sommet avant de calculer, on retrouve 100. Pour la parcelle à coordonnées décimales (0,1 × 0,3), l'aire en flottants et l'aire exacte en fractions ne se distinguent pas : l'effet n'apparaît qu'avec de grandes coordonnées.

### Limites

- Deux parcelles strictement identiques ne sont pas toujours détectées comme se chevauchant : je teste des points (sommets, milieux des côtés, centre) et des croisements, mais pas toutes les configurations où les bords coïncident.
- Les parcelles doivent être des polygones simples (sans côtés qui se croisent). Le programme ne le vérifie pas.
- Le centre de gravité n'est pas toujours à l'intérieur d'une parcelle non convexe (en forme de L par exemple), ce qui peut fausser le test de chevauchement dans ce cas.
- Les tolérances (1e-9) sont choisies à la main. Elles conviennent pour des coordonnées en mètres, pas pour n'importe quelle échelle.
- Le projet reste un outil de calcul : il ne lit pas de vrais fichiers cadastraux.

## Usage de l'intelligence artificielle

J'ai utilisé un assistant d'IA pour ce projet. Il m'a servi à comprendre comment orienter le projet et structurer le code pour qu'il fonctionne.

Ce que j'ai fait moi-même : [à compléter avec ce que tu as réellement relu, lancé, modifié ou vérifié].

Les solutions des TP ont aussi été produites avec l'aide de l'assistant, à partir des corrigés du cours, puis reprises dans mon propre format : [à compléter : ce que tu as relu, testé ou modifié].
