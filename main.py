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
        titre_aide = ctk.CTkLabel(self.page_aide, text="Aide", font=("Arial", 28, "bold"))
        titre_aide.pack(pady=50)

        self.afficher_page(self.page_accueil)

    def creer_accueil(self):
        #Mettre logo dans une variable pour la modifier
        image = Image.open("logo_routesure.png")
        largeur, hauteur = image.size
        #Recadrer l'image
        image = image.crop((0,int(hauteur * 0.22), largeur, int(hauteur * 0.78)))
        #Placer le logo dans l'app
        self.logo = ctk.CTkImage(light_image=image, dark_image=image, size=(610, 255))
        label_logo = ctk.CTkLabel(self.page_accueil, image=self.logo, text="")
        label_logo.pack(pady=(25, 5))
        #Création et placement du texte sous le logo
        description = ctk.CTkLabel(self.page_accueil, text="Explorez les données des collisions routières de Montréal", font=("Arial", 16), text_color="#64748B")
        description.pack(pady=(0, 20))
        #Création des emplacements des gros boutons pour les graphiques
        conteneur = ctk.CTkFrame(self.page_accueil, fg_color="transparent")
        conteneur.pack(fill="x", padx=60, pady=10)
        # Mettre les 3 boutons à la même taille
        for i in range(3):
            conteneur.grid_columnconfigure(i, weight=1)
        #Liste de tuple pour les textes des gros boutons
        pages = [("Évolution annuelle", "Visualiser l'évolution des collisions au fil des années.", self.page_graphiques),
        ("Graphique circulaire", "Analyser la répartition des collisions selon leur gravité.", self.page_pie),
        ("Graphique à barres", "Comparer différentes catégories de collisions.", self.page_barres)]
        #Mettre les logos des boutons dans une variable
        icones = ["icone_evolution.png","icone_circulaire.png","icone_barres.png"]
        #Pour garder les icones en mémoire
        self.icones_accueil = []
        # Créer les trois gros boutons
        for i, (titre, description, page) in enumerate(pages):
            #Création de l'objet
            gros_bouton = ctk.CTkFrame(conteneur, fg_color="#EDF5FF", corner_radius=12, height=220)
            #Mise en place
            gros_bouton.grid(row=0, column=i, padx=10, sticky="nsew")
            gros_bouton.grid_propagate(False)
            #Création et placement titre
            titre_gros_bouton = ctk.CTkLabel(gros_bouton, text=titre, font=("Arial", 18, "bold"), text_color="#133E70")
            titre_gros_bouton.pack(pady=(35, 8))
            #Pour que le contenu du bouton soit centré
            contenu = ctk.CTkFrame(gros_bouton, fg_color="transparent")
            contenu.pack(expand=True)
            #Loader l'image du bouton
            image = Image.open(icones[i])
            icone = ctk.CTkImage(light_image=image, dark_image=image, size=(44, 44))
            #Pour le garder en mémoire
            self.icones_accueil.append(icone)
            #Maintenant afficher et placer l'image du bouton
            image_gros_bouton = ctk.CTkLabel(contenu, image=icone, text="")
            image_gros_bouton.pack(pady=(0, 10))
            #Création et placement description du bouton
            texte_gros_bouton = ctk.CTkLabel(gros_bouton, text=description, font=("Arial", 13), text_color="#64748B", wraplength=280)
            texte_gros_bouton.pack(padx=15)
            #Création du bouton en tant que tel, car jusqu'ici nous n'avions qu'un simple encadré non interactif
            for widget in (gros_bouton, contenu, image_gros_bouton, titre_gros_bouton, texte_gros_bouton):
                widget.bind("<Button-1>", lambda event, p=page: self.afficher_page(p))
        #Création et placement du bouton pour charger les données
        bouton_charger = ctk.CTkButton(self.page_accueil, text="Charger des données CSV", command=self.charger_et_actualiser, font=("Arial", 15, "bold"), height=42,width=250)
        bouton_charger.pack(pady=(25, 8))
        bouton_aide = ctk.CTkButton(self.page_accueil, text="Aide", command=lambda: self.afficher_page(self.page_aide), fg_color="transparent", text_color="#1669B5", border_width=1, border_color="#1669B5", height=36, width=130)
        bouton_aide.pack(pady=5)


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