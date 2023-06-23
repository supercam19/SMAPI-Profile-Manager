import customtkinter as ctk
import webbrowser


class HelpMenu:
    def __init__(self, root):
        self.menu = ctk.CTkToplevel(root)
        self.menu.geometry("+%d+%d" % (root.winfo_x() + 100, root.winfo_y() + 100))
        self.menu.title("Help Menu")
        self.menu.resizable(False, False)
        self.stack = []
        for i in range(4):
            self.stack.append(ctk.CTkFrame(self.menu))
            self.stack[i].pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.YES)

        self.stack[0].configure(bg_color='gray24', fg_color='gray24')
        self.title = ctk.CTkLabel(self.stack[0], text="SMAPI Profile Manager Help", text_font=("Arial", 20), fg_color="gray24", height=40, anchor='center')
        self.title.pack(pady=(10, 0), side=ctk.LEFT, fill=ctk.X, expand=ctk.YES)
        self.stack[1].configure(bg_color='gray24', fg_color='gray24')
        self.seperator = ctk.CTkLabel(self.stack[1], text="\U000023AF"*28, text_font=("Arial", 20), fg_color='gray24', height=5)
        self.seperator.pack(side=ctk.LEFT)

        self.help_frameL = ctk.CTkFrame(self.stack[2], bg_color='gray20')
        self.help_frameL.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=ctk.YES)
        self.help_frameR = ctk.CTkFrame(self.stack[2], bg_color='gray20')
        self.help_frameR.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=ctk.YES)
        self.help_selection = ctk.IntVar()
        self.option_radio_1 = ctk.CTkRadioButton(self.help_frameL, text="Open Github Page", variable=self.help_selection, value=0)
        self.option_radio_1.pack(padx=10, pady=20, side=ctk.TOP)
        self.option_radio_1.select()
        self.option_radio_2 = ctk.CTkRadioButton(self.help_frameL, text="Open Instructions", variable=self.help_selection, value=1)
        self.option_radio_2.pack(padx=10, pady=20, side=ctk.TOP)
        self.option_radio_3 = ctk.CTkRadioButton(self.help_frameR, text="Report Issue              ", variable=self.help_selection, value=2)
        self.option_radio_3.pack(padx=10, pady=20, side=ctk.TOP)
        self.option_radio_4 = ctk.CTkRadioButton(self.help_frameR, text="Contribute to Project", variable=self.help_selection, value=3)
        self.option_radio_4.pack(padx=10, pady=20, side=ctk.TOP)

        self.button_frame = ctk.CTkFrame(self.stack[3])
        self.stack[3].configure(bg_color='gray24', fg_color='gray24')
        self.ok_button = ctk.CTkButton(self.stack[3], text="OK", command=self.visit, fg_color='gray24', bg_color='gray24', hover_color='gray18')
        self.ok_button.pack(side=ctk.RIGHT, fill='both', expand=True)
        self.ok_button.bind("<Enter>", lambda event: self.ok_button.configure(bg_color='gray18'))
        self.ok_button.bind("<Leave>", lambda event: self.ok_button.configure(bg_color='gray24'))
        self.cancel_button = ctk.CTkButton(self.stack[3], text="Cancel", command=self.menu.destroy, fg_color='gray24', bg_color='gray24', hover_color='gray18')
        self.cancel_button.pack(side=ctk.RIGHT, fill='both', expand=True)
        self.cancel_button.bind("<Enter>", lambda event: self.cancel_button.configure(bg_color='gray18'))
        self.cancel_button.bind("<Leave>", lambda event: self.cancel_button.configure(bg_color='gray24'))

    def visit(self):
        links = ('https://github.com/supercam19/SMAPI-Profile-Manager',
                 'https://github.com/supercam19/SMAPI-Profile-Manager#how-to-use',
                 'https://github.com/supercam19/SMAPI-Profile-Manager/issues/new',
                 'https://github.com/supercam19/SMAPI-Profile-Manager/pulls')
        webbrowser.open(links[self.help_selection.get()])