import customtkinter as ctk
import os

from PIL import Image

class Aide(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Pour que la page remplisse la fenetre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Créer la page d'aide.
        self.creer_page_aide()

    def creer_page_aide(self):
        # Zone défilable
        zone_aide = ctk.CTkScrollableFrame(self, fg_color="white", corner_radius=0)
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
        def ajouter_section(titre, texte, captures=None):
            #Créer section
            section = ctk.CTkFrame(conteneur, fg_color="#EDF5FF", corner_radius=12)
            section.pack(fill="x", pady=10)

            #titre de la section
            titre_section = ctk.CTkLabel(section, text=titre, font=("Arial", 19, "bold"), text_color="#133E70", anchor="w")
            titre_section.pack(fill="x", padx=25, pady=(18, 8))

            #Ajouter texte d'explication
            texte_section = ctk.CTkLabel(section, text=texte, font=("Arial", 15), text_color="#475569", justify="left", anchor="w", wraplength=900)
            texte_section.pack(fill="x", padx=25, pady=(0, 18))

            # Ajouter des screenshots pour aider plus =)
            if captures:
                for capture in captures:
                    if os.path.exists("images/" + capture):
                        image = Image.open("images/" + capture)

                        # Mettre à la bonne taille
                        largeur = min(image.width, 750)
                        hauteur = int(largeur * image.height / image.width)
                        image_aide = ctk.CTkImage(light_image=image, dark_image=image, size=(largeur, hauteur))
                        self.images_aide.append(image_aide)

                        # Afficher l'image dans la section
                        label_image = ctk.CTkLabel(section, image=image_aide, text="")
                        label_image.pack(pady=(5, 20), padx=20)

        # Ajout des sections
        ajouter_section("1. Charger des données CSV", "Depuis la page d'accueil, cliquez sur « Charger des données CSV ».\n\n"
        "Une fenêtre s'ouvrira pour vous permettre de sélectionner un fichier CSV contenant les données des collisions routières.\n\n"
        "Une fois le fichier chargé, les graphiques disponibles seront automatiquement actualisés.",
        ["chargement1.png", "chargement2.png"])

        ajouter_section("2. Naviguer dans l'application", "Depuis l'accueil, cliquez sur l'une des trois grandes cartes pour accéder au graphique souhaité.\n\n"
        "Vous pouvez également utiliser le menu « Graphiques » dans la barre supérieure pour changer de page et le bouton « Accueil » pour revenir au menu principal.",
        ["navigation1.png","navigation2.png"])

        ajouter_section("3. Graphique d'évolution annuelle", "Ce graphique permet de visualiser l'évolution des collisions et des victimes au fil des années.\n\n"
        "Utilisez le menu « Statistique à afficher » pour sélectionner le nombre de collisions, de morts, de blessés ou d'autres catégories de victimes.\n\n"
        "Le graphique et le résumé statistique s'actualiseront selon votre sélection.",
        ["evolution.png"])

        ajouter_section("4. Graphique circulaire", "Le graphique circulaire permet d'observer la répartition des collisions selon leur gravité.\n\n"
        "Sélectionnez une année dans le menu déroulant. Chaque portion représente une catégorie de gravité, exprimée en pourcentage.",
        ["circulaire.png"])

        ajouter_section("5. Graphique à barres", "Le graphique à barres permet d'observer la répartition d'un certain type de victime à travers les mois d'une année.\n\n"
        "Sélectionnez une année et un type de victime dans les menu déroulant. Chaque barre représente le nombre de victime dans un mois de l'année sélectionnée.",
        ["barres.png"])

        ajouter_section("6. Exporter les données en CSV", "L'objectif de cette fonctionnalité est de permettre l'enregistrement des données représentées dans le graphique.\n\n"
        "Vous pouvez utiliser le menu « Fichier », sélectionner l'option Sauvegarder Données, puis choisir le nom et l'emplacement du fichier CSV.",
        ["export_csv1.png","export_csv2.png"])

        ajouter_section("7. Enregistrer un graphique en PNG", "Une fonctionnalité d'exportation permet de sauvegarder le graphique affiché sous forme d'image PNG.\n\n"
        "Vous pourrez ainsi réutiliser le graphique dans des présentations, des rapports ou d'autres documents. Sélectionner l'option Sauvegarder Graphique, puis choisir le nom et l'emplacement du fichier PNG.",
        ["export_png1.png", "export_png2.png"])