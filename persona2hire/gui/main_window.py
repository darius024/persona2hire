"""Main application window."""

import csv
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename

from ..data.job_sectors import JobSectors
from ..cv.parser import read_cv_file, validate_cv_data, get_cv_summary
from ..analysis.job_analyzer import filter_candidates
from .cv_form import create_cv_form
from .dialogs import select_data_dialog
from .results import show_results, show_jobs, show_personality


class ToolTip:
    """Simple tooltip class for Tkinter widgets."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        """Show the tooltip."""
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(
            self.tooltip,
            text=self.text,
            bg="#333",
            fg="white",
            relief="solid",
            borderwidth=1,
            font=("calibre", 10),
            padx=6,
            pady=3,
        )
        label.pack()

    def hide(self, event=None):
        """Hide the tooltip."""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class MainWindow:
    """Main application window class."""

    def __init__(self):
        self.window = Tk()
        self.window.title("Persona2Hire - CV & Personality Analysis")
        self.window.configure(bg="#1a1a2e")

        # Try to maximize window (works differently on different OS)
        try:
            self.window.state("zoomed")
        except TclError:
            # Fallback for Linux/Mac
            self.window.attributes("-zoomed", True)

        self.persons = []
        self.file_paths = []  # Keep track of file paths
        self.filter_criteria = {}
        self.job_var = StringVar()

        self._setup_ui()

    def _setup_ui(self):
        """Set up all UI components."""
        self._create_header()
        self._create_job_selector()
        self._create_buttons()
        self._create_file_list()
        self._create_action_buttons()
        self._setup_keyboard_shortcuts()

    def _setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts for common actions."""
        # Ctrl+O: Open file
        self.window.bind("<Control-o>", lambda e: self._open_file())
        self.window.bind("<Control-O>", lambda e: self._open_file())

        # Ctrl+N: New CV
        self.window.bind("<Control-n>", lambda e: self._make_cv())
        self.window.bind("<Control-N>", lambda e: self._make_cv())

        # Ctrl+Enter: Analyze
        self.window.bind("<Control-Return>", lambda e: self._analyze_data())

        # Ctrl+E: Export
        self.window.bind("<Control-e>", lambda e: self._export_results())
        self.window.bind("<Control-E>", lambda e: self._export_results())

        # Delete: Remove selected
        self.window.bind("<Delete>", lambda e: self._remove_file())
        self.window.bind("<BackSpace>", lambda e: self._remove_file())

        # Escape: Clear job selector
        self.window.bind("<Escape>", lambda e: self._hide_job_list())

    def _create_header(self):
        """Create the header section."""
        Label(
            self.window,
            text="Persona2Hire",
            bg="#1a1a2e",
            fg="#e94560",
            font=("Helvetica", 32, "bold"),
        ).place(relx=0.5, rely=0.03, anchor=CENTER)

        Label(
            self.window,
            text="CV & Personality Analysis Tool",
            bg="#1a1a2e",
            fg="#c3c3c3",
            font=("Helvetica", 14),
        ).place(relx=0.5, rely=0.07, anchor=CENTER)

    def _create_job_selector(self):
        """Create job sector selector."""
        # Label
        Label(
            self.window,
            text="Job Sector:",
            bg="#1a1a2e",
            fg="white",
            font=("calibre", 14),
        ).place(relx=0.32, rely=0.13, anchor=E)

        # Entry field
        self.job_entry = Entry(
            self.window,
            textvariable=self.job_var,
            width=30,
            font=("calibre", 14),
            bg="#2a2a3e",
            fg="white",
            insertbackground="white",
        )
        self.job_entry.place(relx=0.5, rely=0.13, anchor=CENTER)

        # Job list dropdown
        self.job_listbox = Listbox(
            self.window,
            height=10,
            width=35,
            selectmode="single",
            bg="#2a2a3e",
            fg="white",
            font=("calibre", 11),
            selectbackground="#e94560",
        )
        for sector in sorted(JobSectors.keys()):
            self.job_listbox.insert(END, sector)

        # Bind events for dropdown behavior
        self.job_entry.bind("<FocusIn>", self._show_job_list)
        self.job_entry.bind("<KeyRelease>", self._filter_job_list)
        self.job_listbox.bind("<<ListboxSelect>>", self._on_job_select)

        # Hide dropdown when clicking elsewhere
        self.window.bind("<Button-1>", self._on_window_click)

        # Select Data button
        Button(
            self.window,
            text="Filter Criteria",
            command=self._select_data,
            bg="#e94560",
            fg="white",
            activebackground="#ff6b6b",
            activeforeground="white",
            font=("calibre", 12),
            padx=15,
        ).place(relx=0.72, rely=0.13, anchor=CENTER)

    def _create_buttons(self):
        """Create main action buttons."""
        # Make CV button
        btn_new = Button(
            self.window,
            text="Create New CV",
            command=self._make_cv,
            bg="#4ecca3",
            fg="black",
            activebackground="#7ee8c0",
            activeforeground="black",
            height=2,
            width=15,
            font=("calibre", 14, "bold"),
        )
        btn_new.place(relx=0.25, rely=0.24, anchor=CENTER)
        ToolTip(btn_new, "Create a new CV (Ctrl+N)")

        # Choose File button
        btn_load = Button(
            self.window,
            text="Load CV File(s)",
            command=self._open_file,
            bg="#6c5ce7",
            fg="white",
            activebackground="#a29bfe",
            activeforeground="white",
            height=2,
            width=15,
            font=("calibre", 14, "bold"),
        )
        btn_load.place(relx=0.5, rely=0.24, anchor=CENTER)
        ToolTip(btn_load, "Load existing CV files (Ctrl+O)")

        # Analyze Data button
        btn_analyze = Button(
            self.window,
            text="Analyze All",
            command=self._analyze_data,
            bg="#00b894",
            fg="white",
            activebackground="#55efc4",
            activeforeground="black",
            height=2,
            width=15,
            font=("calibre", 14, "bold"),
        )
        btn_analyze.place(relx=0.75, rely=0.24, anchor=CENTER)
        ToolTip(btn_analyze, "Analyze all CVs for selected sector (Ctrl+Enter)")

    def _create_file_list(self):
        """Create the file list with scrollbar."""
        # Frame for the list
        frame = Frame(self.window, bg="#2a2a3e", padx=10, pady=10)
        frame.place(relx=0.5, rely=0.55, anchor=CENTER, width=800, height=350)

        # Label
        Label(
            frame,
            text="Loaded CVs",
            bg="#2a2a3e",
            fg="white",
            font=("calibre", 14, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Listbox with scrollbar
        list_frame = Frame(frame, bg="#2a2a3e")
        list_frame.pack(fill=BOTH, expand=True)

        self.listbox = Listbox(
            list_frame,
            height=12,
            selectmode="extended",
            bg="#1a1a2e",
            fg="#4ecca3",
            font=("calibre", 11),
            selectbackground="#e94560",
            activestyle="none",
        )
        scrollbar = Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)

        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Status label
        self.status_label = Label(
            frame,
            text="No CVs loaded",
            bg="#2a2a3e",
            fg="#c3c3c3",
            font=("calibre", 10),
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

    def _create_action_buttons(self):
        """Create bottom action buttons."""
        button_frame = Frame(self.window, bg="#1a1a2e")
        button_frame.place(relx=0.5, rely=0.88, anchor=CENTER)

        # Remove button
        Button(
            button_frame,
            text="Remove Selected",
            command=self._remove_file,
            bg="#d63031",
            fg="white",
            activebackground="#ff7675",
            activeforeground="white",
            font=("calibre", 12),
            padx=15,
        ).pack(side=LEFT, padx=10)

        # Show Jobs button
        Button(
            button_frame,
            text="Show Jobs Match",
            command=self._show_jobs,
            bg="#fdcb6e",
            fg="black",
            activebackground="#ffeaa7",
            activeforeground="black",
            font=("calibre", 12),
            padx=15,
        ).pack(side=LEFT, padx=10)

        # Show Personality button
        Button(
            button_frame,
            text="Show Personality",
            command=self._show_personality,
            bg="#74b9ff",
            fg="black",
            activebackground="#a4d4ff",
            activeforeground="black",
            font=("calibre", 12),
            padx=15,
        ).pack(side=LEFT, padx=10)

        # Export button
        Button(
            button_frame,
            text="Export Results",
            command=self._export_results,
            bg="#00cec9",
            fg="black",
            activebackground="#81ecec",
            activeforeground="black",
            font=("calibre", 12),
            padx=15,
        ).pack(side=LEFT, padx=10)

        # Clear All button
        Button(
            button_frame,
            text="Clear All",
            command=self._clear_all,
            bg="#636e72",
            fg="white",
            activebackground="#b2bec3",
            activeforeground="black",
            font=("calibre", 12),
            padx=15,
        ).pack(side=LEFT, padx=10)

    def _show_job_list(self, event=None):
        """Show the job sector dropdown."""
        self.job_listbox.place(relx=0.5, rely=0.13, anchor=N, y=25)

    def _hide_job_list(self, event=None):
        """Hide the job sector dropdown."""
        self.job_listbox.place_forget()

    def _filter_job_list(self, event=None):
        """Filter job list based on entry text."""
        search_term = self.job_var.get().lower()
        self.job_listbox.delete(0, END)

        for sector in sorted(JobSectors.keys()):
            if search_term in sector.lower():
                self.job_listbox.insert(END, sector)

        if self.job_listbox.size() > 0:
            self._show_job_list()
        else:
            self._hide_job_list()

    def _on_job_select(self, event=None):
        """Handle job selection from dropdown."""
        selection = self.job_listbox.curselection()
        if selection:
            sector = self.job_listbox.get(selection)
            self.job_var.set(sector)
            self._hide_job_list()

    def _on_window_click(self, event):
        """Handle clicks outside the job listbox."""
        # Check if click is outside the listbox
        widget = event.widget
        if widget != self.job_listbox and widget != self.job_entry:
            self._hide_job_list()

    def _select_data(self):
        """Open the data selection dialog."""
        self.filter_criteria = select_data_dialog(self.window)

    def _make_cv(self):
        """Open the CV creation form."""
        create_cv_form(self.window, self.persons, self.listbox, self._on_cv_created)

    def _on_cv_created(self, cv_data: dict, file_path: str):
        """Callback when a new CV is created."""
        self.file_paths.append(file_path)
        self._update_status()

    def _open_file(self):
        """Open a file dialog to select CV file(s)."""
        filepaths = askopenfilenames(
            title="Select CV File(s)",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )

        if not filepaths:
            return

        loaded_count = 0
        errors = []

        for filepath in filepaths:
            try:
                person = read_cv_file(filepath)

                # Validate the CV data
                is_valid, validation_errors = validate_cv_data(person)
                if not is_valid:
                    errors.append(f"{filepath}: {', '.join(validation_errors)}")
                    continue

                self.persons.append(person)
                self.file_paths.append(filepath)

                # Show summary in listbox
                summary = get_cv_summary(person)
                self.listbox.insert(END, summary)
                loaded_count += 1

            except FileNotFoundError:
                errors.append(f"{filepath}: File not found")
            except UnicodeDecodeError:
                errors.append(f"{filepath}: Unable to read file encoding")
            except Exception as e:
                errors.append(f"{filepath}: {str(e)}")

        self._update_status()

        if errors:
            error_msg = "\n".join(errors[:5])  # Show max 5 errors
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more errors"
            messagebox.showwarning(
                "Some Files Could Not Be Loaded",
                f"Loaded {loaded_count} file(s).\n\nErrors:\n{error_msg}",
            )

    def _remove_file(self):
        """Remove selected file(s) from the list."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a CV to remove.")
            return

        # Remove in reverse order to maintain correct indices
        for index in reversed(selection):
            if 0 <= index < len(self.persons):
                self.persons.pop(index)
                self.file_paths.pop(index)
                self.listbox.delete(index)

        self._update_status()

    def _clear_all(self):
        """Clear all loaded CVs."""
        if not self.persons:
            return

        if messagebox.askyesno("Confirm", "Remove all loaded CVs?"):
            self.persons.clear()
            self.file_paths.clear()
            self.listbox.delete(0, END)
            self._update_status()

    def _analyze_data(self):
        """Analyze all loaded CVs for the selected job sector."""
        if not self.persons:
            messagebox.showinfo("No CVs", "Please load some CV files first.")
            return

        sector = self.job_var.get().strip()

        if not sector:
            messagebox.showinfo("No Sector", "Please select or enter a job sector.")
            return

        if sector not in JobSectors:
            # Try to find a matching sector
            matches = [s for s in JobSectors if sector.lower() in s.lower()]
            if matches:
                sector = matches[0]
                self.job_var.set(sector)
            else:
                messagebox.showwarning(
                    "Invalid Sector",
                    f"'{sector}' is not a valid job sector.\nPlease select from the dropdown.",
                )
                return

        # Apply filter criteria if set
        persons_to_analyze = self.persons
        if self.filter_criteria:
            persons_to_analyze = filter_candidates(self.persons, self.filter_criteria)
            if not persons_to_analyze:
                messagebox.showinfo(
                    "No Matches",
                    "No candidates match the filter criteria.\n"
                    "Try adjusting your filters.",
                )
                return
            if len(persons_to_analyze) < len(self.persons):
                messagebox.showinfo(
                    "Filtered",
                    f"Analyzing {len(persons_to_analyze)} of {len(self.persons)} "
                    "candidates that match your filter criteria.",
                )

        show_results(self.window, persons_to_analyze, sector)

    def _show_jobs(self):
        """Show suitable jobs for the selected person."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a CV first.")
            return

        index = selection[0]
        if 0 <= index < len(self.persons):
            show_jobs(self.window, self.persons[index])

    def _show_personality(self):
        """Show personality analysis for the selected person."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a CV first.")
            return

        index = selection[0]
        if 0 <= index < len(self.persons):
            show_personality(self.window, self.persons[index])

    def _update_status(self):
        """Update the status label."""
        count = len(self.persons)
        if count == 0:
            self.status_label.config(text="No CVs loaded")
        elif count == 1:
            self.status_label.config(text="1 CV loaded")
        else:
            self.status_label.config(text=f"{count} CVs loaded")

    def _export_results(self):
        """Export analysis results to a CSV file."""
        from ..analysis.job_analyzer import analyze_job, get_score_breakdown
        from ..analysis.personality_analyzer import analyze_personality

        if not self.persons:
            messagebox.showinfo("No CVs", "Please load some CV files first.")
            return

        sector = self.job_var.get().strip()
        if not sector or sector not in JobSectors:
            messagebox.showinfo(
                "Select Sector",
                "Please select a valid job sector before exporting.",
            )
            return

        # Ask for save location
        filepath = asksaveasfilename(
            title="Export Results",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            initialfile=f"results_{sector}.csv",
        )

        if not filepath:
            return

        try:
            # Analyze and export
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Header row
                writer.writerow(
                    [
                        "Rank",
                        "First Name",
                        "Last Name",
                        "Email",
                        "Total Score",
                        "Education Score",
                        "Work Experience Score",
                        "Skills Score",
                        "Languages Score",
                        "Soft Skills Score",
                        "Additional Score",
                        "Personality Type",
                        "Nationality",
                    ]
                )

                # Calculate scores and sort
                results = []
                for person in self.persons:
                    score = analyze_job(person, sector)
                    personality = analyze_personality(person)
                    breakdown = get_score_breakdown(person, sector)
                    results.append((person, score, personality, breakdown))

                results.sort(key=lambda x: x[1], reverse=True)

                # Write data rows
                for rank, (person, score, personality, breakdown) in enumerate(
                    results, 1
                ):
                    writer.writerow(
                        [
                            rank,
                            person.get("FirstName", ""),
                            person.get("LastName", ""),
                            person.get("EmailAddress", ""),
                            f"{score:.1f}",
                            f"{breakdown.get('education', 0):.1f}",
                            f"{breakdown.get('work_experience', 0):.1f}",
                            f"{breakdown.get('skills', 0):.1f}",
                            f"{breakdown.get('languages', 0):.1f}",
                            f"{breakdown.get('soft_skills', 0):.1f}",
                            f"{breakdown.get('additional', 0):.1f}",
                            personality,
                            person.get("Nationality", ""),
                        ]
                    )

            messagebox.showinfo(
                "Export Complete",
                f"Results exported successfully!\n\nFile: {filepath}",
            )

        except OSError as e:
            messagebox.showerror("Export Error", f"Could not save file:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def run(self):
        """Start the main event loop."""
        self.window.mainloop()


def create_main_window():
    """Create and return the main application window."""
    return MainWindow()
