import pandas as pd

from tkinter import filedialog, messagebox
from matplotlib.figure import Figure

class DataHandler():
    """Fait la gestion des fichiers et du DataFrame."""

    def __init__(self):
        self.df = pd.DataFrame() # DataFrame initialement vide.
        self.df_resultats = pd.DataFrame() # Dataframe pour l'exportation des données
        self.graph_resultat = Figure() # Graphique pour l'exportation des données

    def charger_csv(self):
        """Charger les données."""

        # Demander à l'utilisateur de choisir un fichier CSV.
        chemin = filedialog.askopenfilename(title="Charger fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

        # Si le cours d'enregistrement est annulé, retoruner rien (ou dans ce cas, False, car on vérifie si le fichier à été chargé).
        if not chemin:
            return False

        # Gestion d'erreurs pour les fichiers qu'on charge.
        try:
            # Lire le fichier .csv avec la fonction de pandas qui permet de faire ça.
            # Cela doit automatiquement créer un dataframe avec les données du fichier csv.
            self.df = pd.read_csv(chemin)

            print("Données chargées!")
            return True

        except Exception as erreur: 
            messagebox.showerror("Erreur", str(erreur))
            return False

    def sauvegarder_fichier(self, file_type):
        """Sauvegarder des fichiers."""
        
        # Si le DataFrame de résultats est vide, afficher un erreur.
        if self.df_resultats.empty:
            messagebox.showwarning("Alerte", "Aucune donnée à exporter.")
            return

        # Extension du fichier en lowercase.
        extension = file_type.lower()

        # Ouvrir l'application de file explorer et demander à l'utilisateur d'écrire le nom du fichier.
        chemin = filedialog.asksaveasfilename(
            title=F"Sauvegarder comme fichier {file_type.upper()}", 
            filetypes=[
                (f"Fichiers {file_type.upper()}", f"*.{extension}")
            ],
            defaultextension=extension
        )

        # Si l'utilisateur annule le cours d'enregistrement, retourner rien.
        if not chemin:
            return 

        # Retourner le chemin du fichier.
        return chemin

    def sauvegarder_avec_gestion_erreur(self, save_function, file_type, message):
        """Sauvegarder des fichiers avec la gestion des erreurs."""
        # Gestion d'erreurs.
        try:
            # Acquerir le chemin par la fonction "sauvegarder_fichier"
            path = self.sauvegarder_fichier(file_type)

            # Si le programme a été arreté, retourner rien.
            if not path:
                return

            # Appeler la fonction de sauvegarde d'une classe ou quoi qui ce soit.
            save_function(path)

            # Joli message :)
            print(message)
        except Exception as erreur:
            # Retourner un message d'erreur si quelque chose va mal.
            messagebox.showerror("Erreur", str(erreur))

    def sauvegarder_donnees(self):
        """Sauvegarder des données en fichiers .csv."""

        # Sauvegarder les donnees du dataframe dans un fichier csv.
        self.sauvegarder_avec_gestion_erreur(lambda path: self.df_resultats.to_csv(path, index=False), "csv", "Données enregistrées!")

    def sauvegarder_graphique(self):
        """Sauvegarder un graphique en fichier .png."""

        # Sauvegarder un image du graphique en ficher png.
        self.sauvegarder_avec_gestion_erreur(lambda path: self.graph_resultat.savefig(path), "png", "Graphique enregistrée!")
