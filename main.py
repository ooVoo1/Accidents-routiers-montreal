import customtkinter as ctk
import tkinter as tk

from PIL import Image

from datahandler import DataHandler

from pages.aide import Aide
from pages.circulaire import Circulaire
from pages.graphique import Graphique
from pages.barres import Barres

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RouteSûre")
        self.configure(fg_color="white")
        self.geometry("1240x768")
        self.handler = DataHandler()

        #Créer le menu
        self.create_menu()

        #Pour que les pages remplissent bien la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Créer pages
        self.page_accueil = ctk.CTkFrame(self, fg_color= "white")
        self.page_aide = Aide(self, fg_color="white")
        self.page_graphiques = Graphique(self, self.handler, fg_color="white")
        self.page_pie = Circulaire(self, self.handler, fg_color="white")
        self.page_barres = Barres(self, self.handler, fg_color="white")

        #Placer pages
        self.page_accueil.grid(row=0, column=0, sticky="nsew")
        self.page_graphiques.grid(row=0, column=0, sticky="nsew")
        self.page_aide.grid(row=0, column=0, sticky="nsew")
        self.page_pie.grid(row=0, column=0, sticky="nsew")
        self.page_barres.grid(row=0, column=0, sticky="nsew")

        #Création page accueil
        self.creer_accueil()
        self.afficher_page(self.page_accueil)

    def creer_accueil(self):
        # Pour que l'accueil s'adapte à la fenêtre
        self.page_accueil.grid_columnconfigure(0, weight=1)
        self.page_accueil.grid_rowconfigure(0, weight=4)
        self.page_accueil.grid_rowconfigure(2, weight=3)
        self.page_accueil.grid_rowconfigure(3, weight=1)

        # Place pour le logo RouteSure
        place_logo = ctk.CTkFrame(self.page_accueil,fg_color="transparent")
        place_logo.grid(row=0, column=0, sticky="nsew")

        # Loader et recadrer le logo
        image = Image.open("images/logo_routesure.png")
        largeur, hauteur = image.size
        image = image.crop((0, int(hauteur * 0.22), largeur, int(hauteur * 0.78)))

        #Afficher et placer logo
        self.logo = ctk.CTkImage(light_image=image, dark_image=image, size=(610, 255))
        label_logo = ctk.CTkLabel(place_logo,image=self.logo,text="")
        label_logo.pack(expand=True)

        # Adapter la taille du logo à la fenêtre
        def adapter_logo(event):
            proportion = image.width / image.height
            largeur_logo = min(
                int(event.width * 0.8), 
                960, 
                int(event.height * 0.85 * proportion)
            )
            if largeur_logo > 0:
                hauteur_logo = int(largeur_logo / proportion)
                self.logo.configure(size=(largeur_logo, hauteur_logo))

        place_logo.bind("<Configure>", adapter_logo)

        # Description de l'app en dessous du logo
        description = ctk.CTkLabel(self.page_accueil, text="Explorez les données des collisions routières de Montréal", font=("Arial", 16), text_color="#64748B")
        description.grid(row=1, column=0, pady=10)

        # Emplacements des gros boutons
        conteneur = ctk.CTkFrame(self.page_accueil, fg_color="transparent")
        conteneur.grid(row=2, column=0, sticky="nsew", padx=50, pady=10)
        conteneur.grid_rowconfigure(0, weight=1)

        for i in range(3):
            conteneur.grid_columnconfigure(i, weight=1, uniform="cartes")

        #Liste de tuples avec le contenu des boutons
        pages = [("Évolution annuelle", "Visualiser l'évolution des collisions au fil des années.", self.page_graphiques),
        ("Graphique circulaire", "Analyser la répartition des collisions selon leur gravité.", self.page_pie),
        ("Graphique à barres", "Comparer différentes catégories de collisions.", self.page_barres)]

        #Mettre les icones des 3 gros boutons dans une variable
        icones = ["icone_evolution.png", "icone_circulaire.png", "icone_barres.png"]

        #Pour garder les icones en mémoire
        self.icones_accueil = []

        # Création des trois gros boutons
        for i, (titre, description, page) in enumerate(pages):
            #Création et placement de l'objet
            gros_bouton = ctk.CTkFrame(conteneur, fg_color="#EDF5FF", corner_radius=12)
            gros_bouton.grid(row=0, column=i, padx=10, sticky="nsew")

            # Centrer le contenu dans le bouton
            contenu = ctk.CTkFrame(gros_bouton, fg_color="transparent")
            contenu.pack(expand=True)

            #Mettre icone du bouton
            icone = ctk.CTkImage(light_image=Image.open("images/" + icones[i]), size=(48, 48))
            self.icones_accueil.append(icone)
            image_gros_bouton = ctk.CTkLabel(contenu, image=icone, text="")
            image_gros_bouton.pack(pady=(0, 12))

            # Titre du bouton
            titre_gros_bouton = ctk.CTkLabel(contenu, text=titre, font=("Arial", 19, "bold"), text_color="#133E70")
            titre_gros_bouton.pack(pady=(0, 10))

            # Description du graphique associé au bouton
            texte_gros_bouton = ctk.CTkLabel(contenu, text=description, font=("Arial", 14), text_color="#64748B", wraplength=260)
            texte_gros_bouton.pack(padx=15)

            # Rendre bouton clickable (parceque pour l'instant ce n'était qu'un carré avec du texte et une image)
            for widget in (gros_bouton, contenu, image_gros_bouton, titre_gros_bouton, texte_gros_bouton):
                widget.bind("<Button-1>", lambda event, p=page: self.afficher_page(p))

        # place des boutons aide et charger (AC)
        place_boutons_AC = ctk.CTkFrame(self.page_accueil,fg_color="transparent")
        place_boutons_AC.grid(row=3, column=0, sticky="nsew")

        # Pour que les boutons aide et charger soient alignés
        ligne_boutons = ctk.CTkFrame(place_boutons_AC, fg_color="transparent")
        ligne_boutons.pack(expand=True)

        # image de fichier pour bouton charger
        self.icone_charger = ctk.CTkImage(light_image=Image.open("images/icone_charger.png"), size=(24, 24))

        # bouton charger CSV
        bouton_charger = ctk.CTkButton(ligne_boutons, text="Charger des données CSV", image=self.icone_charger, compound="left",
        command=self.charger_et_actualiser, font=("Arial", 15, "bold"), height=52, width=290, corner_radius=10)
        # placer le bouton
        bouton_charger.pack(side="left", padx=8)

        # image de "?" pour le bouton aide
        self.icone_aide = ctk.CTkImage(light_image=Image.open("images/icone_aide.png"), size=(22, 22))

        # bouton aide
        bouton_aide = ctk.CTkButton(ligne_boutons, text="Aide", image=self.icone_aide, compound="left", command=lambda: self.afficher_page(self.page_aide),
        fg_color="transparent", text_color="#1669B5", border_width=1, border_color="#CDD8E4", font=("Arial", 15), height=52, width=145, corner_radius=10)

        # placer le bouton
        bouton_aide.pack(side="left", padx=8)

    def afficher_page(self, page):
        pages = (
            self.page_accueil,
            self.page_graphiques,
            self.page_aide,
            self.page_pie,
            self.page_barres
        )

        # Masquer les pages inactives
        for p in pages:
            if p == page:
                p.grid()
            else:
                p.grid_remove()

        # Afficher la page sélectionnée
        page.tkraise()

        if page == self.page_accueil:
            self.config(menu="")
        else:
            self.config(menu=self.menu_principal)
            
    def charger_et_actualiser(self):
        if self.handler.charger_csv():
            self.page_graphiques.graph.update_graph(self.page_graphiques.selection.get(), self.page_graphiques.texte_stats)
            self.page_pie.pie_graph.update_pie(self.page_pie.selection_annees.get())
            self.page_barres.barres_graphe.update_bar(self.page_barres.selection_annees_bar.get(),self.page_barres.selection_type.get())
        
    def create_menu(self):
        self.menu_principal = tk.Menu(self)
        menu = self.menu_principal
        menu.option_add("*Menu.font", "Arial 12")

        #Accueil
        menu.add_command(label="Accueil", command=lambda: self.afficher_page(self.page_accueil))

        #Aide
        menu.add_command(label="Aide", command=lambda: self.afficher_page(self.page_aide))

        #File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Sauvegarder Données", command=self.handler.sauvegarder_donnees)
        file_menu.add_command(label="Sauvegarder Graphique", command=self.handler.sauvegarder_graphique)
        file_menu.add_command(label="Charger", command=self.charger_et_actualiser)

        #Menu graphiques
        graphiques_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Graphiques", menu=graphiques_menu)

        # Évolution annuelle
        graphiques_menu.add_command(label="Évolution annuelle", command=lambda: self.afficher_page(self.page_graphiques))

        # Pie graph
        graphiques_menu.add_command(label="Graphique circulaire", command=lambda: self.afficher_page(self.page_pie))

        # Graphique à barres
        graphiques_menu.add_command(label="Graphique à barres", command=lambda: self.afficher_page(self.page_barres))

        
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()