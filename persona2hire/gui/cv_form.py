"""CV creation form window."""

from tkinter import *
from tkinter import messagebox
from typing import Callable, Optional


def create_cv_form(
    parent,
    persons_list: list,
    listbox: Listbox,
    on_cv_created: Optional[Callable] = None,
):
    """
    Create and display the CV form window.

    Args:
        parent: Parent Tkinter window
        persons_list: List to append new person data to
        listbox: Listbox widget to update with new CV
        on_cv_created: Optional callback when CV is created (receives cv_data, file_path)
    """
    from ..cv.writer import write_cv_file, create_empty_cv
    from ..cv.parser import validate_cv_data, get_cv_summary

    cv_window = Toplevel(parent)
    cv_window.title("Create New CV")
    cv_window.configure(bg="#f5f5f5")

    # Try to maximize window
    try:
        cv_window.state("zoomed")
    except TclError:
        cv_window.attributes("-zoomed", True)

    entry_widgets = {}  # Store entry widgets by field name

    def validate_and_upload():
        """Validate form data and create CV."""
        # Collect form data
        cv_data = create_empty_cv()

        for field_name, widget in entry_widgets.items():
            value = widget.get().strip()
            cv_data[field_name] = value

        # Validate
        is_valid, errors = validate_cv_data(cv_data)

        if not is_valid:
            messagebox.showerror(
                "Validation Error",
                "Please fix the following issues:\n\n" + "\n".join(errors),
            )
            return

        # Additional check: at least a name is required
        if not cv_data.get("FirstName") and not cv_data.get("LastName"):
            messagebox.showerror(
                "Name Required", "Please enter at least a first name or last name."
            )
            return

        try:
            # Write CV file
            file_path = write_cv_file(cv_data)

            # Add to persons list
            persons_list.append(cv_data)

            # Update listbox with summary
            summary = get_cv_summary(cv_data)
            listbox.insert(END, summary)

            # Call callback if provided
            if on_cv_created:
                on_cv_created(cv_data, file_path)

            # Show success message
            messagebox.showinfo(
                "CV Created", f"CV saved successfully!\n\nFile: {file_path}"
            )

            cv_window.destroy()

        except OSError as e:
            messagebox.showerror("File Error", f"Could not save CV file:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    def create_section_header(frame, text, row):
        """Create a section header label."""
        Label(
            frame,
            text=text,
            bg="#4a90d9",
            fg="white",
            font=("calibre", 14, "bold"),
            padx=10,
            pady=5,
        ).grid(row=row, column=0, columnspan=4, sticky="ew", pady=(15, 5))

    def create_field(
        frame, label_text, field_name, row, col=0, width=40, required=False
    ):
        """Create a label and entry field pair."""
        # Label
        label = label_text
        if required:
            label += " *"

        Label(
            frame, text=label, bg="#f0f0f0", fg="#333", font=("calibre", 11), anchor="e"
        ).grid(row=row, column=col, sticky="e", padx=(20, 10), pady=5)

        # Entry
        entry_var = StringVar()
        entry = Entry(
            frame,
            textvariable=entry_var,
            width=width,
            font=("calibre", 11),
            bg="white",
            fg="black",
        )
        entry.grid(row=row, column=col + 1, sticky="w", padx=10, pady=5)

        entry_widgets[field_name] = entry_var
        return entry

    # Main container frame
    frame_window = Frame(cv_window, bg="#f5f5f5")
    frame_window.pack(expand=True, fill=BOTH)
    frame_window.rowconfigure(0, weight=1)
    frame_window.columnconfigure(0, weight=1)

    # Canvas + Scrollbar
    canvas = Canvas(frame_window, bg="#f5f5f5", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = Scrollbar(frame_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Scrollable frame
    scroll_frame = Frame(canvas, bg="#f5f5f5")

    # Title
    title_frame = Frame(scroll_frame, bg="#2c3e50", height=80)
    title_frame.pack(fill=X)
    Label(
        title_frame,
        text="Create New Curriculum Vitae",
        bg="#2c3e50",
        fg="white",
        font=("Helvetica", 24, "bold"),
        pady=20,
    ).pack()

    # Form frame
    form_frame = Frame(scroll_frame, bg="#f0f0f0", padx=30, pady=20)
    form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Configure grid
    for i in range(4):
        form_frame.columnconfigure(i, weight=1)

    row = 0

    # Personal Information Section
    create_section_header(form_frame, "Personal Information", row)
    row += 1

    create_field(form_frame, "First Name:", "FirstName", row, 0, 30, required=True)
    create_field(form_frame, "Last Name:", "LastName", row, 2, 30, required=True)
    row += 1

    create_field(form_frame, "Street Name:", "StreetName", row, 0, 50)
    create_field(form_frame, "House Number:", "HouseNumber", row, 2, 15)
    row += 1

    create_field(form_frame, "City:", "City", row, 0, 30)
    create_field(form_frame, "Country:", "Country", row, 2, 30)
    row += 1

    create_field(form_frame, "Telephone:", "TelephoneNumber", row, 0, 25)
    create_field(form_frame, "Email:", "EmailAddress", row, 2, 35)
    row += 1

    create_field(form_frame, "Sex:", "Sex", row, 0, 10)
    create_field(form_frame, "Date of Birth:", "DateOfBirth", row, 2, 15)
    row += 1

    create_field(form_frame, "Nationality:", "Nationality", row, 0, 25)
    row += 1

    # Work Experience Section
    create_section_header(form_frame, "Work Experience", row)
    row += 1

    for i in [1, 2, 3]:
        Label(
            form_frame,
            text=f"Position {i}",
            bg="#f0f0f0",
            fg="#4a90d9",
            font=("calibre", 11, "bold"),
        ).grid(row=row, column=0, sticky="w", padx=20, pady=(10, 0))
        row += 1

        create_field(form_frame, "Company:", f"Workplace{i}", row, 0, 40)
        create_field(
            form_frame, "Dates (DD.MM.YYYY - DD.MM.YYYY):", f"Dates{i}", row, 2, 30
        )
        row += 1

        create_field(form_frame, "Job Title:", f"Occupation{i}", row, 0, 40)
        row += 1

        create_field(form_frame, "Main Activities:", f"MainActivities{i}", row, 0, 80)
        row += 1

    # Education Section
    create_section_header(form_frame, "Education & Training", row)
    row += 1

    create_field(form_frame, "High School:", "HighSchool", row, 0, 50)
    row += 1

    create_field(form_frame, "University/College:", "College/University", row, 0, 50)
    row += 1

    create_field(form_frame, "Subjects Studied:", "SubjectsStudied", row, 0, 60)
    create_field(form_frame, "Years:", "YearsStudied", row, 2, 5)
    row += 1

    create_field(form_frame, "Qualifications:", "QualificationsAwarded", row, 0, 60)
    row += 1

    create_field(form_frame, "Master's Degree 1:", "Master1", row, 0, 50)
    row += 1

    create_field(form_frame, "Master's Degree 2:", "Master2", row, 0, 50)
    row += 1

    # Skills Section
    create_section_header(form_frame, "Skills", row)
    row += 1

    create_field(form_frame, "Communication Skills:", "CommunicationSkills", row, 0, 80)
    row += 1

    create_field(
        form_frame,
        "Organizational/Managerial:",
        "OrganizationalManagerialSkills",
        row,
        0,
        80,
    )
    row += 1

    create_field(form_frame, "Job-Related Skills:", "JobRelatedSkills", row, 0, 80)
    row += 1

    create_field(form_frame, "Computer Skills:", "ComputerSkills", row, 0, 80)
    row += 1

    create_field(form_frame, "Other Skills:", "OtherSkills", row, 0, 80)
    row += 1

    create_field(form_frame, "Driving License:", "DrivingLicense", row, 0, 15)
    row += 1

    # Languages Section
    create_section_header(form_frame, "Languages", row)
    row += 1

    create_field(form_frame, "Mother Language:", "MotherLanguage", row, 0, 30)
    row += 1

    create_field(form_frame, "Language 1:", "ModernLanguage1", row, 0, 25)
    create_field(form_frame, "Level:", "Level1", row, 2, 15)
    row += 1

    create_field(form_frame, "Language 2:", "ModernLanguage2", row, 0, 25)
    create_field(form_frame, "Level:", "Level2", row, 2, 15)
    row += 1

    # Additional Information Section
    create_section_header(form_frame, "Additional Information", row)
    row += 1

    create_field(form_frame, "Publications:", "Publications", row, 0, 80)
    row += 1

    create_field(form_frame, "Presentations:", "Presentations", row, 0, 80)
    row += 1

    create_field(form_frame, "Projects:", "Projects", row, 0, 80)
    row += 1

    create_field(form_frame, "Conferences:", "Conferences", row, 0, 80)
    row += 1

    create_field(form_frame, "Honours & Awards:", "HonoursAndAwards", row, 0, 80)
    row += 1

    create_field(form_frame, "Memberships:", "Memberships", row, 0, 80)
    row += 1

    # Personality Section
    create_section_header(form_frame, "About You", row)
    row += 1

    Label(
        form_frame,
        text="Short Description (personality traits, work style):",
        bg="#f0f0f0",
        fg="#333",
        font=("calibre", 11),
    ).grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 5))
    row += 1

    desc_var = StringVar()
    entry_widgets["ShortDescription"] = desc_var
    Entry(
        form_frame, textvariable=desc_var, width=100, font=("calibre", 11), bg="white"
    ).grid(row=row, column=0, columnspan=4, sticky="w", padx=20, pady=5)
    row += 1

    Label(
        form_frame,
        text="Hobbies & Interests (comma-separated):",
        bg="#f0f0f0",
        fg="#333",
        font=("calibre", 11),
    ).grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 5))
    row += 1

    hobbies_var = StringVar()
    entry_widgets["Hobbies"] = hobbies_var
    Entry(
        form_frame,
        textvariable=hobbies_var,
        width=100,
        font=("calibre", 11),
        bg="white",
    ).grid(row=row, column=0, columnspan=4, sticky="w", padx=20, pady=5)
    row += 1

    # Submit Button
    button_frame = Frame(scroll_frame, bg="#2c3e50", height=100)
    button_frame.pack(fill=X, pady=20)

    Button(
        button_frame,
        text="Create CV",
        command=validate_and_upload,
        bg="#27ae60",
        fg="white",
        activebackground="#2ecc71",
        activeforeground="white",
        font=("calibre", 16, "bold"),
        padx=40,
        pady=10,
    ).pack(pady=30)

    Label(
        button_frame,
        text="* Required fields",
        bg="#2c3e50",
        fg="#aaa",
        font=("calibre", 10),
    ).pack()

    # Configure canvas
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.update_idletasks()
    canvas.configure(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))

    # Bind mousewheel
    canvas.bind("<Enter>", bind_to_mousewheel)
    canvas.bind("<Leave>", unbind_from_mousewheel)
