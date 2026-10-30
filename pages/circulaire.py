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
        self.pie_graph = PieMaker(self, self.handler)
        self.pie_graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        options_annees = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        self.selection_annees = tk.StringVar(value = options_annees[0])

        menuDeroulantGraphique = ctk.CTkOptionMenu(self, variable=self.selection_annees, values=options_annees, command=self.pie_graph.update_pie, font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)

        TitreMenuDeroulantGraphique = ctk.CTkLabel(self, text="Année", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

