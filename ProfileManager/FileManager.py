"""
@author: supercam19
@github: https://github.com/supercam19
@license: MIT
@description: Manages file loading and saving
"""

import json
from time import time
import os
from requests import get as get_url
from requests import exceptions
from ctypes import windll


def save_profile(data):
    # Save profile data by deleting old data, then dumping the entire list of profiles into the file
    with open('profiles.json', 'a') as f:
        f.truncate(0)
        json.dump(data, f, indent=4)


def edit_saved_profile(profiles_data, profile_name,  new_value=None, key=None, action='edit'):
    # Edit a profile in the save file
    if action == 'edit':
        # Compare profile names to find the one to edit
        for i, profile in enumerate(profiles_data):
            if profile['name'] == profile_name:
                # If a key is specified, edit that key, otherwise rewrite the entire profile
                if key is None:
                    profiles_data[i] = new_value
                else:
                    profile[key] = new_value
                    profiles_data[i] = profile
    elif action == 'delete':
        # Compare profile names to find the one to delete
        for profile in profiles_data:
            if profile['name'] == profile_name:
                profiles_data.remove(profile)
    save_profile(profiles_data)
    return profiles_data


def load_profiles():
    # Load profiles from the save file
    with open('profiles.json', 'r') as f:
        data = json.load(f)
    # This line returns an empty list if there are no profiles to prevent errors
    return [] if data == {} else data


def convert_legacy_profiles(profiles_data):
    # Automatically converts profiles stored in the old format to the new format
    with open('profiles.txt', 'r') as f:
        for line in f:
            prof_name, prof_path = line.split(';')
            profiles_data.append({'name': prof_name, 'path': prof_path, 'created': int(time())})
    save_profile(profiles_data)
    os.remove('profiles.txt')


def load_settings():
    # Load settings from the save file
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings


def save_settings(settings):
    # Save settings to the save file
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
                    try:
                        f.write(get_url(f'https://github.com/supercam19/SMAPI-Profile-Manager/blob/main/ProfileManager/{file}?raw=true').content)
                    except exceptions.ConnectionError:
                        windll.user32.MessageBoxW(None, u"Error downloading assets, check your internet connection or firewall", u"Error", 0x00000000 | 0x00000010)


def update_files():
    # Re-download files that might have changed in the update
    print('Updating files...')
    for file in ('assets/background.png', 'assets/iconsheet.png'):
        os.remove(file)
    check_files()

