import os
from tkinter import filedialog, PhotoImage
import customtkinter as tk
from UIelements import *
import requests
import json
from ctypes import windll
from subprocess import call
from time import time


class Profile:
    def __init__(self, info):
        self.name = info['name']
        if 'path' in info: self.path = info['path'].rstrip("\n")
        info['special'] = None if 'special' not in info else info['special']
        self.special = info['special']
        self.prof_info = info # all other profile information
        if 'last_launched' not in self.prof_info: self.prof_info['last_launched'] = -1
        self.prof_frame = tk.CTkFrame(window.profiles_list, width=480, height=32)
        self.prof_frame.pack_propagate(False)
        self.left_frame = tk.CTkFrame(self.prof_frame, width=320, height=32, fg_color='gray21', bg_color='gray21')
        self.left_frame.pack_propagate(False)
        self.right_frame = tk.CTkFrame(self.prof_frame, width=140, height=32, fg_color='gray21', bg_color='gray21')
        self.right_frame.pack_propagate(False)
        self.prof_title = tk.CTkLabel(self.left_frame, text=self.name, fg_color="gray21", text_font=("Arial", 12), anchor='w')
        self.prof_button = Button(self.right_frame, text="\U000025B6", fg_color="gray21", text_font=("Arial", 24), text_color='white', hover_color='gray21', width=32, command=self.select_profile)
        self.prof_edit = Button(self.right_frame, image=window.icons.gear, fg_color="gray21", height=40, type='button', text_color='white', hover_image=window.icons.gear_dark, width=32, command=self.edit_profile)
        self.prof_delete = Button(self.right_frame, width=32, image=window.icons.trash_closed, height=40, type='button', hover_image=window.icons.trash_opened, command=self.delete_profile)

        self.launch_tooltip = Tooltip(self.prof_button, "Launch the game with this profile")
        self.edit_tooltip = Tooltip(self.prof_edit, "Edit this profile")
        self.delete_tooltip = Tooltip(self.prof_delete, "Delete this profile")
        self.name_tooltip = Tooltip(self.prof_title, self.name)

    def draw_profile(self):
        self.prof_frame.pack(pady=2)
        self.left_frame.pack(side='left', padx=(10, 0))
        self.prof_title.pack(side=tk.LEFT, padx=(20, 10))
        self.prof_button.pack(side=tk.RIGHT, padx=(1, 2))
        self.prof_edit.pack(side=tk.RIGHT, padx=(1, 0))
        if self.special != 'unmodded': self.prof_delete.pack(side=tk.RIGHT)
        self.right_frame.pack(side='right')
        if 'warning_label' in globals(): warning_label.pack_forget()

    def select_profile(self):
        edit_saved_profile(self.name, int(time()), key='last_used')
        if self.special != 'unmodded':
            cmd = f'start cmd /c \"\"{settings["smapi_path"]}\" --mods-path \"{self.path}\"\"'
            call(cmd, shell=True)
        else:
            if bool(self.prof_info['force_smapi']):
                call(f'start cmd /c \"\"{settings["smapi_path"]}\"', shell=True)
                return
            game_path = settings['smapi_path']
            game_path = os.path.dirname(game_path)
            if os.path.exists(game_path + '/Stardew Valley.exe'):
                cmd = f'start cmd /c \"\"{game_path}/Stardew Valley.exe\"\"'
                call(cmd)
            else:
                cmd = f'start cmd /c \"\"{settings["smapi_path"]}\"'
                call(cmd, shell=True)

    def edit_profile(self):
        editor = ProfileEditor(window, self.prof_info, self.load_changed_info)
        window.wait_window(editor.editor)
        edit_saved_profile(self.name, self.prof_info, action='edit')
        self.name = self.prof_info['name']
        if 'path' in self.prof_info: self.path = self.prof_info['path'].rstrip("\n")
        self.prof_title.configure(text=self.name)

    def load_changed_info(self, info):
        self.prof_info = info

    def delete_profile(self):
        self.prof_frame.destroy()
        self.prof_title.destroy()
        self.prof_button.destroy()
        self.prof_delete.destroy()
        # Remove the profile from the text file
        edit_saved_profile(self.name, action='delete')
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
    profiles.append(Profile({'name': prof_name, 'path': prof_path, 'created': int(time())}))
    profiles[-1].draw_profile()
    profiles_data.append({'name': prof_name, 'path': prof_path, 'created': int(time())})
    save_profile(profiles_data)


def save_profile(data):
    with open('profiles.json', 'a') as f:
        f.truncate(0)
        json.dump(data, f, indent=4)


def edit_saved_profile(profile_name,  new_value=None, key=None, action='edit'):
    """
    Edits a saved profile
    :param profile_name: The name value of the profile to edit
    :param new_value: The new value to set the key to.
    :param key: The key to edit. If None, it will try to replace the entire profile
    :param action: The action to perform. Can be 'edit' or 'delete'
    """
    if action == 'edit':
        for i, profile in enumerate(profiles_data):
            if profile['name'] == profile_name:
                if key is None:
                    profiles_data[i] = new_value
                else:
                    profile[key] = new_value
                    profiles_data[i] = profile
            save_profile(profiles_data)
    elif action == 'delete':
        for profile in profiles_data:
            if profile['name'] == profile_name:
                profiles_data.remove(profile)
        save_profile(profiles_data)
    else:
        raise ValueError("Action must be either 'edit' or 'delete'")


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
            profiles_data.append({'name': prof_name, 'path': prof_path, 'created': int(time())})
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
    if 'force_smapi' not in profiles_data[0]: profiles_data.insert(0, {'name': 'Unmodded', 'force_smapi': False, 'special': 'unmodded'})
    for profile in profiles_data:
        profiles.append(Profile(profile))
        profiles[-1].draw_profile()

    if not profiles:
        warning_label = tk.CTkLabel(window.profiles_list, text="No profiles found, use the + button to add a profile")
        warning_label.pack(pady=20, padx=100)

    window.mainloop()

