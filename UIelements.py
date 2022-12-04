import customtkinter as ctk
from tkinter import PhotoImage


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SMAPI Mod Manager")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))

        self.top_frame = Frame(self, width=500, height=200)
        self.top_frame.propagate(False)
        self.top_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.banner = PhotoImage(file="assets/background.png")
        self.banner_label = ctk.CTkLabel(self.top_frame, image=self.banner, width=400, height=200, anchor='nw')
        self.banner_label.pack(side="left", fill="x")

        self.control_frame = Frame(self.top_frame, width=100, height=200)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side="right", fill="y")

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


class Popup:
    def __init__(self, title, message, root, text_box=True):
        self.popup = ctk.CTkToplevel(root)
        self.popup.title(title)
        self.popup.geometry("300x100")
        # self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)
        self.popup_label = ctk.CTkLabel(self.popup, text=message)
        self.popup_label.pack()
        self.text_box = text_box
        if text_box:
            self.popup_text = ctk.CTkEntry(self.popup, width=200)
            self.popup_text.pack(pady=10)
        self.popup_button = ctk.CTkButton(self.popup, text="OK", command=self.close_popup, width=10)
        self.popup_button.pack()

    def close_popup(self):
        popup_info.change(self.popup_text.get())
        self.popup.destroy()


class PopupInfo:
    def __init__(self):
        self.info = 'Error'

    def __str__(self):
        return self.info

    def change(self, info):
        assert isinstance(info, str)
        self.info = info


popup_info = PopupInfo()