import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.ticker import AutoMinorLocator

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os

class DataHandler():
    """Fait la gestion des fichiers et du DataFrame."""

    def __init__(self):
        self.df = pd.DataFrame() # DataFrame initialement vide.
        self.chemin_courante = "" # Chemin courante du fichier
        self.df_resultats = pd.DataFrame() #Dataframe pour exportation des données
        self.graph_resultat = Figure()

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

    def sauvegarder_fichier(self, file_type, message):
        # Si le DataFrame de résultats est vide, afficher un erreur.
        if self.df_resultats.empty:
            messagebox.showwarning("Alerte", "Aucun donnée a été affiché")
            return

        # Ouvrir l'application de file explorer et demander à l'utilisateur d'écrire le nom du fichier.
        chemin = filedialog.asksaveasfilename(title=F"Sauvegarder comme fichier {file_type.upper()}", filetypes=[(f"Fichiers {file_type.upper()}", f"*.{file_type.lower()}")])

        # Si l'utilisateur annule le cours d'enregistrement, retourner rien.
        if not chemin:
            return 

        # Éviter d'écrire l'extension du ficher dans la zone de texte, faire sa automatiquement.
        if not chemin.lower().endswith(f".{file_type.lower()}"):
            chemin += f".{file_type.lower()}"

        # Joli message :)
        print(message)

        # Retourner le chemin du fichier.
        return chemin

    def sauvegarder_avec_gestion_erreur(self, save_function, file_type, message):
        # Gestion d'erreurs.
        try:
            # Acquerir le chemin par la fonction "sauvegarder_fichier"
            path = self.sauvegarder_fichier(file_type, message)

            # Si le programme a été arreté, retourner rien.
            if not path:
                return

            # Appeler la fonction de sauvegarde d'une classe ou quoi qui ce soit.
            save_function(path)
        except Exception as erreur:
            # Retourner un message d'erreur si quelque chose va mal.
            messagebox.showerror("Erreur", str(erreur))

    def sauvegarder_donnees(self):
        # Sauvegarder les donnees du dataframe dans un fichier csv.
        self.sauvegarder_avec_gestion_erreur(lambda path: self.df_resultats.to_csv(path, index=False), "csv", "Données enregistrées!")

    def sauvegarder_graphique(self):
        # Sauvegarder un image du graphique en ficher png.
        self.sauvegarder_avec_gestion_erreur(lambda path: self.graph_resultat.savefig(path), "png", "Graphique enregistrée!")

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

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accidents routiers Montreal")
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
        self.creer_page_graphique_circulaire()

        #Page accueil
        label = ctk.CTkLabel(self.page_accueil, text="C'est la Page d'Accueil")
        label.pack(pady=20)

        #Page aide
        titre_aide = ctk.CTkLabel(self.page_aide, text="Aide", font=("Arial", 28, "bold"))
        titre_aide.pack(pady=50)

        # Page graphique à barres
        titre_barres = ctk.CTkLabel(self.page_barres, text="Graphique à barres", font=("Arial", 28, "bold"))
        titre_barres.pack(pady=50)
        self.afficher_page(self.page_accueil)

    def creer_page_graphiques(self):
        # Création du graphique
        self.graph = GraphMaker(self.page_graphiques)
        self.graph.place(relx=0.6, rely=0.35, anchor="center", relwidth=0.75, relheight=0.7)

        # Variable pour le choix de la statistique
        self.selection = tk.StringVar(value="Nombre de collisions")

        # Liste des statistiques disponibles
        options = ["Nombre de collisions", "Nombre de morts", "Nombre de blessés graves", "Nombre de blessés légers",
        "Nombre total de victimes", "Nombre de victimes piétons", "Nombre de victimes moto", "Nombre de victimes vélo"]

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
        self.texte_stats = ctk.CTkLabel(self.stats_frame, text="Chargez un fichier CSV.", font=("Arial", 13), text_color="black", justify="left", anchor="w")
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

    def afficher_page(self, page):
        page.tkraise()

    def charger_et_actualiser(self):
        if self.handler.charger_csv():
            self.update_graph(self.selection.get())
            self.update_pie(self.selection_annees.get())

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
        self.handler.graph_resultat = self.graph.figure

    def update_pie(self,choix):
        if self.handler.df.empty:
            return

        annee = int(choix)

        df_annee = self.handler.df[self.handler.df['AN'] == annee]
        resultat = df_annee.groupby("GRAVITE").size()

        #df_perc = resultat.replace({x: round((100 * x) / sum(resultat.values), 1) for x in resultat.values})
        #self.handler.df_resultats = df_perc.reset_index(name=f"Pourcentage des valeurs en {annee}")

        row = list(resultat.index)
        columns = list(resultat.values)

        self.pie_graph.creat_graph(row,columns,annee)
        
    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
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
        graphiques_menu.add_command(label="Pie graph", command=lambda: self.afficher_page(self.page_pie))

        # Graphique à barres
        graphiques_menu.add_command(label="Graphique à barres", command=lambda: self.afficher_page(self.page_barres))

        
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()