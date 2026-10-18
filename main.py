import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.create_menu()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        menu.option_add("*Menu.font", "Arial 12")

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Sauvegarder", command=self.sauvegarder_donnees)
        file_menu.add_command(label="Charger", command=self.charger_donnees)
        
    def on_button_pressed(self):
        self.button.configure(text="Clicked!")

    def sauvegarder_donnees(self):
        chemin = filedialog.asksaveasfilename(title="Sauvegarder comme fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])

        if not chemin:
            return

        if not chemin.lower().endswith(".csv"):
            chemin += ".csv"

        try:
            self.df.to_csv(chemin, index=False)
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
    
    def charger_donnees(self):
        chemin = filedialog.askopenfilename(title="Ouvrir fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])
        if chemin:
            try:
                self.df = importer_csv(chemin)
                print("Données chargées!", self.df)
            except Exception as erreur:
                messagebox.showerror("Erreur", str(erreur))

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()