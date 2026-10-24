import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.ticker import AutoMinorLocator

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

import os

class DataHandler():
    """Fait la gestion des fichiers et du DataFrame."""

    def __init__(self):
        self.df = pd.DataFrame() # DataFrame initialement vide.
        self.chemin_courante = "" # Chemin courante du fichier
        self.df_resultats = pd.DataFrame() #Dataframe pour exportation des données


    def charger_csv(self):
        """Charger les données."""

        # Demander à l'utilisateur de choisir un fichier CSV.

        chemin = filedialog.askopenfilename(title="Charger fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

        # Si le cours de chargement n'est pas annulée, implementer les données du fichier CSV choisi dans le dataframe.
        # Assigner le chemin dans la variable 'chemin_courante'.
        # Lancer un erreur si quelque chose ne marche pas.

        if not chemin:
            return False

        try:
            self.df = pd.read_csv(chemin)
            self.chemin_courante = chemin
            print("Données chargées!")
            return True

        except Exception as erreur: 
            messagebox.showerror("Erreur", str(erreur))
            return False
    def sauvegarder_csv(self):
        """Sauvegarder les données."""

        # Vérifier si un fichier CSV à été chargé. Si oui, garder le nom du fichier courante, sinon on le laisse vide.

        fichier_courante = os.path.basename(self.chemin_courante) if os.path.exists(self.chemin_courante) else ""

        # Ouvrir l'application d'enregistrement pour sauvegarder le fichier.
        # Si un fichier à deja été chargée, sauvegarder avec le nom courant si l'utilisateur desire d'écraser le fichier actuel.
        # Il est possible de changer le nom du fichier à sauvegarder si l'utilisateur désire de créer un nouveau fichier .csv,
        # avec les données.

        chemin = filedialog.asksaveasfilename (
            title="Sauvegarder comme fichier CSV", 
            filetypes=[("Fichiers CSV", "*.csv")], 
            initialfile=fichier_courante
        )

        # Si l'opération d'enregistrement en cours est annulée, ne rien retourner.

        if not chemin:
            return

        # Pour éviter d'écrire le suffixe de l'extension de fichier dans la zone de texte. La fonction le fait automatiquement.

        if not chemin.lower().endswith(".csv"):
            chemin += ".csv"

        # Gestion d'erreur.
        # Si un erreur est déclenché, lancer un alerte. Sinon, enregistrer le fichier CSV.

        try:
            self.df.to_csv(chemin)
            print("Données sauvegardées!")
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))

class GraphMaker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))
        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)
        # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

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

class PieMaker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))
        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)
        # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def creat_graph(self,row, columns,titre):
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


class BarMaker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))
        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)
        # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    def creat_graph(self,pivot_df):
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


