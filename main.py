import os
from tkinter import filedialog, PhotoImage
import customtkinter as tk
from UIelements import *
import requests
import json
from ctypes import windll
from subprocess import call


class Profile:
    def __init__(self, name, path):
        self.name = name
        self.path = path.rstrip("\n")
        self.prof_frame = tk.CTkFrame(window.profiles_list, width=480, height=32)
        self.prof_frame.pack_propagate(False)
        self.left_frame = tk.CTkFrame(self.prof_frame, width=380, height=32, fg_color='gray21', bg_color='gray21')
        self.left_frame.pack_propagate(False)
        self.right_frame = tk.CTkFrame(self.prof_frame, width=100, height=32, fg_color='gray21', bg_color='gray21')
        self.right_frame.pack_propagate(False)
        self.prof_title = tk.CTkLabel(self.left_frame, text=self.name, fg_color="gray21", text_font=("Arial", 12), anchor='w')
        self.prof_button = Button(self.right_frame, text="\U000025B6", fg_color="gray21", text_font=("Arial", 24), text_color='white', hover_color='gray21', width=40)
        self.prof_delete = Button(self.right_frame, width=40, image=window.icons.trash_closed, height=40, type='button', hover_image=window.icons.trash_opened)
        self.prof_button.configure(command=self.select_profile)
        self.prof_delete.configure(command=self.delete_profile)

        self.launch_tooltip = Tooltip(self.prof_button, "Launch the game with this profile")
        self.delete_tooltip = Tooltip(self.prof_delete, "Delete this profile")
        self.name_tooltip = Tooltip(self.prof_title, self.name)

    def draw_profile(self):
        global profile_number
        profile_number += 1
        self.prof_frame.pack(pady=2)
        self.left_frame.pack(side='left', padx=(10, 0))
        self.right_frame.pack(side='right')
        self.prof_title.pack(side=tk.LEFT, padx=(20, 10))
        self.prof_button.pack(side=tk.RIGHT, padx=(2, 4))
        self.prof_delete.pack(side=tk.RIGHT)
        if 'warning_label' in globals(): warning_label.pack_forget()

    def select_profile(self):
        cmd = f'start cmd /c \"\"{settings["smapi_path"]}\" --mods-path \"{self.path}\"\"'
        call(cmd, shell=True)

    def delete_profile(self):
        self.prof_frame.destroy()
        self.prof_title.destroy()
        self.prof_button.destroy()
        self.prof_delete.destroy()
        # Remove the profile from the text file
        for profile in profiles_data:
            if profile['name'] == self.name:
                profiles_data.remove(profile)
        save_profile(profiles_data)


def add_profile():
    prof_path = filedialog.askdirectory()
    # Write the name of the profile to a text file to save for later
    popup = Popup("Name your profile", "Enter a name for your profile", window)
    # Wait for the popup to close
    window.wait_window(popup.popup)
    prof_name = str(popup_info)
    # set prof_name to the first 100 characters of itself if it is longer than 100 characters
    prof_name = prof_name[:100] if len(prof_name) > 100 else prof_name
    profiles.append(Profile(prof_name, prof_path))
    profiles[-1].draw_profile()
    save_profile(profiles_data)


def save_profile(data):
    with open('profiles.json', 'a') as f:
        f.truncate(0)
        json.dump(data, f, indent=4)


def load_profiles():
    with open('profiles.json', 'r') as f:
        try:
            profiles_json = json.load(f)
        except json.decoder.JSONDecodeError:
            return []
    return profiles_json


def convert_legacy_profiles():
    """
    Automatically converts profiles stored in the old format to the new format
    """
    with open('profiles.txt', 'r') as f:
        for line in f:
            prof_name, prof_path = line.split(';')
            profiles_data.append({'name': prof_name, 'path': prof_path})
    save_profile(profiles_data)
    os.remove('profiles.txt')


def load_settings():
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_settings():
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)


def check_files():
    # Check if critical files are missing, if so, download/create them
    if not os.path.exists('profiles.json'):
        with open('profiles.json', 'w') as f:
            f.write('')
    if not os.path.exists('settings.json'):
        with open('settings.json', 'w') as f:
            f.write('{}')
    if not os.path.exists('assets'):
        os.mkdir('assets')
    if not os.path.exists('profiles'):
        os.mkdir('profiles')
    if not os.path.exists('assets/background.png'):
        background_img = requests.get('https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/assets/background.png?raw=true')
        with open('assets/background.png', 'wb') as f:
            f.write(background_img.content)
    if not os.path.exists('assets/iconsheet.png'):
        icon_img = requests.get('https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/assets/iconsheet.png?raw=true')
        with open('assets/iconsheet.png', 'wb') as f:
            f.write(icon_img.content)


profiles = []
profile_number = 0
name_input = ''
VERSION = "v1.1.4"

if __name__ == '__main__':
    check_files()
    settings = load_settings()
    profiles_data = []
    # Initialize the TK window
    tk.set_appearance_mode("dark")
    windll.user32.SetProcessDPIAware()
    window = Window()
    window.add_prof_button.configure(command=add_profile)

    if 'smapi_path' not in settings or not os.path.exists(settings['smapi_path']):
        if os.path.exists('C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'):
            settings['smapi_path'] = 'C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'
        else:
            popup = Popup("SMAPI not found!", "Select the SMAPI executable", window, False)
            window.wait_window(popup.popup)
            settings['smapi_path'] = filedialog.askopenfilename(title="Select StardewModdingAPI.exe", filetypes=[("StardewModdingAPI.exe", "*.exe")])
        save_settings()

    if os.path.exists('profiles.txt'): convert_legacy_profiles()
    profiles_data = load_profiles()
    for profile in profiles_data:
        profiles.append(Profile(profile['name'], profile['path']))
        profiles[-1].draw_profile()

    if not profiles:
        warning_label = tk.CTkLabel(window.profiles_list, text="No profiles found, use the + button to add a profile")
        warning_label.pack(pady=20, padx=100)

    window.mainloop()

