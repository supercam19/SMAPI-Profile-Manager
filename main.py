import os
from tkinter import filedialog, PhotoImage
import customtkinter as tk
from UIelements import *


class Profile:
    def __init__(self, name, path):
        self.name = name
        self.path = path.rstrip("\n")
        self.prof_frame = tk.CTkFrame(window.profiles_list, width=480, height=30)
        self.prof_frame.pack_propagate(False)
        self.prof_title = tk.CTkLabel(self.prof_frame, text=self.name, bg="gray", text_font=("Arial", 12))
        self.prof_button = tk.CTkButton(self.prof_frame, text="Launch", fg_color="lime", hover_color="green", width=40, text_color="black", command=self.select_profile)
        self.prof_delete = tk.CTkButton(self.prof_frame, text="Delete", fg_color="red", hover_color="darkred", width=40, command=self.delete_profile)

    def draw_profile(self):
        global profile_number
        profile_number += 1
        self.prof_frame.pack(pady=2)
        self.prof_title.pack(side=tk.LEFT, padx=2)
        self.prof_button.pack(side=tk.RIGHT, padx=10)
        self.prof_delete.pack(side=tk.RIGHT)

    def select_profile(self):
        os.chdir(self.path)
        os.chdir('..')
        # Find the name of the profile being disabled
        with open('C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/Mods/profile.txt', 'r') as f:
            prof_name = f.read()
        os.system(f'ren "Mods" "Mods_{prof_name}"')
        os.system(f'ren "Mods_{self.name.upper()}" "Mods"')

        os.system('START "" "StardewModdingAPI.exe"')

    def delete_profile(self):
        self.prof_frame.destroy()
        self.prof_title.destroy()
        self.prof_button.destroy()
        self.prof_delete.destroy()
        # Remove the profile from the text file
        with open('profiles.txt', 'r') as f:
            lines = f.readlines()
        with open('profiles.txt', 'w') as f:
            for line in lines:
                if not line.startswith(self.name):
                    f.write(line)


class Popup:
    def __init__(self, title, message):
        self.popup = tk.CTkToplevel(window)
        self.popup.title(title)
        self.popup.geometry("300x100")
        # self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", self.close_popup)
        self.popup_label = tk.CTkLabel(self.popup, text=message)
        self.popup_label.pack()
        self.popup_text = tk.CTkEntry(self.popup, width=200)
        self.popup_text.pack(pady=10)
        self.popup_button = tk.CTkButton(self.popup, text="OK", command=self.close_popup, width=10)
        self.popup_button.pack()

    def close_popup(self):
        global name_input
        name_input = self.popup_text.get()
        self.popup.destroy()


def add_profile():
    prof_path = filedialog.askdirectory()
    # Write the name of the profile to a text file to save for later
    popup = Popup("Name your profile", "Enter a name for your profile")
    # Wait for the popup to close
    window.wait_window(popup.popup)
    prof_name = name_input
    with open(f'{prof_path}\\profile.txt', 'w') as f:
        f.write(prof_name.upper())
    os.system(f'ren "{prof_path}" "Mods_{prof_name.upper()}"')
    profiles.append(Profile(prof_name, prof_path))
    profiles[-1].draw_profile()
    save_profile(prof_name, prof_path)


def save_profile(name, path):
    # Write the name and path of the profile to the profiles.txt file
    with open('profiles.txt', 'a') as f:
        f.write(f'{name};{path}\n')


def load_profiles():
    # Load the users profiles from the profiles.txt file
    with open('profiles.txt', 'r') as f:
        for line in f:
            prof_name, prof_path = line.split(';')
            profiles.append(Profile(prof_name, prof_path))
            profiles[-1].draw_profile()


profiles = []
profile_number = 0
name_input = ''
VERSION = "v1.0.0"

# Initialize the TK window
window = Window()
add_prof_button = tk.CTkButton(window.top_frame, text="+", text_font=("Arial", 18), width=50, command=add_profile).pack(padx=10, pady=10, side=tk.RIGHT, anchor=tk.N)

try:
    load_profiles()
except FileNotFoundError:
    pass

window.mainloop()

