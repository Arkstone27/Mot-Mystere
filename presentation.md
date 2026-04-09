# Mot-Mystere
Un jeu inspiré du jeu du pendu, développé dans le cadre des cours de NSI Terminale

## Structure du projet

Il y a 5 fichiers pythons :
- **main.py** qui lance l'interface et le jeu
  
- **frames.py** où 3 frames de l'interface sont présentes :
  - Pour demander un pseudo au démarrage
  - Pour afficher le tableau des scores
  - Pour afficher les titres et le graphique de la répartition des notes
    
- **version_print.py** qui lance le jeu avec comme interface la console python

- **notation.py** qui au lancement calcule les notes des différents mots présent dans dico_francais.txt

- **simplification_texte.py** qui permet d'enlever les espaces dans les fichiers txt contenues dans le répertoire data

## Notation
La notation des mots présents dans le fichier * *dico_francais.txt* * est une partie importante du projet
Après de nombreux tests voici le comment se déroule la calcul final des notes :

1. A partir du texte contenues dans le fichier data on produit une table qui permet de récupérer le nombre d'occurrence de tel lettre après tel lettre (et cela de manière récursive)
   exemple: Il y a 534 occurrences de la lettre a, après cet lettre a, il y a 43 occurrences de la lettre l. Après cet lettre l, il y a 13 occurrences de la lettre i. (On a donc 13 occurrences du motif "ali".

3. 
