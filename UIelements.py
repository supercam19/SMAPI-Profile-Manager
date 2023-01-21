import customtkinter as ctk
from tkinter import PhotoImage
from main import VERSION
from tkinter import filedialog
from webbrowser import open as open_url
from datetime import datetime


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


class Frame(ctk.CTkFrame):
    # Frame object (just a regular CTkFrame)
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # define size of frame
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)


class Button(ctk.CTkButton):
    # Define a custom button that changes colour or image on hover
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
        # On button hover
        if self.type == 'text':
            self.configure(text_color="gray45")
        elif self.type == 'button':
            self.configure(image=self.hover_image)

    def leave(self, event=None):
        # On button leave
        if self.type == 'text':
            self.configure(text_color=self.text_color_default)
        elif self.type == 'button':
            self.configure(image=self.image_default)


class Popup:
    # Popup window, can have textbox, or just a message
    def __init__(self, title, message, root, text_box=True, callback=None):
        self.popup = ctk.CTkToplevel(root)
        self.popup.title(title)
        self.popup.geometry("300x100+%d+%d" % (root.winfo_x() + 100, root.winfo_y() + 100))
        self.popup.focus()
        # self.popup.resizable(False, False)
        self.popup.protocol("WM_DELETE_WINDOW", self.destruct)
        self.popup_label = ctk.CTkLabel(self.popup, text=message)
        self.popup_label.pack()
        self.text_box = text_box
        self.callback = callback
        if text_box:
            self.popup_text = ctk.CTkEntry(self.popup, width=200)
            self.popup_text.after(100, self.popup_text.focus)
            self.popup_text.pack(pady=10)
        self.popup_button = ctk.CTkButton(self.popup, text="OK", command=self.close_popup, width=10)
        self.popup_button.pack()

        self.popup.bind("<Return>", self.close_popup)

    def close_popup(self, event=None):
        # Save text box value to the popup_info object
        if self.text_box: self.callback({"name": self.popup_text.get()})
        self.popup.destroy()

    def destruct(self):
        # If the popup is closed, set the popup_info object to None
        self.callback({"name": None})
        self.popup.destroy()


class ProfileEditor:
    # Profile editor window
    def __init__(self, root, profile_data, callback):
        self.prof_info = profile_data
        self.callback = callback
        self.dropdown_active = False
        self.properties_frame = None
        self.protected_values = ('created', 'last_launched')  # Do not allow user to modify these
        self.editor = ctk.CTkToplevel(root, bg="gray18")
        self.editor.title("Profile Editor - " + self.prof_info['name'])
        self.editor.geometry("+%d+%d" % (root.winfo_x() + 100, root.winfo_y() + 100))

        # Edit profile name
        self.eName = self.editable_text('Name:')[2]  # returns the textbox object
        self.eName.insert(0, self.prof_info['name'])

        if self.prof_info['special'] != 'unmodded':
            # Show a path editor if this is not the unmodded profile
            self.ePathFrame, _, self.ePathEntry = self.editable_text('Path:', entry_alignement='left')
            self.browse_button = ctk.CTkButton(self.ePathFrame, text="...", width=5,
                                     command=self.browse_path)
            self.browse_button.pack(padx=(0, 10), side='right')
            self.browse_button_tooltip = Tooltip(self.browse_button, "Browse profile path")
            self.ePathEntry.insert(0, self.prof_info['path'])
        else:
            # Show the force smapi checkbox if this is the unmodded profile
            self.eForceSMAPI = self.editable_true_false('Force SMAPI:')[2]
            self.eForceSMAPI.select() if self.prof_info['force_smapi'] else self.eForceSMAPI.deselect()

        self.properties_dropdown = ctk.CTkButton(self.editor, text=('\U000023AF'*4) + ' Properties v ' + ('\U000023AF'*25), width=10,
                                       command=self.dropdown_manager, fg_color='gray18', hover_color='gray22')
        self.properties_dropdown.pack(pady=(10, 0))

        self.apply_button = ctk.CTkButton(self.editor, text="Apply", command=self.apply_changes, width=10)
        self.apply_tooltip = Tooltip(self.apply_button, "Apply changes")
        self.apply_button.pack(pady=10)

        self.editor.bind("<Return>", self.apply_changes)

    def editable_text(self, title, entry_alignement='right'):
        # Creates a frame with a label and a textbox
        frame = Frame(self.editor, width=300, height=40)
        frame.pack_propagate(False)
        frame.pack()
        label = ctk.CTkLabel(frame, text=title, width=30)
        label.pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, width=210)
        entry.pack(side=entry_alignement, padx=(0, 10), pady=8)
        return frame, label, entry

    def editable_true_false(self, title):
        # Creates a frame with a label and a checkbox
        frame = Frame(self.editor, width=300, height=40)
        frame.pack_propagate(False)
        frame.pack()
        label = ctk.CTkLabel(frame, text=title, width=50)
        label.pack(side="left", padx=10)
        check = ctk.CTkCheckBox(frame, text='')
        check.pack(padx=10, side='right')
        return frame, label, check

    def dropdown_manager(self):
        if self.dropdown_active:
            self.dropdown_active = False
            self.properties_dropdown.configure(text=('\U000023AF'*4) + ' Properties v ' + ('\U000023AF'*25))
            self.properties_frame.destroy()
        else:
            self.dropdown_active = True
            self.apply_button.pack_forget()
            self.properties_dropdown.configure(text=('\U000023AF'*4) + ' Properties ^ ' + ('\U000023AF'*25))
            self.properties_frame = Frame(self.editor, bg="gray18", width=240, height=40*len(self.protected_values))
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
                    colour = 'gray45' if i % 2 == 0 else 'gray30'
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
                           'last_launched': self.prof_info['last_launched'], 'special': None})
        elif self.prof_info['special'] == 'unmodded':
            self.callback({'name': self.eName.get(), 'special': 'unmodded', 'force_smapi': self.eForceSMAPI.get(), 'created': self.prof_info['created'],
                           'last_launched': self.prof_info['last_launched']})
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


class Tooltip:
    # Mouse hover tooltips that can be attached to widgets
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
        self.id = self.widget.after(self.wait_time, self.show_tip)

    def unschedule(self):
        # Unschedule scheduled popups
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tip(self, event=None):
        # Get the position the tooltip needs to appear at
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_pointerx() + 1
        y += self.widget.winfo_pointery() + 1
        self.tw = ctk.CTkToplevel(self.widget)
        # Leaves only the label and removes the topbar of the window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f'+{x}+{y}')
        """
        The background colour and the foreground colour need to be really similar because the label widget
        has un-removable anti-aliasing that makes the colors blend -> there will be different colour pixels
        on the edge of the label.
        """
        self.tw.wm_attributes('-transparentcolor', '#555555')
        self.tw.configure(bg="#555555")
        label = ctk.CTkLabel(self.tw, text=self.text, corner_radius=10, bg_color='#555555', fg_color='#545454', width=1)
        label.pack(padx=1, pady=1)
        self.tw.geometry = label.winfo_width() + 1, label.winfo_height() + 1

    def hide_tip(self):
        self.unschedule()
        if self.tw: self.tw.withdraw()


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