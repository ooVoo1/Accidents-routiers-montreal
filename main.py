import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os

"""
def importer_csv(chemin):
    df = pd.read_csv(chemin)
    return df
"""

class DataHandler():
    """Fait la gestion des fichiers et du DataFrame."""

    def __init__(self):
        self.df = pd.DataFrame() # DataFrame initialement vide.
        self.chemin_courante = "" # Chemin courante du fichier

    def charger_csv(self):
        """Charger les données."""

        # Demander l'utilisateur à choisir un fichier CSV.

        chemin = filedialog.askopenfilename(title="Charger fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

        # Si le cours de chargement n'est pas annulée, implementer les données du fichier CSV choisi dans le dataframe.
        # Assigner le chemin dans la variable 'chemin_courante'.
        # Lancer un erreur si quelque chose ne marche pas.

        if chemin:
            try:
                self.df = pd.read_csv(chemin)
                self.chemin_courante = chemin

                print("Données chargées!")
            except Exception as erreur: 
                messagebox.showerror("Erreur", str(erreur))

    def sauvegarder_csv(self):
        """Sauvegarder les données."""

        # Vérifier si un fichier CSV à été chargé. Si oui, garder le nom du fichier courante, sinon on le laisse vide.

        fichier_courante = os.path.basename(self.chemin_courante) if os.path.exists(self.chemin_courante) else ""

        # Ouvrir l'application d'enregistrement pour sauvegarder le fichier.
        # Si un fichier à deja été chargée, sauvegarder avec le nom courant si l'utilisateur desire d'écraser le fichier actuel.
        # Il est possible de changer le nom du fichier à sauvegarder si l'utilisateur désire de créer un nouveau fichier .csv,
        # avec les données.

        chemin = filedialog.asksaveasfilename (
            title="Sauvegarder comme fichier CSV", 
            filetypes=[("Fichiers CSV", "*.csv")], 
            initialfile=fichier_courante
        )

        # Si l'opération d'enregistrement en cours est annulée, ne rien retourner.

        if not chemin:
            return

        # Pour éviter d'écrire le suffixe de l'extension de fichier dans la zone de texte. La fonction le fait automatiquement.

        if not chemin.lower().endswith(".csv"):
            chemin += ".csv"

        # Gestion d'erreur.
        # Si un erreur est déclenché, lancer un alerte. Sinon, enregistrer le fichier CSV.

        try:
            self.df.to_csv(chemin)
            print("Données sauvegardées!")
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))

class GraphMaker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))
        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)
         # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_graph(self, x, y, titre, label_y):
        # Effacer l'ancien graphique
        self.ax.clear()
        # Tracer la nouvelle courbe
        self.ax.plot(x, y, marker="o")
        # Personnaliser
        self.ax.set_title(titre)
        self.ax.set_xlabel("Année")
        self.ax.set_ylabel(label_y)
        self.ax.grid(True)
        # Ajuster l'espacement
        self.figure.tight_layout()
        # Actualiser le graphique
        self.canvas.draw_idle()

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accidents routiers Montreal")
        self.config(bg="white")
        self.geometry("1240x768")
        self.handler = DataHandler()
        self.graph = GraphMaker(self)
        self.graph.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.6)

        """
        self.df = pd.read_csv("collisions_routieres.csv")
        self.df_filtre = self.df.copy()
        self.df_resultats = pd.DataFrame()
        """
        self.create_menu()
    def update_graph(self, choix):
        #Si les données ne sont pas chargées, arrêter l'éxecution
        if self.handler.df.empty:
            return
        #Dico d'équivalence pour les noms de colonnes du DataFrame
        colonnes = {"Nombre de morts": "NB_MORTS","Nombre de blessés graves": "NB_BLESSES_GRAVES",
        "Nombre de blessés légers": "NB_BLESSES_LEGERS","Nombre total de victimes": "NB_VICTIMES_TOTAL",
        "Nombre de victimes piétons": "NB_VICTIMES_PIETON","Nombre de victimes moto": "NB_VICTIMES_MOTO",
        "Nombre de victimes vélo": "NB_VICTIMES_VELO"}

        # Créer serie avec les données souhaitée pour le graphique
        if choix == "Nombre de collisions":
            resultats = self.handler.df.groupby("AN").size()
        else:
            colonne = colonnes[choix]
            resultats = self.handler.df.groupby("AN")[colonne].sum()

        # Garder les résultats pour en cas d'exportation
        self.handler.df_resultats = resultats.reset_index(name=choix)
        self.graph.create_graph(x=resultats.index, y=resultats.values, titre=choix + " par année", label_y=choix)
        
    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        menu.option_add("*Menu.font", "Arial 12")

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Sauvegarder", command=self.handler.sauvegarder_csv)
        file_menu.add_command(label="Charger", command=self.handler.charger_csv)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()