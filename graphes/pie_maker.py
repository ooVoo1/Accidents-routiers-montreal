import customtkinter as ctk
from tkinter import messagebox
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


        #pour l'affichage du cercle pour qu'il reste un cercle
        self.ax.axis('equal')

        self.figure.tight_layout()
        self.canvas.draw_idle()

    def update_pie(self, choix, texte_stats):
        # Si le DataFrame est vide, retourner rien.
        if self.handler.df.empty:
            return

        # Choix d'année. 
        annee = int(choix)

        df_annee = self.handler.df[self.handler.df['AN'] == annee]
        resultat = df_annee.groupby("GRAVITE").size()
          #Ne pas faire de graphique si il n'y a pas d'accidents dans l'année
        if resultat.empty or resultat.sum() == 0:
            messagebox.showwarning("Aucune donnée", "Aucune collision enregistrée pour cette année.")
            return
        #df_perc = resultat.replace({x: round((100 * x) / sum(resultat.values), 1) for x in resultat.values})
        #self.handler.df_resultats = df_perc.reset_index(name=f"Pourcentage des valeurs en {annee}")

        row = list(resultat.index)
        columns = list(resultat.values)

        total = resultat.sum()
        total_dommage_inferieur = resultat["Dommages matériels inférieurs au seuil de rapportage"].sum()
        total_materiel = resultat["Dommages matériels seulement"].sum()
        total_leger = resultat["Léger"].sum()
        total_grave = resultat["Grave"].sum()
        total_mortel = resultat["Mortel"].sum()

        texte = (f"Total de cette année: {int(total)}\n\n"
                       f"Total de dommage matériels inférieurs au seuil de rapportage: {int(total_dommage_inferieur)}\n\n"
                       f"Total de dommage matériels seulement: {int(total_materiel)}\n\n"
                       f"Total d'accident léger: {int(total_leger)}\n\n"
                       f"Total d'accident grave: {int(total_grave)}\n\n"
                       f"Total d'accident mortel: {int(total_mortel)}\n\n"
                       )
        texte_stats.configure(text=texte)

        self.create_graph(row, columns, annee)