"""Dialog windows for data selection and filtering."""

from tkinter import *


# Theme colors (matching main_window.py)
THEME = {
    "bg": "#2c3e50",
    "fg": "white",
    "accent": "#4ecca3",
    "entry_bg": "#34495e",
    "entry_fg": "white",
    "button_bg": "#6c5ce7",
    "button_hover": "#a29bfe",
    "header_bg": "#1a252f",
    "success": "#4ecca3",
}


class SelectDataDialog:
    """Dialog for selecting candidate filtering criteria."""

    def __init__(self, parent):
        self.parent = parent
        self.criteria = {}
        self.applied = False
        self.entry_data = []

    def show(self) -> dict:
        """
        Show the dialog and return the selected criteria.

        Returns:
            Dictionary of filter criteria, or empty dict if cancelled
        """
        self._create_dialog()
        return self.criteria if self.applied else {}

    def _create_dialog(self):
        """Create and configure the dialog window."""
        self.dialog = Toplevel(self.parent)
        self.dialog.title("Filter Candidates")
        self.dialog.configure(bg=THEME["bg"])
        self.dialog.resizable(False, False)

        # Center the window
        dialog_width = 600
        dialog_height = 500
        position_right = int(self.dialog.winfo_screenwidth() / 2 - dialog_width / 2)
        position_down = int(self.dialog.winfo_screenheight() / 2 - dialog_height / 2)
        self.dialog.geometry(
            f"{dialog_width}x{dialog_height}+{position_right}+{position_down}"
        )

        # Make modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # Header
        header_frame = Frame(self.dialog, bg=THEME["header_bg"], height=60)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)

        Label(
            header_frame,
            text="🔍 Filter Candidates",
            bg=THEME["header_bg"],
            fg=THEME["accent"],
            font=("calibre", 18, "bold"),
        ).pack(pady=15)

        # Subtitle
        Label(
            self.dialog,
            text="Set criteria to narrow down your candidate search",
            bg=THEME["bg"],
            fg="#95a5a6",
            font=("calibre", 11),
        ).pack(pady=(10, 20))

        # Form frame
        form_frame = Frame(self.dialog, bg=THEME["bg"])
        form_frame.pack(fill=BOTH, expand=True, padx=40)

        row = 0

        # Nationality
        nationality_var = StringVar()
        self.entry_data.append(nationality_var)
        self._create_field(
            form_frame,
            "Nationality:",
            nationality_var,
            row,
            width=30,
            hint="e.g., German, British",
        )
        row += 1

        # Age range
        age_frame = Frame(form_frame, bg=THEME["bg"])
        age_frame.grid(row=row, column=0, columnspan=2, sticky="w", pady=8)

        Label(
            age_frame,
            text="Age Range:",
            bg=THEME["bg"],
            fg=THEME["fg"],
            font=("calibre", 12),
        ).pack(side=LEFT)

        age_min_var = StringVar()
        age_max_var = StringVar()
        self.entry_data.extend([age_min_var, age_max_var])

        Entry(
            age_frame,
            textvariable=age_min_var,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["entry_fg"],
            width=6,
            font=("calibre", 12),
        ).pack(side=LEFT, padx=(10, 5))
        Label(
            age_frame, text="to", bg=THEME["bg"], fg=THEME["fg"], font=("calibre", 12)
        ).pack(side=LEFT, padx=5)
        Entry(
            age_frame,
            textvariable=age_max_var,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["entry_fg"],
            width=6,
            font=("calibre", 12),
        ).pack(side=LEFT, padx=(5, 10))
        Label(
            age_frame, text="years", bg=THEME["bg"], fg="#95a5a6", font=("calibre", 11)
        ).pack(side=LEFT)
        row += 1

        # Sex
        sex_var = StringVar()
        self.entry_data.append(sex_var)
        self._create_field(form_frame, "Sex:", sex_var, row, width=8, hint="M or F")
        row += 1

        # Experience
        exp_frame = Frame(form_frame, bg=THEME["bg"])
        exp_frame.grid(row=row, column=0, columnspan=2, sticky="w", pady=8)

        Label(
            exp_frame,
            text="Min. Experience:",
            bg=THEME["bg"],
            fg=THEME["fg"],
            font=("calibre", 12),
        ).pack(side=LEFT)

        experience_var = StringVar()
        self.entry_data.append(experience_var)

        Entry(
            exp_frame,
            textvariable=experience_var,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["entry_fg"],
            width=6,
            font=("calibre", 12),
        ).pack(side=LEFT, padx=(10, 5))
        Label(
            exp_frame, text="years", bg=THEME["bg"], fg="#95a5a6", font=("calibre", 11)
        ).pack(side=LEFT)
        row += 1

        # Skills
        skills_var = StringVar()
        self.entry_data.append(skills_var)
        self._create_field(
            form_frame,
            "Required Skills:",
            skills_var,
            row,
            width=35,
            hint="comma-separated",
        )
        row += 1

        # Languages
        languages_var = StringVar()
        self.entry_data.append(languages_var)
        self._create_field(
            form_frame,
            "Required Languages:",
            languages_var,
            row,
            width=35,
            hint="comma-separated",
        )
        row += 1

        # Button frame
        button_frame = Frame(self.dialog, bg=THEME["bg"])
        button_frame.pack(fill=X, pady=30, padx=40)

        Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg="#636e72",
            fg="white",
            activebackground="#b2bec3",
            activeforeground="black",
            font=("calibre", 12),
            width=12,
            cursor="hand2",
        ).pack(side=LEFT)

        Button(
            button_frame,
            text="Apply Filter",
            command=self._apply,
            bg=THEME["success"],
            fg="black",
            activebackground="#7ee8c0",
            activeforeground="black",
            font=("calibre", 12, "bold"),
            width=15,
            cursor="hand2",
        ).pack(side=RIGHT)

        # Keyboard shortcuts
        self.dialog.bind("<Return>", lambda e: self._apply())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())

        # Focus first field
        self.dialog.focus_set()

    def _create_field(self, parent, label_text, var, row, width=30, hint=None):
        """Create a labeled entry field."""
        frame = Frame(parent, bg=THEME["bg"])
        frame.grid(row=row, column=0, columnspan=2, sticky="w", pady=8)

        Label(
            frame, text=label_text, bg=THEME["bg"], fg=THEME["fg"], font=("calibre", 12)
        ).pack(side=LEFT)

        entry = Entry(
            frame,
            textvariable=var,
            bg=THEME["entry_bg"],
            fg=THEME["entry_fg"],
            insertbackground=THEME["entry_fg"],
            width=width,
            font=("calibre", 12),
        )
        entry.pack(side=LEFT, padx=(10, 5))

        if hint:
            Label(
                frame,
                text=f"({hint})",
                bg=THEME["bg"],
                fg="#95a5a6",
                font=("calibre", 10),
            ).pack(side=LEFT)

    def _apply(self):
        """Apply the selected criteria."""
        self.criteria = {
            "nationality": self.entry_data[0].get(),
            "age_min": self.entry_data[1].get(),
            "age_max": self.entry_data[2].get(),
            "sex": self.entry_data[3].get(),
            "experience_years": self.entry_data[4].get(),
            "skills": self.entry_data[5].get(),
            "languages": self.entry_data[6].get(),
        }
        self.applied = True
        self.dialog.destroy()


def select_data_dialog(parent) -> dict:
    """
    Show the data selection dialog.

    Args:
        parent: Parent Tkinter window

    Returns:
        Dictionary of filter criteria
    """
    dialog = SelectDataDialog(parent)
    return dialog.show()
