import os
from tkinter import filedialog, PhotoImage
import customtkinter as tk
from UIelements import *
import requests
import json


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
        warning_label.pack_forget()

    def select_profile(self):
        os.chdir(os.path.dirname(settings['smapi_path']))
        # Find the name of the profile being disabled
        try:
            with open('Mods/profile.txt', 'r') as f:
                prof_name = f.read()
            os.system(f'ren "Mods" "Mods_{prof_name}"')
        except FileNotFoundError:
            pass

        os.system(f'ren "Mods_{self.name.upper()}" "Mods"')

        os.system(f'START "" "{settings["smapi_path"]}"')

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


def add_profile():
    prof_path = filedialog.askdirectory()
    # Write the name of the profile to a text file to save for later
    popup = Popup("Name your profile", "Enter a name for your profile", window)
    # Wait for the popup to close
    window.wait_window(popup.popup)
    prof_name = str(popup_info)
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


def load_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_settings():
    with open('settings.json', 'w') as f:
        json.dump(settings, f)


def check_files():
    # Check if critical files are missing, if so, download/create them
    if not os.path.exists('profiles.txt'):
        with open('profiles.txt', 'w') as f:
            f.write('')
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            f.write('{}')
    if not os.path.exists('assets'):
        os.mkdir('assets')
    if not os.path.exists('assets/background.png'):
        background_img = requests.get('https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/assets/background.png?raw=true')
        with open('assets/background.png', 'wb') as f:
            f.write(background_img.content)
    if not os.path.exists('assets/logo.png'):
        icon_img = requests.get('https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/assets/logo.png?raw=true')
        with open('assets/logo.png', 'wb') as f:
            f.write(icon_img.content)


profiles = []
profile_number = 0
name_input = ''
VERSION = "v1.1.0"

if __name__ == '__main__':
    check_files()
    settings = load_settings()
    # Initialize the TK window
    window = Window()
    add_prof_button = tk.CTkButton(window.control_frame, text="+", text_font=("Arial", 18), width=50, command=add_profile)
    add_prof_tooltip = ToolTip(add_prof_button, "Add a new profile")
    add_prof_button.pack(pady=10, anchor=tk.N)
    warning_label = tk.CTkLabel(window.profiles_list, text="No profiles found, use the + button to add a profile")
    warning_label.pack(pady=20, padx=100)

    if 'smapi_path' not in settings or not os.path.exists(settings['smapi_path']):
        if os.path.exists('C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'):
            settings['smapi_path'] = 'C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'
        else:
            popup = Popup("SMAPI not found!", "Select the SMAPI executable", window, False)
            window.wait_window(popup.popup)
            settings['smapi_path'] = filedialog.askopenfilename(title="Select StardewModdingAPI.exe", filetypes=[("StardewModdingAPI.exe", "*.exe")])
        save_settings()

    load_profiles()

    window.mainloop()

