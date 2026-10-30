import customtkinter as ctk
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BarMaker(ctk.CTkFrame):
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

    def create_graph(self,pivot_df):
        #pour enlever l'ancien graphique
        self.ax.clear()

        #créer le graphe à bar
        pivot_df.plot(kind = 'bar', ax =self.ax, width = 0.8)
        self.ax.set_xlabel("Mois")
        self.ax.set_ylabel("Nombre total de victimes")
        self.ax.grid(axis='y', linestyle="--", alpha=0.7)
        self.ax.legend(loc='lower left', bbox_to_anchor=(0.5, -0.4), ncol= 2)

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def update_bar(self, choix, choix2):
        # Si le DataFrame est vide, retourner rien.
        if self.handler.df.empty:
            return
        
        annee = int(choix)

        df_annee_bar = self.handler.df[self.handler.df['AN'].astype(int) == annee]
        noms_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        colonnes = {
            "Nombre de morts": "NB_MORTS",
            "Nombre de blessés graves": "NB_BLESSES_GRAVES",
            "Nombre de blessés légers": "NB_BLESSES_LEGERS",
            "Nombre total de victimes": "NB_VICTIMES_TOTAL",
            "Nombre de victimes piétons": "NB_VICTIMES_PIETON",
            "Nombre de victimes moto": "NB_VICTIMES_MOTO",
            "Nombre de victimes vélo": "NB_VICTIMES_VELO"
        }

        df_annee_bar['mois'] = pd.to_datetime(df_annee_bar["DT_ACCDN"], errors="coerce").dt.month
        data_dict = {}

        if choix2 == "Tout":
            for row, col in colonnes.items():
                if col in df_annee_bar.columns:
                    data_dict[row] = df_annee_bar.groupby('mois')[col].sum()

            #Récupérer mois de chaque accident
            pivot_df = pd.DataFrame(data_dict)
            pivot_df = pivot_df.reindex(range(1, 13), fill_value=0)
            pivot_df.index = noms_mois

        else:
            serie_resultat = df_annee_bar.groupby('mois')[colonnes[choix2]].sum()
            pivot_df = pd.DataFrame({choix2: serie_resultat})
            pivot_df = pivot_df.reindex(range(1, 13), fill_value=0)
            pivot_df.index = noms_mois

        self.create_graph(pivot_df)
        