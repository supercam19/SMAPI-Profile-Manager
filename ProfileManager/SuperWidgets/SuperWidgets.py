"""
@author: supercam19
@github: https://github.com/supercam19
@license: MIT
@description: Base customtkinter widgets that are modified for this program
"""

import customtkinter as ctk
from .Util import get_all_children


class Frame(ctk.CTkFrame):
    # Frame object (just a regular CTkFrame)
    def __init__(self, parent, vfx=False, **kwargs):
        super().__init__(parent, **kwargs)
        # define size of frame
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)
        # Adds visual hover effets if vfx is True
        if vfx:
            self.bind("<Enter>", lambda x: self.configure(highlightthickness=1), add="+")
            self.bind("<Leave>", lambda x: self.configure(highlightthickness=0), add="+")
            # for child in get_all_children(self, True, True):
            #     print(child)
            #     child.bind("<Enter>", lambda x: self.configure(fg_color='gray15'), add="+")
            #     child.bind("<Leave>", lambda x: self.configure(fg_color='gray21'), add="+")


class Button(ctk.CTkButton):
    # Define a custom button that changes colour or image on hover
    def __init__(self, parent, type='text', hover_image=None, **kwargs):
        super().__init__(parent, hover=False, **kwargs)
        self.text_color_default = kwargs.get("text_color", "white")
        self.configure(text_color=self.text_color_default)
        self.image_default = kwargs.get("image", None)
        self.configure(image=self.image_default)
        self.state = kwargs.get("state", "normal")
        self.configure(state=self.state)
        self.text = kwargs.get("text", "")
        self.configure(text=self.text)

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