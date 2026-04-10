import pandas as pd
import plotly.express as px

import os
import webbrowser
repertoire = os.path.dirname(os.path.abspath(__file__))

import glob
CARACTERES = "".join([chr(code) for code in range(97,123)]) + "-"

from math import exp

def mot_valide(mot: str):
    global CARACTERES
    # Vérification de la taille du mot
    if len(mot) < 5:
        return False

    # Vérification des lettres dans le mot
    caracteres = CARACTERES
    for lettre in mot:
        if lettre not in caracteres:
            return False
    return True

def is_lettre(caractere: str):
    return caractere == "-" or 96 < ord(caractere) < 123

def is_mot(mot: str):
    lettre_avant = ""
    for lettre in mot:
        if not is_lettre(lettre) or lettre_avant == lettre:
            return False
        lettre_avant = lettre
    return True

def get_texte():
    chemin = os.path.join(repertoire, "data", "**", "*.txt")
    chemins = glob.glob(chemin, recursive=True)

    liste_contenues = []
    for chemin_fichier in chemins:
        with open(chemin_fichier, encoding="utf-8") as fichier:
            contenu = fichier.read().replace("\n", " ")
        liste_contenues.append(contenu)

    return "".join(liste_contenues).lower()

def changement_dico(dico_frequences: dict, motif):
    if motif == "":
        return None

    lettre_debut = motif[0]

    sous_dico = dico_frequences.get(lettre_debut, None)
    if sous_dico is None:
        sous_dico = [0, dict()]

    sous_dico[0] += 1
    dico_frequences[lettre_debut] = sous_dico

    changement_dico(sous_dico[1], motif[1:])
    return None

def calcul_frequence(profondeur_max):
    global CARACTERES
    dico_frequences = {}
    contenu = get_texte()

    for i in range(len(contenu)-1):
        fenetre = contenu[i : i+profondeur_max]

        if not is_mot(fenetre):
            continue

        changement_dico(dico_frequences, fenetre)
    return dico_frequences

def somme_dico(dico_frequences: dict, motif: str):
    if motif == "":
        return 0

    sous_dico = dico_frequences.get(motif[0], None)
    if sous_dico is None:
        return 0

    return sous_dico[0] + somme_dico(sous_dico[1], motif[1:])

def calcul_note(mot: str):
    global dico_frequences
    note = 0

    for i in range(len(mot)):
        note += somme_dico(dico_frequences, mot[i:])

    return note / len(mot)

def afficher_repartition(data_mots):
    data_mots.sort_values('note', ascending=True, inplace=True)
    data_mots["position"] = data_mots["mot"].apply(compter)
    data_mots["taille"] = data_mots["mot"].apply(len)

    figure =  px.scatter(data_mots, x="position", y="note", hover_name='mot', color="note")

    figure.write_html("data\\graphe_repartition.html")
    chemin_graphe = os.path.abspath("data\\graphe_repartition.html")
    webbrowser.open(f"file://{chemin_graphe}")

position_globale = 0
def compter(mot):
    global position_globale
    position_globale += 1
    return position_globale

def sigmoide(note: float):
    return 1 / (1 + exp(-note))

def normalisation(data_note):
    note_max = data_note.max()
    data_note = data_note.apply(lambda note: note_max - note)

    # Z-Score
    moyenne, ecart_type = data_note.mean(), data_note.std()
    data_note = data_note.apply(lambda note: (note - moyenne) / ecart_type)

    # Linéarisation
    data_note = data_note.apply(lambda note: round(sigmoide(note)*10, 2))
    return data_note

def creation_mots():
    chemin = "data\\dico_francais.txt"
    data_mots = pd.read_csv(chemin)

    masque_mots = data_mots["mot"].apply(mot_valide)
    data_mots = data_mots[masque_mots]

    data_mots["note"] = data_mots["mot"].apply(calcul_note)
    data_mots["note"] = normalisation(data_mots["note"])

    return data_mots

dico_frequences = calcul_frequence(7)
if __name__ == '__main__':
    data_mots = creation_mots()
    afficher_repartition(data_mots)
