import pandas as pd

from tkinter import filedialog, messagebox

import os
import sys

class DataHandler():
    """Fait la gestion des fichiers et du DataFrame."""

    def __init__(self):
        self.df = pd.DataFrame() # DataFrame initialement vide.
        self.df_resultats = pd.DataFrame() # Dataframe pour l'exportation des données
        self.graph_resultat = None # Graphique pour l'exportation des données

    def charger_csv(self):
        """Charger les données."""

        # Demander à l'utilisateur de choisir un fichier CSV.
        chemin = filedialog.askopenfilename(title="Charger fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

        # Si le cours d'enregistrement est annulé, retoruner rien (ou dans ce cas, False, car on vérifie si le fichier à été chargé).
        if not chemin:
            return False

        # Gestion d'erreurs pour les fichiers qu'on charge.
        try:
            df_temporaire = pd.read_csv(chemin)

            # Vérifier si le fichier est vide
            if df_temporaire.empty:
                raise ValueError("Le fichier CSV est vide.")

            # Liste des colonnes nécessaires au fonctionnement de l'application
            colonnes_obligatoires = ["AN", "DT_ACCDN", "GRAVITE", "NB_MORTS", "NB_BLESSES_GRAVES", "NB_BLESSES_LEGERS", 
            "NB_VICTIMES_TOTAL", "NB_VICTIMES_PIETON", "NB_VICTIMES_MOTO", "NB_VICTIMES_VELO"]

            # Trouver les colonnes manquantes
            colonnes_manquantes = []

            for colonne in colonnes_obligatoires:
                if colonne not in df_temporaire.columns:
                    colonnes_manquantes.append(colonne)

            # Refuser le fichier s'il manque des colonnes
            if colonnes_manquantes:
                raise ValueError("Le fichier CSV ne contient pas toutes les colonnes requises.\n\n"
                "Colonnes manquantes :\n"+ "\n".join(colonnes_manquantes))

            # Accepter le fichier seulement après avoir checké si on as toutes les colonnes
            self.df = df_temporaire
            self.chemin_courante = chemin

            # Réinitialiser les anciens résultats
            self.df_resultats = pd.DataFrame()

            print("Données chargées!")
            return True

        except Exception as erreur:
            messagebox.showerror("Erreur de chargement",str(erreur))
            return False

    def sauvegarder_fichier(self, file_type):
        """Sauvegarder des fichiers."""

        if file_type == "csv" and self.df_resultats.empty:
            messagebox.showwarning("Alerte", "Aucune donnée à exporter.")
            return

        if file_type == "png" and self.graph_resultat is None:
            messagebox.showwarning("Alerte", "Aucun graphique à exporter.")
            return

        # Extension du fichier en lowercase.
        extension = file_type.lower()

        # Ouvrir l'application de file explorer et demander à l'utilisateur d'écrire le nom du fichier.
        chemin = filedialog.asksaveasfilename(
            title=F"Sauvegarder comme fichier {file_type.upper()}", 
            filetypes=[
                (f"Fichiers {file_type.upper()}", f"*.{extension}")
            ],
            defaultextension=f".{extension}"
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

    def resource_path(self, relative_path):
        try:
            # Dossier temporaire créé par PyInstaller
            base_path = sys._MEIPASS
        except AttributeError:
            # Exécution normale du script Python
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
