# Mot-Mystere

Un jeu inspiré du jeu du pendu, développé dans le cadre des cours de NSI Terminale

## Structure du projet

Il y a 5 fichiers pythons :

* **main.py** qui lance l'interface et le jeu
* **frames.py** où 3 frames de l'interface sont présentes :

  * Pour demander un pseudo au démarrage
  * Pour afficher le tableau des scores
  * Pour afficher les titres et le graphique de la répartition des notes
* **version\_print.py** qui lance le jeu avec comme interface la console python
* **notation.py** qui au lancement calcule les notes des différents mots présent dans dico\_francais.txt
* **simplification\_texte.py** qui permet d'enlever les espaces dans les fichiers txt contenues dans le répertoire data

## Notation

La notation des mots présents dans le fichier *dico\_francais.txt* est une partie importante du projet.
Après de nombreux tests voici comment se déroule la calcul final des notes :

1. A partir du texte contenu dans le répertoire *data* on produit une table qui permet de récupérer le **nombre d'occurrences** de telle lettre après telle lettre (et cela de manière récursive). Par exemple, il y a 534 occurrences de la lettre `a`. Après cette lettre `a`, il y a 43 occurrences de la lettre `l`. Après cette lettre `l`, il y a 13 occurrences de la lettre `i`. On a donc 13 occurrences du motif `ali`.
2. Pour chaque mot on fait la **somme des nombres d'occurrences** des motifs du mot, à partir de la table d'occurrence. On divise la somme obtenue par la taille du mot pour obtenir la note.

![Erreur de chargement du graphe...](https://github.com/Arkstone27/Mot-Mystere/blob/0305da3c92845b1ffc40682129dd4f8683a7ec1f/Figure\_1.png "Figure 1 : Répartition sans normalisation")

5. Problème les notes sont énormes *(cf figure 1)* et mal réparties. Pour rectifier cela, on doit appliquer une fonction de **normalisation** (ex: divisé par le maximum), ici j'ai utilisé la fonction [sigmoïde](https://fr.wikipedia.org/wiki/Sigmo%25C3%25AFde_%28math%25C3%25A9matiques%29). Mais il faut **préparer les notes** avant, on commence donc par faire le [Z-Score](https://fr.wikipedia.org/wiki/Cote_Z_%28statistiques%29) des notes. On soustrait chaque note par la moyenne des notes puis on divise par l'écart-type des notes. Ensuite on passe chaque note dans la fonction sigmoïde et on multiplie par 10 pour obtenir des notes de 0 à 10 pour chaque mot. Le mot avec une note de 10 est donc le plus "complexe" à trouver *(cf figure 2)*.

![Erreur de chargement du graphe...](https://github.com/Arkstone27/Mot-Mystere/blob/0305da3c92845b1ffc40682129dd4f8683a7ec1f/Figure\_2.png "Figure 2 : Répartition avec normalisation")