class BarMaker(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Création de la figure
        self.figure = Figure(figsize=(7, 4))
        # Création des axes du graphique
        self.ax = self.figure.add_subplot(111)
        # Intégration du graphique dans CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    def creat_graph(self,pivot_df):
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
        self.page_graphiques = ctk.CTkFrame(self, fg_color= "white")
        self.page_aide = ctk.CTkFrame(self, fg_color= "white")
        self.page_pie = ctk.CTkFrame(self, fg_color="white")
        self.page_barres = ctk.CTkFrame(self, fg_color="white")
        #Placer pages
        self.page_accueil.grid(row=0, column=0, sticky="nsew")
        self.page_graphiques.grid(row=0, column=0, sticky="nsew")
        self.page_aide.grid(row=0, column=0, sticky="nsew")
        self.page_pie.grid(row=0, column=0, sticky="nsew")
        self.page_barres.grid(row=0, column=0, sticky="nsew")
        #Création page graphique évolution annuelle
        self.creer_page_graphiques()
        #Création page graphique circulaire
        #Création page graphique circulaire
        self.creer_page_graphique_circulaire()
        #Création page graphique à barres
        self.creer_page_graphique_bar()
        #Création page accueil
        self.creer_accueil()
        #Page aide
        self.creer_page_aide()

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
        image = Image.open("logo_routesure.png")
        largeur, hauteur = image.size
        image = image.crop((0, int(hauteur * 0.22), largeur, int(hauteur * 0.78)))
        #Afficher et placer logo
        self.logo = ctk.CTkImage(light_image=image, dark_image=image, size=(610, 255))
        label_logo = ctk.CTkLabel(place_logo,image=self.logo,text="")
        label_logo.pack(expand=True)

        # Adapter la taille du logo à la fenêtre
        def adapter_logo(event):
            proportion = image.width / image.height
            largeur_logo = min(int(event.width * 0.8),960,int(event.height * 0.85 * proportion))
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
            icone = ctk.CTkImage(light_image=Image.open(icones[i]), size=(48, 48))
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
        self.icone_charger = ctk.CTkImage(light_image=Image.open("icone_charger.png"), size=(24, 24))

        # bouton charger CSV
        bouton_charger = ctk.CTkButton(ligne_boutons, text="Charger des données CSV", image=self.icone_charger, compound="left",
        command=self.charger_et_actualiser, font=("Arial", 15, "bold"), height=52, width=290, corner_radius=10)
        # placer le bouton
        bouton_charger.pack(side="left", padx=8)

        # image de "?" pour le bouton aide
        self.icone_aide = ctk.CTkImage(light_image=Image.open("icone_aide.png"), size=(22, 22))

        # bouton aide
        bouton_aide = ctk.CTkButton(ligne_boutons, text="Aide", image=self.icone_aide, compound="left", command=lambda: self.afficher_page(self.page_aide),
        fg_color="transparent", text_color="#1669B5", border_width=1, border_color="#CDD8E4", font=("Arial", 15), height=52, width=145, corner_radius=10)
        # placer le bouton
        bouton_aide.pack(side="left", padx=8)

    
    def creer_page_aide(self):

        # Pour que la page remplisse la fenetre
        self.page_aide.grid_rowconfigure(0, weight=1)
        self.page_aide.grid_columnconfigure(0, weight=1)

        # Zone défilable
        zone_aide = ctk.CTkScrollableFrame(self.page_aide, fg_color="white", corner_radius=0)
        zone_aide.grid(row=0, column=0, sticky="nsew")

        # Conteneur principal
        conteneur = ctk.CTkFrame(zone_aide, fg_color="transparent")
        conteneur.pack(fill="both", padx=60, pady=30)

        # Titre de la page
        titre = ctk.CTkLabel(conteneur, text="Page d'aide RouteSûre", font=("Arial", 30, "bold"), text_color="#133E70")
        titre.pack(pady=(0, 12))
        #texte d'accueil
        introduction = ctk.CTkLabel(conteneur, text="Découvrez comment importer, visualiser et analyser les données des collisions routières de Montréal.", font=("Arial", 15), text_color="#64748B", wraplength=850)
        introduction.pack(pady=(0, 25))

        # Garder les images en mémoire
        self.images_aide = []

        # Fonction pour créer une section de la page
        def ajouter_section(titre, texte, capture=None):
            #Créer section
            section = ctk.CTkFrame(conteneur, fg_color="#EDF5FF", corner_radius=12)
            section.pack(fill="x", pady=10)
            #titre de la section
            titre_section = ctk.CTkLabel(section, text=titre, font=("Arial", 19, "bold"), text_color="#133E70", anchor="w")
            titre_section.pack(fill="x", padx=25, pady=(18, 8))
            #Ajouter texte d'explication
            texte_section = ctk.CTkLabel(section, text=texte, font=("Arial", 15), text_color="#475569", justify="left", anchor="w", wraplength=900)
            texte_section.pack(fill="x", padx=25, pady=(0, 18))

            # Ajouter un screenshot pour aider plus =)
            if capture and os.path.exists(capture):
                image = Image.open(capture)
                largeur = min(image.width, 750)
                hauteur = int(largeur * image.height / image.width)

                image_aide = ctk.CTkImage(light_image=image, dark_image=image, size=(largeur, hauteur))

                self.images_aide.append(image_aide)

                label_image = ctk.CTkLabel(section, image=image_aide, text="")
                label_image.pack(pady=(0, 20))

        # Ajout des sections
        ajouter_section("1. Charger des données CSV", "Depuis la page d'accueil, cliquez sur « Charger des données CSV ».\n\n"
        "Une fenêtre s'ouvrira pour vous permettre de sélectionner un fichier CSV contenant les données des collisions routières.\n\n"
        "Une fois le fichier chargé, les graphiques disponibles seront automatiquement actualisés.",
        "captures/chargement.png")

        ajouter_section("2. Naviguer dans l'application", "Depuis l'accueil, cliquez sur l'une des trois grandes cartes pour accéder au graphique souhaité.\n\n"
        "Vous pouvez également utiliser le menu « Graphiques » dans la barre supérieure pour changer de page et le bouton « Accueil » pour revenir au menu principal.",
        "captures/navigation.png")

        ajouter_section("3. Graphique d'évolution annuelle", "Ce graphique permet de visualiser l'évolution des collisions et des victimes au fil des années.\n\n"
        "Utilisez le menu « Statistique à afficher » pour sélectionner le nombre de collisions, de morts, de blessés ou d'autres catégories de victimes.\n\n"
        "Le graphique et le résumé statistique s'actualiseront selon votre sélection.",
        "captures/evolution.png")

        ajouter_section("4. Graphique circulaire", "Le graphique circulaire permet d'observer la répartition des collisions selon leur gravité.\n\n"
        "Sélectionnez une année dans le menu déroulant. Chaque portion représente une catégorie de gravité, exprimée en pourcentage.",
        "captures/circulaire.png")

        ajouter_section("5. Exporter les données en CSV", "L'objectif de cette fonctionnalité est de permettre l'enregistrement des données représentées dans le graphique.\n\n"
        "Lorsque l'exportation des résultats sera implémentée, vous pourrez utiliser le menu « Fichier », sélectionner l'option de sauvegarde, puis choisir le nom et l'emplacement du fichier CSV.",
        "captures/export_csv.png")

        ajouter_section("6. Enregistrer un graphique en PNG", "Une fonctionnalité d'exportation permettra de sauvegarder le graphique affiché sous forme d'image PNG.\n\n"
        "Vous pourrez ainsi réutiliser les graphiques dans des présentations, des rapports ou d'autres documents. Cette fonctionnalité reste à implémenter.",
        "captures/export_png.png")


    def creer_page_graphiques(self):

        # Création du graphique
        self.graph = GraphMaker(self.page_graphiques)

        self.graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)


        # Liste des statistiques disponibles
        options = ["Nombre de collisions", "Nombre de morts", "Nombre de blessés graves", "Nombre de blessés légers",
        "Nombre total de victimes", "Nombre de victimes piétons", "Nombre de victimes moto", "Nombre de victimes vélo"]
        # Variable pour le choix de la statistique
        self.selection = tk.StringVar(value=options[0])

        # Menu déroulant
        menuDeroulantGraphique = ctk.CTkOptionMenu(self.page_graphiques, variable=self.selection, values=options, command=self.update_graph, font=("Arial", 13), corner_radius=8, height=36)

        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)

        # Label du menu déroulant
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self.page_graphiques, text="Statistique à afficher", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")

        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

        # Encadré des statistiques
        self.stats_frame = ctk.CTkFrame(self.page_graphiques, fg_color="white", border_width=1, border_color="#D9DEE5", corner_radius=12)

        self.stats_frame.place(relx=0.025, rely=0.32, anchor="nw", relwidth=0.20, relheight=0.27)

        # Titre de l'encadré
        self.titre_stats = ctk.CTkLabel(self.stats_frame, text="Résumé statistique", font=("Arial", 16, "bold"), text_color="black")

        self.titre_stats.pack(pady=(12, 8))

        # Texte des statistiques
        self.texte_stats = ctk.CTkLabel(self.stats_frame, text="Chargez un fichier CSV", font=("Arial", 13), text_color="black", justify="left", anchor="w")

        self.texte_stats.pack(fill="x", padx=12, pady=8)

    def creer_page_graphique_circulaire(self):
        self.pie_graph = PieMaker(self.page_pie)
        self.pie_graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)
        
        options_annees = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        self.selection_annees = tk.StringVar(value = options_annees[0])

        menuDeroulantGraphique = ctk.CTkOptionMenu(self.page_pie, variable=self.selection_annees, values=options_annees, command=self.update_pie, font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self.page_pie, text="Année", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

    def creer_page_graphique_bar(self):
        self.barres_graphe = BarMaker(self.page_barres)
        self.barres_graphe.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        options_annees = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        options_type = ["Tout","Nombre de morts", "Nombre de blessés graves", "Nombre de blessés légers",
                "Nombre total de victimes", "Nombre de victimes piétons", "Nombre de victimes moto", "Nombre de victimes vélo"]

        self.selection_annees_bar = tk.StringVar(value = options_annees[0])
        self.selection_type = tk.StringVar(value= options_type[0])

        
        menuDeroulantGraphique = ctk.CTkOptionMenu(self.page_barres, variable=self.selection_annees_bar, values=options_annees, command=lambda val:self.update_bar(self.selection_annees_bar.get(), self.selection_type.get()), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.09, anchor="nw", relwidth=0.2)
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self.page_barres, text="Année", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.05, anchor="center")

        menuDeroulantGraphique = ctk.CTkOptionMenu(self.page_barres, variable=self.selection_type, values=options_type, command=lambda val:self.update_bar(self.selection_annees_bar.get(), self.selection_type.get()), font=("Arial", 13), corner_radius=8, height=36)
        menuDeroulantGraphique.place(relx=0.025, rely=0.25, anchor="nw", relwidth=0.2)
        TitreMenuDeroulantGraphique = ctk.CTkLabel(self.page_barres, text="Type de victime", font=("Arial", 16, "bold"), text_color="black", fg_color="transparent")
        TitreMenuDeroulantGraphique.place(relx=0.125, rely=0.21, anchor="center")

        


    def afficher_page(self, page):
        page.tkraise()
        if page == self.page_accueil:
            self.config(menu="")
        else:
            self.config(menu=self.menu_principal)


    def charger_et_actualiser(self):
        if self.handler.charger_csv():
            self.update_graph(self.selection.get())
            self.update_pie(self.selection_annees.get())
            self.update_bar(self.selection_annees_bar.get(),self.selection_type.get())

    

    def update_graph(self, choix):
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
        self.graph.create_graph(x=resultats.index, y=resultats.values, titre=choix + " par année", label_y=choix)
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
        self.texte_stats.configure(text=texte)

    def update_pie(self,choix):
        if self.handler.df.empty:
            return
        annee = int(choix)
        df_annee = self.handler.df[ self.handler.df['AN'] == annee]
        resultat = df_annee.groupby("GRAVITE").size()
        row = list(resultat.index)
        columns = list(resultat.values)
        self.pie_graph.creat_graph(row,columns,annee)

    def update_bar(self,choix,choix2):
        if self.handler.df.empty:
            return
        annee = int(choix)
        df_annee_bar = self.handler.df[ self.handler.df['AN'].astype(int) == annee]
        noms_mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        colonnes = {"Nombre de morts": "NB_MORTS","Nombre de blessés graves": "NB_BLESSES_GRAVES","Nombre de blessés légers": "NB_BLESSES_LEGERS","Nombre total de victimes": "NB_VICTIMES_TOTAL","Nombre de victimes piétons": "NB_VICTIMES_PIETON","Nombre de victimes moto": "NB_VICTIMES_MOTO","Nombre de victimes vélo": "NB_VICTIMES_VELO"
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

        self.barres_graphe.creat_graph(pivot_df)



        
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
        file_menu.add_command(label="Sauvegarder", command=self.handler.sauvegarder_csv)
        file_menu.add_command(label="Charger", command=self.charger_et_actualiser)

        #Menu graphiques
        graphiques_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Graphiques", menu=graphiques_menu)

        # Évolution annuelle
        graphiques_menu.add_command(label="Évolution annuelle", command=lambda: self.afficher_page(self.page_graphiques))

        # Pie graph
        graphiques_menu.add_command(label="Pie graph", command=lambda: self.afficher_page(self.page_pie))

        # Graphique à barres
        graphiques_menu.add_command(label="Graphique à barres", command=lambda: self.afficher_page(self.page_barres))

        
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()