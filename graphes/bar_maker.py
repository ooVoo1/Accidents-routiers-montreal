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

    def update_bar(self, choix, choix2, texte_stats):
        # Si le DataFrame est vide, retourner rien.
        if self.handler.df.empty:
            return
        
        annee = int(choix)

       #pour avoir la bonne année
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

        #pour ajouter une colonne de mois
        df_annee_bar['mois'] = pd.to_datetime(df_annee_bar["DT_ACCDN"], errors="coerce").dt.month
        data_dict = {}

        # si l'option tout
        if choix2 == "Tout":
            #créer un dataframe meilleur pour un graphique à barres
            for row, col in colonnes.items():
                if col in df_annee_bar.columns:
                    data_dict[row] = df_annee_bar.groupby('mois')[col].sum()

            
            accident_df = pd.DataFrame(data_dict)
            accident_df = accident_df.reindex(range(1, 13), fill_value=0)
            accident_df.index = noms_mois

            # Données destinées à l'exportation CSV
            self.handler.df_resultats = accident_df.reset_index(names=f"Mois de l'année {choix}")

            nb_mort = accident_df["Nombre de morts"].sum()
            nb_grave = accident_df["Nombre de blessés graves"].sum()
            nb_leger = accident_df["Nombre de blessés légers"].sum()
            nb_victime = accident_df[ "Nombre total de victimes"].sum()
            nb_pieton = accident_df["Nombre de victimes piétons"].sum()
            nb_moto = accident_df["Nombre de victimes moto"].sum()
            nb_velo = accident_df["Nombre de victimes vélo"].sum()
           
            
            texte = (f"Total d'accident léger: {int(nb_leger)}\n\n"
                        f"Total d'accidents grave: {int(nb_grave)}\n\n"
                        f"Total de morts: {int(nb_mort)}\n\n"
                        f"Total de victimes: {int(nb_victime)}\n\n"
                        f"Total de victimes piétonniaires: {int(nb_pieton)}\n\n"
                        f"Total de victimes à moto: {int(nb_moto)}\n\n"
                        f"Total de victimes à vélo: {int(nb_velo)}"
                        )
            
            texte_stats.configure(text=texte)

        else:
            #si il veut juste 1 type de victime au lieu de tout
            serie_resultat = df_annee_bar.groupby('mois')[colonnes[choix2]].sum()

            accident_df = pd.DataFrame({choix2: serie_resultat})
            accident_df = accident_df.reindex(range(1, 13), fill_value=0)
            accident_df.index = noms_mois

            # Données destinées à l'exportation CSV
            self.handler.df_resultats = accident_df.reset_index(names=f"Mois de l'année {choix}")

            total_accident = accident_df[choix2].sum()
            mois_record = accident_df[choix2].idxmax()

            texte = (f"Total d'accident: {int(total_accident)}\n\n"
                     f"Mois record: {str(mois_record)}"            
                    )
        
            texte_stats.configure(text=texte)

        self.create_graph(accident_df)
        self.handler.graph_resultat = self.figure
        