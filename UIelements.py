import customtkinter as ctk
from tkinter import PhotoImage


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SMAPI Mod Manager")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconphoto(True, PhotoImage(file="smapi.png"))

        self.top_frame = Frame(self, width=500, height=200)
        self.top_frame.propagate(False)
        self.top_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.banner = PhotoImage(file="background.png")
        self.banner_label = ctk.CTkLabel(self.top_frame, image=self.banner, width=400, height=200, anchor='nw')
        self.banner_label.pack(side="left", fill="x")
        # self.display_banner = ctk.CTkCanvas(self.top_frame, width=400, height=200, bg="white")
        # self.display_banner.create_image(0, 0, image=self.banner, anchor="nw")
        # self.display_banner.pack(side="left", fill=ctk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(self, width=500)
        self.profiles_list = Frame(self, width=500, height=360)
        self.scrollbar = ctk.CTkScrollbar(self.profiles_list, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 200), window=self.profiles_list, anchor='nw')
        self.scrollbar.pack(side="right", fill="y")
        self.profiles_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class Frame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # define size of frame
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)
