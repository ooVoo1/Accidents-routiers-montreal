import customtkinter as ctk
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphMaker(ctk.CTkFrame):
    def __init__(self, master, handler):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))

        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)

        # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # DataHandler
        self.handler = handler

    def create_graph(self, x, y, titre, label_y):
        # Effacer ancien graphique
        self.ax.clear()

        # Tracer la nouvelle courbe
        self.ax.plot(x, y, marker="o")

        # Personnaliser
        self.ax.set_xticks(x)
        self.ax.set_title(titre)
        self.ax.set_xlabel("Année")
        self.ax.set_ylabel(label_y)

        # Ajouter quadrillage mineur
        self.ax.xaxis.set_minor_locator(AutoMinorLocator(5))
        self.ax.yaxis.set_minor_locator(AutoMinorLocator(5))

        # Quadrillage majeur
        self.ax.grid(which="major", linestyle="-", linewidth=0.8, alpha=0.5)

        # Quadrillage mineur
        self.ax.grid(which="minor", linestyle=":", linewidth=0.5, alpha=0.5)     

        # Ajuster espacement
        self.figure.tight_layout()

        # Refaire graphique
        self.canvas.draw_idle()

    def update_graph(self, choix, texte_stats):
        #Si les données ne sont pas chargées, arrêter l'éxecution
        if self.handler.df.empty:
            return

        print(f"L'utilisateur a cliqué sur : {choix}")

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

        self.create_graph(x=resultats.index, y=resultats.values, titre=choix + " par année", label_y=choix)

        #Récupération de données pour statsbox
        total = resultats.sum()
        annee_record = resultats.idxmax()
        maximum = resultats.max()
        noms_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        #Récupérer mois de chaque accident
        mois = pd.to_datetime(self.handler.df["DT_ACCDN"], errors="coerce").dt.month

        #Classer les accidents par leur mois
        if choix == "Nombre de collisions":
            resultats_mois = self.handler.df.groupby(mois).size()
        else:
            resultats_mois = self.handler.df.groupby(mois)[colonne].sum()

        #Assigner meilleur mois
        numero_mois = int(resultats_mois.idxmax())
        mois_record = noms_mois[numero_mois - 1]

        #Créer texte pour statsbox
        texte = (f"Total : {int(total)}\n\n"
        f"Année record : {int(annee_record)}\n\n"
        f"Maximum annuel : {int(maximum)}\n\n"
        f"Mois record : {mois_record}")

        texte_stats.configure(text=texte)
        self.handler.graph_resultat = self.figure