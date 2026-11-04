import customtkinter as ctk
import tkinter as tk

from graphes.pie_maker import PieMaker

class Circulaire(ctk.CTkFrame):
    def __init__(self, master, handler, **kwargs):
        super().__init__(master, **kwargs)
        # DataHandler
        self.handler = handler

        # Créer page du graphique circulaire.
        self.creer_page_graphique_circulaire()

    def creer_page_graphique_circulaire(self):
        # Ajouter le graphique circulaire (pie).
        self.pie_graph = PieMaker(self, self.handler)
        self.pie_graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        # Options disponibles pour le menu dropdown.
        options_annees = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        self.selection_annees = tk.StringVar(value = options_annees[0])
        
        # Créer bouton dropdown.
        menuDeroulantGraphique = ctk.CTkOptionMenu(self, variable=self.selection_annees, values=options_annees, command=lambda var:self.pie_graph.update_pie(self.selection_annees.get(),self.texte_stats), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)

        # Titre du graphique.
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self, text="Année", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

        # Encadré des statistiques
        self.stats_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="#D9DEE5", corner_radius=12)
        self.stats_frame.place(relx=0.025, rely=0.5, anchor="nw", relwidth=0.3, relheight=0.35)

        # Titre de l'encadré
        self.titre_stats = ctk.CTkLabel(self.stats_frame, text="Résumé statistique", font=("Arial", 20, "bold"), text_color="black")
        self.titre_stats.pack(pady=(12, 8))

        # Texte pour les statistiques
        self.texte_stats = ctk.CTkLabel(self.stats_frame, text="Chargez un fichier CSV", font=("Arial", 18), text_color="black", justify="left", anchor="w")
        self.texte_stats.pack(fill="x", padx=12, pady=8)

