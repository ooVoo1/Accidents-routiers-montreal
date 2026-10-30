import customtkinter as ctk
import tkinter as tk

from graphes.graph_maker import GraphMaker

class Graphique(ctk.CTkFrame):
    def __init__(self, master, handler, **kwargs):
        super().__init__(master, **kwargs)
        # DataHandler
        self.handler = handler

        # Créer la page du graphique.
        self.creer_page_graphiques()

    def creer_page_graphiques(self):
        # Création du graphique
        self.graph = GraphMaker(self, self.handler)
        self.graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        # Liste des statistiques disponibles
        options = ["Nombre de collisions", "Nombre de morts", "Nombre de blessés graves", "Nombre de blessés légers",
        "Nombre total de victimes", "Nombre de victimes piétons", "Nombre de victimes moto", "Nombre de victimes vélo"]

        # Variable pour le choix de la statistique
        self.selection = tk.StringVar(value=options[0])

        # Menu déroulant
        menuDeroulantGraphique = ctk.CTkOptionMenu(self, variable=self.selection, values=options, command=lambda choix: self.graph.update_graph(choix, self.texte_stats), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)

        # Label du menu déroulant
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self, text="Statistique à afficher", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

        # Encadré des statistiques
        self.stats_frame = ctk.CTkFrame(self, fg_color="white", border_width=1, border_color="#D9DEE5", corner_radius=12)
        self.stats_frame.place(relx=0.025, rely=0.32, anchor="nw", relwidth=0.20, relheight=0.27)

        # Titre de l'encadré
        self.titre_stats = ctk.CTkLabel(self.stats_frame, text="Résumé statistique", font=("Arial", 16, "bold"), text_color="black")
        self.titre_stats.pack(pady=(12, 8))

        # Texte des statistiques
        self.texte_stats = ctk.CTkLabel(self.stats_frame, text="Chargez un fichier CSV", font=("Arial", 13), text_color="black", justify="left", anchor="w")
        self.texte_stats.pack(fill="x", padx=12, pady=8)