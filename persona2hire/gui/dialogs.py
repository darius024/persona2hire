"""Dialog windows for data selection and filtering."""

from tkinter import *


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
        self.dialog.title("Select Data")
        self.dialog.configure(bg='snow')
        
        # Center the window
        dialog_width = 900
        dialog_height = 400
        position_right = int(self.dialog.winfo_screenwidth() / 2 - dialog_width / 2)
        position_down = int(self.dialog.winfo_screenheight() / 2 - dialog_height / 2)
        self.dialog.geometry(f"900x400+{position_right}+{position_down}")
        
        # Title
        label_text = Label(self.dialog, text="Choose the criteria in which the candidates should fit.",
                           bg="lawngreen", fg="black", font=('calibre', 16))
        label_text.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        # Nationality
        nationality_var = StringVar()
        self.entry_data.append(nationality_var)
        Label(self.dialog, text="Nationalities:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.225)
        Entry(self.dialog, textvariable=nationality_var, bg="thistle", fg="black",
              width=40, font=('calibre', 14)).place(relx=0.26, rely=0.225)
        
        # Age range
        age_min_var = StringVar()
        age_max_var = StringVar()
        self.entry_data.extend([age_min_var, age_max_var])
        Label(self.dialog, text="Between:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.35)
        Entry(self.dialog, textvariable=age_min_var, bg="thistle", fg="black",
              width=5, font=('calibre', 14)).place(relx=0.23, rely=0.35)
        Label(self.dialog, text="and", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.33, rely=0.35)
        Entry(self.dialog, textvariable=age_max_var, bg="thistle", fg="black",
              width=5, font=('calibre', 14)).place(relx=0.41, rely=0.35)
        Label(self.dialog, text="years", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.51, rely=0.35)
        
        # Sex
        sex_var = StringVar()
        self.entry_data.append(sex_var)
        Label(self.dialog, text="Sex:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.475)
        Entry(self.dialog, textvariable=sex_var, bg="thistle", fg="black",
              width=5, font=('calibre', 14)).place(relx=0.18, rely=0.475)
        
        # Experience
        experience_var = StringVar()
        self.entry_data.append(experience_var)
        Label(self.dialog, text="Minimum experience:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.6)
        Entry(self.dialog, textvariable=experience_var, bg="thistle", fg="black",
              width=5, font=('calibre', 14)).place(relx=0.36, rely=0.6)
        Label(self.dialog, text="years", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.45, rely=0.6)
        
        # Skills
        skills_var = StringVar()
        self.entry_data.append(skills_var)
        Label(self.dialog, text="Skills:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.725)
        Entry(self.dialog, textvariable=skills_var, bg="thistle", fg="black",
              width=50, font=('calibre', 14)).place(relx=0.19, rely=0.725)
        
        # Languages
        languages_var = StringVar()
        self.entry_data.append(languages_var)
        Label(self.dialog, text="Languages:", bg="darkslategray", fg="white",
              font=('calibre', 14)).place(relx=0.1, rely=0.85)
        Entry(self.dialog, textvariable=languages_var, bg="thistle", fg="black",
              width=50, font=('calibre', 14)).place(relx=0.25, rely=0.85)
        
        # Apply button
        Button(self.dialog, text="Apply", command=self._apply,
               bg="royalblue", fg="white", activebackground="cornflowerblue", activeforeground="white",
               height=1, width=10, font=('calibre', 20)).place(relx=0.8, rely=0.5, anchor=CENTER)
    
    def _apply(self):
        """Apply the selected criteria."""
        self.criteria = {
            "nationality": self.entry_data[0].get(),
            "age_min": self.entry_data[1].get(),
            "age_max": self.entry_data[2].get(),
            "sex": self.entry_data[3].get(),
            "experience_years": self.entry_data[4].get(),
            "skills": self.entry_data[5].get(),
            "languages": self.entry_data[6].get()
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
