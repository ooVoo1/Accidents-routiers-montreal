from tkinter import CENTER
from turtle import position
import customtkinter as ctk

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accidetns routiers Montreal")
        self.geometry("1240x768")

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()
print("Salut")