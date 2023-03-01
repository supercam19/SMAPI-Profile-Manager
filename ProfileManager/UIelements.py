"""
@author: supercam19
@github: https://github.com/supercam19
@license: MIT
@description: Manages the user interface of the program
"""

import customtkinter as ctk
from tkinter import PhotoImage
from main import VERSION
from webbrowser import open as open_url
from SuperWidgets.SuperWidgets import Frame
from SuperWidgets.Tooltip import Tooltip


class Window(ctk.CTk):
    def __init__(self, settings, sort_callback=None):
        super().__init__()
        self.sort_callback = sort_callback
        self.title("SMAPI Mod Manager")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW")

        # Calculate how to place the window in the center of screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry('500x400+%d+%d' % (x, y + 30))

        self.icons = IconSheet('assets/iconsheet.png')
        self.iconphoto(True, self.icons.logo)

        # Banner image (top left)
        self.top_frame = Frame(self, width=500, height=200)
        self.top_frame.propagate(False)
        self.top_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.banner = PhotoImage(file="assets/background.png")
        self.banner_label = ctk.CTkLabel(self.top_frame, image=self.banner, width=400, height=200, anchor='nw')
        self.banner_label.pack(side="left")

        # Control buttons (top right)
        self.control_frame = Frame(self.top_frame, width=100, height=200)
        self.control_frame.pack_propagate(False)
        self.control_frame.pack(side="right", fill="y")
        self.add_prof_button = ctk.CTkButton(self.control_frame, text="+", text_font=("Arial", 18), width=50,)
        self.add_prof_tooltip = Tooltip(self.add_prof_button, "Add a new profile")
        self.add_prof_button.pack(pady=(10, 5), anchor=ctk.N)
        self.undo_button = ctk.CTkButton(self.control_frame, text="\U000021A9", text_font=("Arial", 18), width=50, state="disabled")
        self.undo_tooltip = Tooltip(self.undo_button, "Revert last change to profiles")
        self.undo_button.pack(pady=5, anchor=ctk.N)
        self.github_button = ctk.CTkButton(self.control_frame, text="\U0001F6C8", text_color='white', text_font=("Arial", 20),
                                           width=50, command=lambda: open_url("https://github.com/supercam19/SMAPI-Profile-Manager"), pady=0)
        self.github_tooltip = Tooltip(self.github_button, "Help (Open GitHub page)")
        self.github_button.pack(pady=5, anchor="n")
        self.version_label = ctk.CTkLabel(self.control_frame, text="Version: " + VERSION,
                                          width=100, height=20, text_font=("Arial", 7))
        self.version_label.pack(side="bottom", fill="x", pady=5)
        self.control_frame.lift()

        # Sorting bar
        self.sorting_frame = Frame(self, width=500, height=30)
        self.sorting_frame.propagate(False)
        self.sorting_frame.pack(fill="both", expand=True, side="top", anchor="w")
        self.sorting_label = ctk.CTkLabel(self.sorting_frame, text="Sort:", height=20, text_font=("Arial", 12), anchor="e")
        self.sorting_label.pack(side="left", anchor="w", padx=(30, 15), pady=5)
        self.sorting_dropdown = ctk.CTkOptionMenu(self.sorting_frame, width=100, height=20, text_font=("Arial", 12),
                                                  values=["Name", "Last Played", "Created"], command=self.sort_callback)
        self.sorting_dropdown.pack(side="left", anchor="w", pady=5)
        self.sorting_dropdown.set(settings['sort']) if 'sort' in settings else self.sorting_dropdown.set("Name")
        self.invert_sort_checkbox = ctk.CTkCheckBox(self.sorting_frame, text="Invert", width=20, height=20,
                                                    text_font=("Arial", 12), command=self.sort_callback)
        self.invert_sort_checkbox.pack(side="left", anchor="w", padx=15, pady=5)
        if 'invert' in settings:
            self.invert_sort_checkbox.select() if settings['invert'] else self.invert_sort_checkbox.deselect()

        # Profiles list (bottom)
        self.canvas = ctk.CTkCanvas(self, bd=0, width=0, height=0)
        self.canvas.configure(height=240)
        self.profiles_list = Frame(self, width=500)
        self.profiles_list.bind_all("<MouseWheel>", self._on_mousewheel)
        self.profiles_list.lower()
        self.scrollbar = ctk.CTkScrollbar(self.profiles_list, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 200), window=self.profiles_list, anchor='nw')
        self.canvas.config(bg="gray18")
        self.canvas.config(highlightthickness=0)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.scrollbar.pack(side="right", fill="y")
        self.profiles_list.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        mouse_y = self.winfo_pointery() - self.winfo_rooty()
        if mouse_y > 360:
            self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def update_bar(self, new_ver, dont_show_callback):
        self.msg_frame = Frame(self, fg_color='blue', bg_color='blue')
        self.msg_frame.pack(side='bottom', fill='x')
        msg = ctk.CTkLabel(self.msg_frame, text=f'New version available: {new_ver}', text_font=('Arial', 8))
        msg.pack(side='left', padx=(2, 0))

        # Link to download the newest release
        download_button = ctk.CTkButton(self.msg_frame, text='| Download', command=lambda: open_url('https://github.com/supercam19/SMAPI-Profile-Manager/releases/latest'),
                                        fg_color='blue', text_font=('Arial', 8), hover_color='#0000DD', width=1)
        download_button.pack(side='left')
        download_button.bind('<Enter>', lambda e: download_button.configure(text_font=('Arial', 8, 'underline')))
        download_button.bind('<Leave>', lambda e: download_button.configure(text_font=('Arial', 8)))

        # Don't show new version message again
        dont_show_button = ctk.CTkButton(self.msg_frame, text='| Don\'t show again', command=lambda: self.dont_show_update_bar_again(dont_show_callback),
                                         fg_color='blue', text_font=('Arial', 8), hover_color='#0000DD', width=1)
        dont_show_button.pack(side='left')
        dont_show_button.bind('<Enter>', lambda e: dont_show_button.configure(text_font=('Arial', 8, 'underline')))
        dont_show_button.bind('<Leave>', lambda e: dont_show_button.configure(text_font=('Arial', 8)))

        hide_button = ctk.CTkButton(self.msg_frame, text='x', command=self.hide_update_bar, fg_color='blue', text_font=('Arial', 12), hover_color='#0000DD', width=1)
        hide_button.pack(side='right', padx=5)

    def dont_show_update_bar_again(self, callback):
        self.hide_update_bar()
        callback()

    def hide_update_bar(self):
        self.msg_frame.pack_forget()


