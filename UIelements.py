import customtkinter as ctk
from tkinter import PhotoImage
from main import VERSION
import tkinter
from webbrowser import open as open_url


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SMAPI Mod Manager")
        self.geometry("500x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW")

        self.icons = IconSheet('assets/iconsheet.png')
        self.iconphoto(True, self.icons.logo)

        # Banner image (top left)
        self.top_frame = Frame(self, width=500, height=200)
        self.top_frame.propagate(False)
        self.top_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.banner = PhotoImage(file="assets/background.png")
        self.banner_label = ctk.CTkLabel(self.top_frame, image=self.banner, width=400, height=200, anchor='nw')
        self.banner_label.pack(side="left", fill="x")

        # Control buttons (top right)
        self.control_frame = Frame(self.top_frame, width=100, height=200)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side="right", fill="y")
        self.add_prof_button = ctk.CTkButton(self.control_frame, text="+", text_font=("Arial", 18), width=50,)
        self.add_prof_tooltip = Tooltip(self.add_prof_button, "Add a new profile")
        self.add_prof_button.pack(pady=(10, 5), anchor=ctk.N)
        self.github_button = ctk.CTkButton(self.control_frame, text="\U0001F6C8", text_color='white', text_font=("Arial", 20),
                                           width=50, command=lambda: open_url("https://github.com/supercam19/SMAPI-Profile-Manager"), pady=0)
        self.github_tooltip = Tooltip(self.github_button, "Help (Open GitHub page)")
        self.github_button.pack(pady=5, anchor="n")
        self.version_label = ctk.CTkLabel(self.control_frame, text="Version: " + VERSION, width=100, height=20, text_font=("Arial", 7))
        self.version_label.pack(side="bottom", fill="x", pady=5)

        # Profiles list (bottom)
        self.canvas = ctk.CTkCanvas(self, bd=0)
        self.profiles_list = Frame(self, width=500, height=360)
        self.scrollbar = ctk.CTkScrollbar(self.profiles_list, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 200), window=self.profiles_list, anchor='nw')
        self.canvas.config(bd=0)
        self.canvas.config(bg="gray18")
        self.canvas.config(highlightthickness=0)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollbar.pack(side="right", fill="y")
        self.profiles_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))




class Frame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # define size of frame
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)


class Button(ctk.CTkButton):
    # define a custom button that changes colour on hover
    def __init__(self, parent, type='text', hover_image=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)
        self.configure(width=self.width, height=self.height)
        self.text = kwargs.get("text", None)
        self.configure(text=self.text)
        self.text_font = kwargs.get("text_font", ("Arial", 10))
        self.configure(text_font=self.text_font)
        self.text_color_default = kwargs.get("text_color", "white")
        self.configure(text_color=self.text_color_default)
        self.bg_color = kwargs.get("bg_color", "gray21")
        self.configure(bg=self.bg_color)
        self.fg_color = kwargs.get("fg_color", "gray21")
        self.configure(fg_color=self.fg_color)
        self.border_color = kwargs.get("border_color", "gray21")
        self.configure(highlightbackground=self.border_color)
        self.border_width = kwargs.get("border_width", 1)
        self.configure(highlightthickness=self.border_width)
        self.border_radius = kwargs.get("border_radius", 5)
        self.configure(relief="flat")
        self.configure(borderwidth=self.border_radius)
        self.command = kwargs.get("command", None)
        self.configure(command=self.command)
        self.image_default = kwargs.get("image", None)
        self.configure(image=self.image)
        self.padding = kwargs.get("padding", (0, 0))
        self.configure(padx=self.padding[0], pady=self.padding[1])
        self.cursor = kwargs.get("cursor", "arrow")
        self.configure(cursor=self.cursor)
        self.state = kwargs.get("state", "normal")
        self.configure(state=self.state)

        # Special properties
        self.type = type  # text, image
        self.hover_image = hover_image  # image to display on hover

        self.bind("<Enter>", self.on_enter, add="+")
        self.bind("<Leave>", self.leave, add="+")

    def on_enter(self, event=None):
        if self.type == 'text':
            self.configure(text_color="gray45")
        elif self.type == 'button':
            self.configure(image=self.hover_image)

    def leave(self, event=None):
        if self.type == 'text':
            self.configure(text_color=self.text_color_default)
        elif self.type == 'button':
            self.configure(image=self.image_default)


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
        """
        The background colour and the foreground colour need to be really similar because the label widget
        has un-removable anti-aliasing that makes the colors blend -> there will be different colour pixels
        on the edge of the label.
        """
        self.tw.wm_attributes('-transparentcolor', '#555555')
        self.tw.configure(bg="#555555")
        label = ctk.CTkLabel(self.tw, text=self.text, corner_radius=10, bg_color='#555555', fg_color='#545454')
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


class IconSheet:
    def __init__(self, path):
        self.path = path
        self.sheet = PhotoImage(file=self.path)
        self.logo = self.get_icon(0, 0, 63, 63)
        self.trash_closed = self.get_icon(64, 0, 63, 63).subsample(2, 2)
        self.trash_opened = self.get_icon(128, 0, 63, 63).subsample(2, 2)

    def get_icon(self, x, y, width, height):
        icon = PhotoImage()
        icon.tk.call(icon, 'copy', self.sheet, '-from', x, y, x + width, y + height, '-to', 0, 0)
        return icon


popup_info = PopupInfo()

