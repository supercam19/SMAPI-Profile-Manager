from tkinter import filedialog
import customtkinter as tk
from UIelements import *
from FileManager import *
from ctypes import windll
from subprocess import call
from time import time


class Profile:
    def __init__(self, info):
        # Extract profile info from the dict 'info'
        self.name = info['name']
        if 'path' in info: self.path = info['path'].rstrip("\n")
        info['special'] = None if 'special' not in info else info['special']
        self.special = info['special']
        self.prof_info = info  # all other profile information
        if 'last_launched' not in self.prof_info: self.prof_info['last_launched'] = -1
        self.created = info['created']
        self.last_launched = info['last_launched']
        # Define profile widgets
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

        # Define profile tooltips
        self.launch_tooltip = Tooltip(self.prof_button, "Launch the game with this profile")
        self.edit_tooltip = Tooltip(self.prof_edit, "Edit this profile")
        self.delete_tooltip = Tooltip(self.prof_delete, "Delete this profile")
        self.name_tooltip = Tooltip(self.prof_title, self.name)

    def draw_profile(self):
        # Pack all profile widgets
        self.prof_frame.pack(pady=2)
        self.left_frame.pack(side='left', padx=(10, 0))
        self.prof_title.pack(side=tk.LEFT, padx=(20, 10))
        self.prof_button.pack(side=tk.RIGHT, padx=(1, 2))
        self.prof_edit.pack(side=tk.RIGHT, padx=(1, 0))
        if self.special != 'unmodded': self.prof_delete.pack(side=tk.RIGHT)
        self.right_frame.pack(side='right')

    def hide_profile(self):
        # Unpack all profile widgets
        for widget in self.prof_frame.winfo_children(): widget.pack_forget()
        self.prof_frame.pack_forget()

    def select_profile(self):
        # Launches the game with the selected profile
        # Update the Last Played stat for the profile
        edit_saved_profile(profiles_data, self.name, int(time()), key='last_launched')
        # If not the unmodded profile, launch with SMAPI and a custom mods path
        if self.special != 'unmodded':
            cmd = f'start cmd /c \"\"{settings["smapi_path"]}\" --mods-path \"{self.path}\"\"'
            call(cmd, shell=True)
        # If it is the unmodded profile...
        else:
            # and the profile has the setting force_smapi set to True, launch with SMAPI...
            if bool(self.prof_info['force_smapi']):
                call(f'\"{settings["smapi_path"]}\"', shell=True)
                return
            # otherwise try to launch the game through the vanilla exe file...
            game_path = os.path.dirname(settings['smapi_path'])
            if os.path.exists(game_path + '/Stardew Valley.exe'):
                cmd = f'start cmd /c \"\"{game_path}/Stardew Valley.exe\"\"'
                call(cmd)
            # if the executable can't be found, launch through SMAPI.
            else:
                cmd = f'start cmd /c \"\"{settings["smapi_path"]}\"\"'
                call(cmd, shell=True)

    def edit_profile(self):
        # Launches the profile editor, then applies changes
        editor = ProfileEditor(window, profile_data=self.prof_info, callback=self.load_changed_info)
        window.wait_window(editor.editor)
        edit_saved_profile(profiles_data, self.name, self.prof_info, action='edit')
        self.name = self.prof_info['name']
        if 'path' in self.prof_info: self.path = self.prof_info['path'].rstrip("\n")
        self.prof_title.configure(text=self.name)

    def load_changed_info(self, info):
        # Used to pass any changed profile info back into the main file from UIelements
        self.prof_info = info

    def delete_profile(self):
        # Remove profile widgets, then remove profile from the save file
        self.prof_frame.destroy()
        self.prof_title.destroy()
        self.prof_button.destroy()
        self.prof_delete.destroy()
        # Remove the profile from the text file
        edit_saved_profile(profiles_data, self.name, action='delete')


def add_profile():
    # Add a new profile (top right button)
    prof_path = filedialog.askdirectory()
    popup = Popup("Name your profile", "Enter a name for your profile", window)
    window.wait_window(popup.popup)
    # Gets the information from the popup (profile name)
    prof_name = str(popup_info)
    # Restrict profile name to 100 characters
    prof_name = prof_name[:100] if len(prof_name) > 100 else prof_name
    profiles.append(Profile({'name': prof_name, 'path': prof_path, 'created': int(time())}))
    profiles[-1].draw_profile()
    profiles_data.append({'name': prof_name, 'path': prof_path, 'created': int(time())})
    save_profile(profiles_data)

def sort_profiles(sort=None):
    # Manages profile sorting
    invert = window.invert_sort_checkbox.get()
    # Save the unmodded profile to local var unmodded
    unmodded = profiles[0]
    # Remove unmodded profile from profiles list
    profiles.pop(0)
    if sort is None:
        # If the sorting method didn't change, but invert was toggled
        profiles.reverse()
        # Re-insert the unmodded profile back at position 0
        profiles.insert(0, unmodded)
    else:
        # If the sorting method does change...
        if sort == 'Name':
            profiles.sort(key=lambda x: x.name, reverse=invert)
        elif sort == 'Created':
            profiles.sort(key=lambda x: x.created, reverse=invert)
        elif sort == 'Last Played':
            profiles.sort(key=lambda x: x.last_launched, reverse=invert)
        # Re-insert the unmodded profile back at position 0
        profiles.insert(0, unmodded)
    # Un-pack all the profiles first...
    for profile in profiles:
        profile.hide_profile()
    # Then repack them in the new order
    for profile in profiles:
        profile.draw_profile()

    # Save sorting preferences to settings file
    if sort is not None: settings['sort'] = sort
    settings['invert'] = invert
    save_settings(settings)


profiles = []
name_input = ''
VERSION = "v1.2.1"

if __name__ == '__main__':
    check_files()
    settings = load_settings()
    profiles_data = []
    # Initialize the TK window
    tk.set_appearance_mode("dark")
    # This method makes the tk window scale properly at different monitor DPI scales
    windll.user32.SetProcessDPIAware()
    window = Window(settings, sort_callback=sort_profiles)
    window.add_prof_button.configure(command=add_profile)

    # Check for the SMAPI executable and prompt user if not found
    if 'smapi_path' not in settings or not os.path.exists(settings['smapi_path']):
        if os.path.exists('C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'):
            settings['smapi_path'] = 'C:/Program Files (x86)/Steam/steamapps/common/Stardew Valley/StardewModdingAPI.exe'
        else:
            popup = Popup("SMAPI not found!", "Select the SMAPI executable", window, False)
            window.wait_window(popup.popup)
            settings['smapi_path'] = filedialog.askopenfilename(title="Select StardewModdingAPI.exe", filetypes=[("StardewModdingAPI.exe", "*.exe")])
        save_settings(settings)

    if os.path.exists('profiles.txt'): convert_legacy_profiles(profiles_data)
    profiles_data = load_profiles()
    # Make sure the unmodded profile is added to the save
    if profiles_data == []: profiles_data.insert(0, {'name': 'Unmodded', 'force_smapi': False, 'special': 'unmodded', 'created': int(time())})
    elif 'force_smapi' not in profiles_data[0]: profiles_data.insert(0, {'name': 'Unmodded', 'force_smapi': False, 'special': 'unmodded', 'created': int(time())})
    for profile in profiles_data:
        profiles.append(Profile(profile))
    sort_profiles(settings['sort']) if 'sort' in settings else sort_profiles('Name')
    for profile in profiles:
        profile.draw_profile()

    window.mainloop()