class Popup:
    # Popup window, can have textbox, or just a message
    def __init__(self, title, message, root, text_box=True, callback=None):
        self.popup = ctk.CTkToplevel(root)
        self.popup.title(title)
        self.popup.geometry("+%d+%d" % (root.winfo_x() + 100, root.winfo_y() + 100))
        self.popup.minsize(300, 100)
        self.popup.focus()
        # self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", self.destruct)
        self.popup_label = ctk.CTkLabel(self.popup, text=message)
        self.popup_label.pack(side="top", pady=10)
        self.text_box = text_box
        self.callback = callback
        if text_box:
            self.popup_text = ctk.CTkEntry(self.popup, width=200)
            self.popup_text.after(100, self.popup_text.focus)
            self.popup_text.pack(pady=10)
        self.button_frame = Frame(self.popup, fg_color='gray14', width=self.popup.winfo_width())
        self.button_frame.pack(side="bottom", pady=10)
        # self.button_frame.pack_propagate(False)
        self.popup_button = ctk.CTkButton(self.button_frame, text="OK", command=self.close_popup, width=10)
        self.popup_button.pack(side="right", padx=10)

        self.progress_frame = Frame(self.popup, fg_color='gray14', height=30, width=300)
        self.drive_letter = ctk.CTkLabel(self.progress_frame, text="")
        self.drive_letter.pack(side="left", padx=2)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, orient=ctk.HORIZONTAL, width=200, mode='determinate')
        self.progress_bar.pack(side="left", padx=2)
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="")
        self.progress_label.pack(side="left", padx=2)
        self.popup.bind("<Return>", self.close_popup)

    def close_popup(self, event=None):
        # Save text box value to the popup_info object
        if self.text_box: self.callback({"name": self.popup_text.get()})
        self.popup.destroy()

    def destruct(self):
        # If the popup is closed, set the popup_info object to None
        if self.callback: self.callback({"name": None})
        self.popup.destroy()

    def add_button(self, text, command, **kwargs):
        button = ctk.CTkButton(self.button_frame, text=text, command=command, width=10, **kwargs)
        button.pack(side="right", padx=10)


class IconSheet:
    # All icons imported from the assets/iconsheet.png file
    def __init__(self, path):
        self.path = path
        self.sheet = PhotoImage(file=self.path)
        self.logo = self.get_icon(0, 0, 63, 63)
        self.trash_closed = self.get_icon(64, 0, 63, 63).subsample(2, 2)
        self.trash_opened = self.get_icon(128, 0, 63, 63).subsample(2, 2)
        self.gear = self.get_icon(192, 0, 63, 63).subsample(2, 2)
        self.gear_dark = self.get_icon(0, 64, 63, 63).subsample(2, 2)

    def get_icon(self, x, y, width, height):
        # Each icon is 64x64, so create a PhotoImage of only those pixels for each icon
        icon = PhotoImage()
        icon.tk.call(icon, 'copy', self.sheet, '-from', x, y, x + width, y + height, '-to', 0, 0)
        return icon