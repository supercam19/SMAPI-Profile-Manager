import os
from tkinter import filedialog
import customtkinter as tk
from UIelements import *
from requests import get as get_url
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
        self.created = info['created']
        self.last_launched = info['last_launched']
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

    def hide_profile(self):
        self.prof_frame.pack_forget()
        self.prof_title.pack_forget()
        self.prof_button.pack_forget()
        self.prof_edit.pack_forget()
        self.prof_delete.pack_forget()

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
                cmd = f'\"{game_path}/Stardew Valley.exe\"'
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
    popup = Popup("Name your profile", "Enter a name for your profile", window)
    window.wait_window(popup.popup)
    prof_name = str(popup_info)
    # Restrict profile name to 100 characters
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
    if action == 'edit':
        for i, profile in enumerate(profiles_data):
            if profile['name'] == profile_name:
                if key is None:
                    profiles_data[i] = new_value
                else:
                    profile[key] = new_value
                    profiles_data[i] = profile
    elif action == 'delete':
        for profile in profiles_data:
            if profile['name'] == profile_name:
                profiles_data.remove(profile)
    save_profile(profiles_data)


def load_profiles():
    with open('profiles.json', 'r') as f:
        if f.read() == '{}': return []
        else: return json.load(f)


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
    check = ('profiles.json', 'settings.json', 'assets', 'assets/background.png', 'assets/iconsheet.png')
    for file in check:
        if file.endswith('.json'):
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    f.write('{}')
        elif '.' not in file:
            if not os.path.exists(file):
                os.mkdir(file)
        elif file.endswith('.png'):
            if not os.path.exists(file):
                with open(file, 'wb') as f:
                    f.write(get_url(f'https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/{file}?raw=true').content)


def sort_profiles(sort=None):
    invert = window.invert_sort_checkbox.get()
    unmodded = profiles[0]
    profiles.pop(0)
    if sort is None:
        profiles.reverse()
        profiles.insert(0, unmodded)
    else:
        if sort == 'Name':
            profiles.sort(key=lambda x: x.name, reverse=invert)
        elif sort == 'Created':
            profiles.sort(key=lambda x: x.created, reverse=invert)
        elif sort == 'Last Played':
            profiles.sort(key=lambda x: x.last_launched, reverse=invert)
        profiles.insert(0, unmodded)
    for profile in profiles:
        profile.hide_profile()
    for profile in profiles:
        profile.draw_profile()

    if sort is not None: settings['sort'] = sort
    settings['invert'] = invert
    save_settings()


profiles = []
name_input = ''
VERSION = "v1.2.0"

if __name__ == '__main__':
    check_files()
    settings = load_settings()
    profiles_data = []
    # Initialize the TK window
    tk.set_appearance_mode("dark")
    windll.user32.SetProcessDPIAware()
    window = Window(settings, sort_callback=sort_profiles)
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
    if profiles_data == []: profiles_data.insert(0, {'name': 'Unmodded', 'force_smapi': False, 'special': 'unmodded', 'created': int(time())})
    elif 'force_smapi' not in profiles_data[0]: profiles_data.insert(0, {'name': 'Unmodded', 'force_smapi': False, 'special': 'unmodded', 'created': int(time())})
    for profile in profiles_data:
        profiles.append(Profile(profile))
    sort_profiles(settings['sort']) if 'sort' in settings else sort_profiles('Name')
    for profile in profiles:
        profile.draw_profile()

    window.mainloop()

