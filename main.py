import customtkinter as ctk
from tkinter import messagebox
ctk.set_appearance_mode("dark")

from notation import *
from frames import *
data_mots = creation_mots()

def choix_niveau(niveau):
    global data_mots

    dico_complexe = {"Facile": (0,10), "Moyen": (1,8), "Difficile": (2,6), "Impossible": (3,4)}
    seuil = dico_complexe[niveau][0]

    plafond_bas = seuil*2.5
    plafond_haut = plafond_bas + 2.5

    data_filtrer = data_mots.loc[(data_mots["note"] >= plafond_bas), :]
    data_filtrer = data_filtrer.loc[(data_filtrer["note"] <= plafond_haut), :]
    return data_filtrer, dico_complexe[niveau][1]

def mot_mystere(mot: str):
    myst = ""

    for lettre in mot:
        if lettre == "-":
            myst += "- "
        else:
            myst += "_ "
    return myst[:-1]

def verification(lettre: str, mot: str):
    return lettre in mot

def lettre_valide(lettre: str, deja_choisies: str):
    if len(lettre) != 1 or lettre in deja_choisies:
        return False

    if 96 < ord(lettre) < 123:
        return True

    return False

def completer_mot(lettre_joueur: str, mot: str, myst: str):
    new_myst = ""

    for indice in range(len(mot)):
        if mot[indice] == lettre_joueur:
            new_myst += lettre_joueur
        else:
            new_myst += myst[indice*2]
        new_myst += " "
    return new_myst[:-1]

# ------------------
# ------------------

class FrameJeu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#333333", border_width=5,  **kwargs)
        self.master = master

        self.btn_partie = ctk.CTkButton(self, text="Nouvelle Partie", command=self.new_jeu, font=("Courier", 15, "bold"))
        self.btn_partie.pack(pady=(20,0))

        # Niveau
        ctk.CTkLabel(self, text="Quel difficulté ?", font=("Courier", 15, "bold")).pack()

        self.niveau_var = ctk.StringVar(value="Facile")
        self.combobox_niveau = ctk.CTkComboBox(self, values=["Facile","Moyen", "Difficile", "Impossible"], variable=self.niveau_var, state="readonly")
        self.combobox_niveau.pack(padx=(20,0), pady=(0,10))

        # Mot mystere
        self.label_myst = ctk.CTkLabel(self, text="X X X X X", font=("Courier",20))
        self.label_myst.pack(pady=(0,0), padx=20)

        self.label_lettres = ctk.CTkLabel(self, text="Lettre déjà choisis :", font=("Courier", 15, "bold"))
        self.label_lettres.pack(padx=20)

        self.label_tentatives = ctk.CTkLabel(self, text="Tentatives :", font=("Courier", 15, "bold"))
        self.label_tentatives.pack(pady=(0, 20))

        # Resultat
        self.label_resultat = ctk.CTkLabel(self, text="", font=("Courier", 15, "bold"))

        # Touches
        self.partie = False

    def choix_mot(self):
        data_filtrer, nb_tentatives = choix_niveau(self.niveau_var.get())

        ligne = data_filtrer.sample(n=1)

        self.mot = ligne["mot"].iloc[0]
        self.note = ligne["note"].iloc[0]
        self.nb_tentatives = nb_tentatives

    def new_jeu(self):
        self.label_resultat.pack_forget()

        self.choix_mot()
        self.myst = mot_mystere(self.mot)

        self.deja_choisies, self.bonnes_lettres = "", set()
        self.taille_objectif = len(set(self.mot)) - (1 if "-" in self.mot else 0)

        self.afficher_etat()
        self.partie = True

    def afficher_etat(self):
        self.label_myst.configure(text=self.myst)
        self.label_lettres.configure(text="Lettre déjà choisis : "+self.deja_choisies)

        self.label_tentatives.configure(text=f"Tentatives : {self.nb_tentatives}")

    def ajout_lettre(self, event):
        if not self.partie:
            return None
        lettre = event.char

        if lettre == "}":
            print(self.mot)

        if not lettre_valide(lettre, self.deja_choisies):
            return None
        self.deja_choisies += lettre

        if verification(lettre, self.mot):
            self.myst = completer_mot(lettre, self.mot, self.myst)
            self.bonnes_lettres.add(lettre)
        else:
            self.nb_tentatives -= 1

        self.afficher_etat()
        self.test_resultat()
        return None

    def test_resultat(self):
        if self.nb_tentatives == 0:
            self.afficher_resultat(False)

        if len(self.bonnes_lettres) == self.taille_objectif:
            self.afficher_resultat(True)

    def afficher_resultat(self, victoire: bool):
        self.partie = False

        if victoire:
            resultat = "Bien joué ! Vous avez gagné ! 🎊"
            self.master.nouvelle_victoire(self.mot, self.note)

        else:
            resultat = "Loser... Le mot était : "+self.mot
        resultat += f"\n La note de votre mot était de : {self.note}/10"

        self.label_resultat.configure(text=resultat)
        self.label_resultat.pack(pady = (0,20), padx=20)

# ------------------
# ------------------

class Jeu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mot Mystere")
        self.resizable(height=False, width=False)

        self.frame_jeu = FrameJeu(self)
        self.frame_score = FrameScore(self)

        self.frame_pseudo = FramePseudo(self)
        self.frame_pseudo.pack()

        self.bind('<Key>', self.frame_jeu.ajout_lettre)
        self.protocol("WM_DELETE_WINDOW", self.fin_jeu)

    def ajout_pseudo(self, pseudo: str):
        self.frame_pseudo.pack_forget()
        FrameInfo(self, pseudo).grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.frame_jeu.grid(column=1, row=1, sticky="nsew")
        self.frame_score.grid(column=0, row=1, sticky="nsew")

        self.pseudo = pseudo

    def nouvelle_victoire(self, mot: str, note: float):
        self.frame_score.ajouter_score(self.pseudo, mot, note)

    def fin_jeu(self):
        if messagebox.askokcancel("Fermeture", "Voulez-vous sauvegarder vos statistiques ?"):
            self.frame_score.sauvegarder_statistiques()
        self.destroy()

    def afficher_graphe(self):
        afficher_repartition(data_mots)

if __name__ == '__main__':
    jeu = Jeu()
    jeu.mainloop()
