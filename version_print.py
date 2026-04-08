from notation import *
from main import mot_mystere, verification, lettre_valide, completer_mot

def demande_niveau():
    niveau = input("Quel difficulté ? : ")

    while niveau not in ["0", "1", "2", "3"]:
        print("Niveau invalide !")
        niveau = input("Quel difficulté ? : ")

    return int(niveau)

def choix_niveau():
    global data_mots

    dico_complexe = {0: ("Facile",10), 1: ("Moyen",8), 2: ("Difficile",6), 3: ("Impossible",4)}

    print("Niveaux:")
    for i in range(4):
        print(" - "+dico_complexe[i][0]+": "+str(i))

    niveau = demande_niveau()
    plafond_bas = niveau*2.5
    plafond_haut = plafond_bas + 2.5

    data_filtrer = data_mots.loc[(data_mots["note"] >= plafond_bas), :]
    data_filtrer = data_filtrer.loc[(data_filtrer["note"] <= plafond_haut), :]
    return data_filtrer, dico_complexe[niveau][1]

def choix_mot():
    data_filtrer, nb_tentatives = choix_niveau()

    ligne = data_filtrer.sample(n=1)

    return ligne["mot"].iloc[0], nb_tentatives, ligne["note"].iloc[0]

data_mots = creation_mots()
# ------------------------------------
# ------------------------------------

def mot_mystere(mot: str):
    myst = ""

    for lettre in mot:
        if lettre == "-":
            myst += "- "
        else:
            myst += "_ "
    return myst[:-1]

def demander_lettre(deja_choisies: str):
    lettre_joueur = input("→ Veuillez choisir une lettre : ")

    while not lettre_valide(lettre_joueur.lower(), deja_choisies):
        print("Votre lettre n'est pas valide !")
        lettre_joueur = input("→ Veuillez choisir une lettre : ")

    return lettre_joueur

def afficher_etat(nb_tentatives: int, deja_choisies: str, myst: str):
    print("-"*20)

    if len(deja_choisies) != 0:
        print("Vous avez déjà choisi : ")
        print(deja_choisies)

    print("Il vous reste "+str(nb_tentatives)+" tentatives !")
    print("→ "+myst)

    print("-" * 20)

def afficher_resultat(victoire: bool, mot: str, note: int):
    print("-" * 20)
    if victoire:
        print("Bien joué ! Vous avez gagné ! 🎊")
    else:
        print("Loser... Le mot était : "+mot)
    print("La note de votre mot était de : "+str(note)+"/10")

def jeu():
    mot, nb_tentatives, note = choix_mot()
    myst = mot_mystere(mot)

    deja_choisies, bonnes_lettres = "", set()
    taille_objectif = len(set(mot)) - (1 if "-" in mot else 0)

    while nb_tentatives != 0:
        afficher_etat(nb_tentatives, deja_choisies, myst)

        lettre_joueur = demander_lettre(deja_choisies)
        deja_choisies += lettre_joueur

        if verification(lettre_joueur, mot):
            myst = completer_mot(lettre_joueur, mot, myst)
            bonnes_lettres.add(lettre_joueur)
        else:
            nb_tentatives -= 1

        if len(bonnes_lettres) == taille_objectif:
            break

    afficher_resultat(len(bonnes_lettres) == taille_objectif, mot, note)

if __name__ == '__main__':
    while True:
        jeu()