import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def importer_csv(chemin):
    df = pd.read_csv(chemin)
    return df

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accidents routiers Montreal")
        self.config(bg="white")
        self.geometry("1240x768")
        self.df = importer_csv("collisions_routieres.csv")
        self.df_filtre = self.df.copy()
        self.df_resultats = pd.DataFrame()

        self.button = ctk.CTkButton(self, command=self.on_button_pressed, text="Click me!", bg_color="white")
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def on_button_pressed(self):
        self.button.configure(text="Clicked!")
    
    def charger_donnees(self):
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if chemin:
            try:
                self.df = importer_csv(chemin)
                print("Données chargées!")
            except Exception as erreur:
                messagebox.showerror("Erreur", str(erreur))
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()