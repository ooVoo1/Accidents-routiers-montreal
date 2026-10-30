import customtkinter as ctk
import tkinter as tk

from graphes.bar_maker import BarMaker

class Barres(ctk.CTkFrame):
    def __init__(self, master, handler, **kwargs):
        super().__init__(master, **kwargs)
        # DataHandler
        self.handler = handler

        # Créer la page du graphique de barrres.
        self.creer_page_graphique_bar()

    def creer_page_graphique_bar(self):
        self.barres_graphe = BarMaker(self, self.handler)
        self.barres_graphe.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        options_annees = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        options_type = ["Tout","Nombre de morts", "Nombre de blessés graves", "Nombre de blessés légers",
                "Nombre total de victimes", "Nombre de victimes piétons", "Nombre de victimes moto", "Nombre de victimes vélo"]

        self.selection_annees_bar = tk.StringVar(value = options_annees[0])
        self.selection_type = tk.StringVar(value= options_type[0])

        menuDeroulantGraphique = ctk.CTkOptionMenu(self, variable=self.selection_annees_bar, values=options_annees, command=lambda val:self.barres_graphe.update_bar(self.selection_annees_bar.get(), self.selection_type.get()), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)

        TitreMenuDeroulantGraphique = ctk.CTkLabel(self, text="Année", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

        menuDeroulantGraphique2 = ctk.CTkOptionMenu(self, variable=self.selection_type, values=options_type, command=lambda val:self.barres_graphe.update_bar(self.selection_annees_bar.get(), self.selection_type.get()), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique2.place(relx=0.025, rely=0.25, anchor="nw", relwidth=0.2)

        TitreMenuDeroulantGraphique2 = ctk.CTkLabel(self, text="Type de victime", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique2.place(relx=0.125, rely=0.21, anchor="center")