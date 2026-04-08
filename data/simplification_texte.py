import os
repertoire = os.path.dirname(os.path.abspath(__file__))

import glob

def ligne_valide(ligne: str):
    for lettre in ligne:
        if lettre.isalpha():
            return True
    return False

chemin = os.path.join(repertoire, "**", "*.txt")
chemins = glob.glob(chemin, recursive=True)

for chemin in chemins:
    nom_fichier = chemin.split("\\")[-1]

    with open(chemin, "r+",encoding="utf-8") as fichier:
        lignes = [l for l in fichier if ligne_valide(l)]
        fichier.seek(0)

        fichier.writelines(lignes)
        fichier.truncate()
