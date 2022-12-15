import customtkinter as ctk
from tkinter import PhotoImage
from main import VERSION
import tkinter


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SMAPI Mod Manager")
        self.geometry("500x400")
        self.resizable(False, False)
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.top_frame = Frame(self, width=500, height=200)
        self.top_frame.propagate(False)
        self.top_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.banner = PhotoImage(file="assets/background.png")
        self.banner_label = ctk.CTkLabel(self.top_frame, image=self.banner, width=400, height=200, anchor='nw')
        self.banner_label.pack(side="left", fill="x")

        self.control_frame = Frame(self.top_frame, width=100, height=200)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side="right", fill="y")
        self.version_label = ctk.CTkLabel(self.control_frame, text="Version: " + VERSION, width=100, height=20, text_font=("Arial", 7))
        self.version_label.pack(side="bottom", fill="x", pady=5)

        self.canvas = ctk.CTkCanvas(self, width=500)
        self.profiles_list = Frame(self, width=500, height=360)
        self.scrollbar = ctk.CTkScrollbar(self.profiles_list, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 200), window=self.profiles_list, anchor='nw')
        self.scrollbar.pack(side="right", fill="y")
        self.profiles_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def close_window(self):
        try:
            exit()
        except KeyboardInterrupt:
            exit()


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
        if self.text_box: popup_info.change(self.popup_text.get())
        self.popup.destroy()


class Tooltip:
    def __init__(self, widget, text):
        self.wait_time = 500  # milliseconds
        self.wrap_length = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.schedule, add="+")
        self.widget.bind("<Leave>", self.leave, add="+")
        self.widget.bind("<ButtonPress>", self.leave, add="+")
        self.id = None
        self.tw = None

    def leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self, event=None):
        # self.unschedule()
        self.id = self.widget.after(self.wait_time, self.show_tip)

    def unschedule(self):
        # Unschedule scheduled popups
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_pointerx() + 10
        y += self.widget.winfo_pointery() + 10
        self.tw = ctk.CTkToplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f'+{x}+{y}')
        label = ctk.CTkLabel(self.tw, text=self.text)
        label.pack(padx=1, pady=1)

    def hide_tip(self):
        self.unschedule()
        if self.tw: self.tw.withdraw()


class PopupInfo:
    def __init__(self):
        self.info = 'Error'

    def __str__(self):
        return self.info

    def change(self, info):
        assert isinstance(info, str)
        self.info = info


popup_info = PopupInfo()