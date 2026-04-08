import customtkinter as ctk
import pandas as pd

class ScrollScore(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, border_width=5, **kwargs)

        self.label_scores = []

    def supprimer_labels(self):
        for label in self.label_scores:
            label.destroy()
        self.label_scores = []

    def afficher_scores(self, liste_scores):
        self.supprimer_labels()

        for pseudo, note, mot  in liste_scores:
            texte = f"{pseudo} - {note}/10\n{mot}"

            label_score = ctk.CTkLabel(self, text=texte, font=("Courier", 15, "bold"))
            label_score.pack(pady=(10,0))
            self.label_scores.append(label_score)

def ouvrir_statistiques():
    data_stats = pd.read_csv("data\\statistiques.csv")

    pseudos = list(data_stats["Pseudonyme"])
    notes = list(data_stats["Note"])
    mots = list(data_stats["Mot"])

    dico_scores = dict()
    for i in range(len(pseudos)):
        dico_scores[pseudos[i]] = (notes[i], mots[i])
    return dico_scores


class FrameScore(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.scroll_score = ScrollScore(self,label_text="Affichage des scores :", label_font=("Courier", 15, "bold"))
        self.scroll_score.grid(column=0, row=0, sticky="nsew")
        self.dico_scores = ouvrir_statistiques()

        self.scroll_score.afficher_scores(self.dico_to_list())

    def dico_to_list(self):
        liste_score = []

        for pseudo in self.dico_scores:
            note, mot = self.dico_scores[pseudo]

            liste_score.append((pseudo, note, mot))

        liste_score = sorted(liste_score, key=lambda triplet: triplet[1], reverse=True)
        return liste_score

    def ajouter_score(self, pseudo: str, mot: str, note: float):
        if pseudo in self.dico_scores:
            note_avant = self.dico_scores[pseudo][0]

            if note_avant < note:
                self.dico_scores[pseudo] = (note, mot)
                self.scroll_score.afficher_scores(self.dico_to_list())
        else:
            self.dico_scores[pseudo] = (note, mot)
            self.scroll_score.afficher_scores(self.dico_to_list())

    def sauvegarder_statistiques(self):
        dico_data = {"Pseudonyme": [], "Note": [], "Mot": []}

        for pseudo in self.dico_scores:
            dico_data["Pseudonyme"].append(pseudo)

            note, mot = self.dico_scores[pseudo]
            dico_data["Note"].append(note)
            dico_data["Mot"].append(mot)

        data_stats = pd.DataFrame(data=dico_data)
        data_stats.to_csv("data\\statistiques.csv", index=False)

# ------------------
# ------------------

class FramePseudo(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.btn_pseudo = ctk.CTkButton(self, text="Choisir un pseudo", command=self.fn_pseudo)
        self.btn_pseudo.pack(padx=40, pady=(20,0))

        self.input_pseudo = ctk.CTkEntry(self)
        self.input_pseudo.pack(pady=(0,20))

    def fn_pseudo(self):
        pseudo = self.input_pseudo.get()

        if pseudo == "" or " " in pseudo or len(pseudo) > 11:
            return None

        self.master.ajout_pseudo(pseudo)

# ------------------
# ------------------

class FrameInfo(ctk.CTkFrame):
    def __init__(self, master, pseudo,  **kwargs):
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text="MOT MYSTERE", font=("Courier", 30, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(self, text="by Mattéo", font=("Courier", 15, "italic", "bold")).grid(row=1, column=1)

        self.btn_graphe = ctk.CTkButton(self, text="Répartition des notes", command=self.master.afficher_graphe, font=("Courier", 15, "bold"))
        self.btn_graphe.grid(row=0, column=0, padx=20)

        ctk.CTkLabel(self, text="Session : " + pseudo, font=("Courier", 20, "bold")).grid(row=1, column=0)

if __name__ == '__main__':
    ouvrir_statistiques()