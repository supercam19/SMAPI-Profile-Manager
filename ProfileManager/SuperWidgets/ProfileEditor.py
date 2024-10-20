"""
@author: supercam19
@github: https://github.com/supercam19
@license: MIT
@description: Profile editor window
"""

import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog
# noinspection PyPackages
from .SuperWidgets import Frame, Button
# noinspection PyPackages
from .Tooltip import Tooltip


class ProfileEditor:
    # Profile editor window
    def __init__(self, root, profile_data, callback):
        self.prof_info = profile_data
        self.callback = callback
        self.dropdown_active = False
        self.properties_frame = None
        self.protected_values = ('created', 'last_launched', 'mods')  # Do not allow user to modify these
        self.editor = ctk.CTkToplevel(root, fg_color="gray18")
        self.editor.withdraw()
        self.editor.after(10, self.display)
        self.editor.title("Profile Editor - " + self.prof_info['name'])
        self.editor.geometry("+%d+%d" % (root.winfo_x() + 100, root.winfo_y() + 100))

        # Edit profile name
        self.eName = self.editable_text('Name:')[2]  # returns the textbox object
        self.eName.insert(0, self.prof_info['name'])

        if self.prof_info['special'] != 'unmodded':
            # Show a path editor if this is not the unmodded profile
            self.ePathFrame, _, self.ePathEntry = self.editable_text('Path:', entry_alignement='left')
            self.ePathEntry.pack_forget()
            self.browse_button = ctk.CTkButton(self.ePathFrame, text="...", width=5,
                                               command=self.browse_path)
            self.browse_button.pack(padx=(0, 10), side='right')
            self.browse_button_tooltip = Tooltip(self.browse_button, "Browse profile path")
            self.ePathEntry.pack(side='right', padx=(0, 10), pady=8)
            self.ePathEntry.pack_propagate(False)
            self.ePathEntry.insert(0, self.prof_info['path'])
            self.ePathEntry.configure(width=173)
        else:
            # Show the force smapi checkbox if this is the unmodded profile
            self.eForceSMAPI = self.editable_true_false('Force SMAPI:')[2]
            self.eForceSMAPI.select() if self.prof_info['force_smapi'] else self.eForceSMAPI.deselect()

        # Pin profile
        self.ePin = self.editable_true_false('Pin:')[2]
        if 'pinned' in self.prof_info:
            self.ePin.select() if self.prof_info['pinned'] else self.ePin.deselect()

        self.properties_dropdown = ctk.CTkButton(self.editor, text=('\U000023AF' * 4) + ' Properties v ' + ('\U000023AF' * 25), width=10,
                                                 command=self.dropdown_manager, fg_color='gray18', hover_color='gray22')
        self.properties_dropdown.pack(pady=(10, 0))

        self.apply_button = ctk.CTkButton(self.editor, text="Apply", command=self.apply_changes, width=10)
        self.apply_tooltip = Tooltip(self.apply_button, "Apply changes")
        self.apply_button.pack(pady=10)

        self.editor.bind("<Return>", self.apply_changes)

    def editable_text(self, title, entry_alignement='right'):
        # Creates a frame with a label and a textbox
        frame = Frame(self.editor, width=300, height=40, fg_color='gray18')
        frame.pack_propagate(False)
        frame.pack()
        label = ctk.CTkLabel(frame, text=title, width=30, anchor='w')
        label.pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, width=210)
        entry.pack(side=entry_alignement, padx=(0, 10), pady=8)
        return frame, label, entry

    def editable_true_false(self, title):
        # Creates a frame with a label and a checkbox
        frame = Frame(self.editor, width=300, height=40, fg_color='gray18')
        frame.pack_propagate(False)
        frame.pack(expand=True, fill='both')
        label = ctk.CTkLabel(frame, text=title, width=50, anchor='w')
        label.pack(side="left", padx=10)
        check = ctk.CTkCheckBox(frame, text='')
        check.pack(padx=3, side='right')
        return frame, label, check

    def dropdown_manager(self):
        if self.dropdown_active:
            self.dropdown_active = False
            self.properties_dropdown.configure(text=('\U000023AF' * 4) + ' Properties v ' + ('\U000023AF' * 25))
            self.properties_frame.destroy()
        else:
            self.dropdown_active = True
            self.apply_button.pack_forget()
            self.properties_dropdown.configure(text=('\U000023AF' * 4) + ' Properties ^ ' + ('\U000023AF' * 25))
            self.properties_frame = Frame(self.editor, fg_color='gray18', width=240, height=40 * len(self.protected_values))
            self.properties_frame.pack_propagate(False)
            self.properties_frame.pack(pady=10)
            self.apply_button.pack(pady=10)
            i = 0
            for key, value in self.prof_info.items():
                if key in self.protected_values:
                    i += 1
                    if key == 'created' or key == 'last_launched':
                        if value == -1:
                            value = 'Never'
                        else:
                            value = datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
                    # Alternate colours for each row
                    colour = 'gray35' if i % 2 == 0 else 'gray25'
                    # Nice formatting for keys
                    key = key.replace('_', ' ').title()
                    subframe = Frame(self.properties_frame, width=300, height=40, fg_color=colour, bg_color=colour)
                    subframe.pack_propagate(False)
                    subframe.pack()
                    key_label = ctk.CTkLabel(subframe, text=key, width=30, fg_color=colour)
                    key_label.pack(side="left", padx=2)
                    value_label = ctk.CTkLabel(subframe, text=value, width=210, fg_color=colour, anchor='e')
                    value_label.pack(side="right", padx=2)

    def apply_changes(self, event=None):
        # Apply changes to the profile by calling the callback function in main.py
        if self.prof_info['special'] == None:
            self.callback({'name': self.eName.get(), 'path': self.ePathEntry.get(), 'created': self.prof_info['created'],
                           'last_launched': self.prof_info['last_launched'], 'special': None, 'pinned': self.ePin.get()})
        elif self.prof_info['special'] == 'unmodded':
            self.callback({'name': self.eName.get(), 'special': 'unmodded', 'force_smapi': self.eForceSMAPI.get(), 'created': self.prof_info['created'],
                           'last_launched': self.prof_info['last_launched'], 'pinned': self.ePin.get()})
        self.editor.destroy()

    def browse_path(self):
        # File explorer window for browsing the mod folder path
        new_path = filedialog.askdirectory()
        # Put the profile editor back on top of other windows once the explorer closes
        self.editor.attributes('-topmost', True)
        # Put the new folder path in the text box
        self.ePathEntry.delete(0, 'end')
        self.ePathEntry.insert(0, new_path)
        # Stop the profile editor from sticking to above other windows (still on top, just not stuck)
        self.editor.attributes('-topmost', False)

    def display(self):
        self.editor.deiconify()
        self.editor.focus()
