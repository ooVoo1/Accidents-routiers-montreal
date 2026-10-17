import customtkinter as ctk
import tkinter as tk

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accidetns routiers Montreal")
        self.config(bg="white")
        self.geometry("1240x768")

        self.button = ctk.CTkButton(self, command=self.on_button_pressed, text="Click me!", bg_color="white")
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def on_button_pressed(self):
        self.button.configure(text="Clicked!")

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MainApplication()
    app.mainloop()
