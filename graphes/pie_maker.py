import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PieMaker(ctk.CTkFrame):
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

    def create_graph(self, row, columns, titre):
        #pour enlever l'ancien graphique
        self.ax.clear()

        #créer le graphe circulaire et faire afficher les valeurs sous forme de pourcentage
        self.ax.pie(columns,  autopct='%1.1f%%', startangle=90)

        #le nom du graphique
        self.ax.set_title(f"Gravité des accidents en {titre}", fontdict={"fontsize": 14, "weight": "bold"})

        #afficher les categories sous forme de  legende
        self.ax.legend(row,title = "Catégories", loc ="lower right", bbox_to_anchor=(1.05, 0.03), fontsize=10)

        #,bbox_to_anchor=(1, 0, 0.5, 1)

        #pour l'affichage du cercle pour qu'il reste un cercle
        self.ax.axis('equal')

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def update_pie(self, choix):
        # Si le DataFrame est vide, retourner rien.
        if self.handler.df.empty:
            return

        # Choix d'année. 
        annee = int(choix)

        df_annee = self.handler.df[self.handler.df['AN'] == annee]
        resultat = df_annee.groupby("GRAVITE").size()

        #df_perc = resultat.replace({x: round((100 * x) / sum(resultat.values), 1) for x in resultat.values})
        #self.handler.df_resultats = df_perc.reset_index(name=f"Pourcentage des valeurs en {annee}")

        row = list(resultat.index)
        columns = list(resultat.values)

        self.create_graph(row, columns, annee)