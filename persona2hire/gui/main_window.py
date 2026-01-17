"""Main application window."""

from tkinter import *
from tkinter.filedialog import askopenfilename

from ..data.job_sectors import JobSectors
from ..cv.parser import read_cv_file
from .cv_form import create_cv_form
from .dialogs import select_data_dialog
from .results import show_results, show_jobs, show_personality


class MainWindow:
    """Main application window class."""
    
    def __init__(self):
        self.window = Tk()
        self.window.title("Persona2Hire - CV & Personality Analysis")
        self.window.configure(bg='black')
        self.window.state("zoomed")
        
        self.persons = []
        self.filter_criteria = {}
        self.job_var = StringVar()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up all UI components."""
        self._create_job_selector()
        self._create_buttons()
        self._create_file_list()
        self._create_action_buttons()
    
    def _create_job_selector(self):
        """Create job sector selector."""
        # Label
        Label(self.window, text="Job applied:", bg="black", fg="white",
              height=1, width=30, font=('calibre', 16)).place(relx=0.35, rely=0.1, anchor=S)
        
        # Entry field
        self.job_entry = Entry(self.window, textvariable=self.job_var, width=27, font=('calibre', 16))
        self.job_entry.place(relx=0.5, rely=0.1, anchor=S)
        
        # Job list dropdown
        self.job_listbox = Listbox(self.window, height=10, width=37, selectmode="extended",
                                   fg="black", font=('calibre', 12))
        for sector in JobSectors:
            self.job_listbox.insert(END, sector)
        
        # Bind events for dropdown behavior
        self.job_entry.bind('<Enter>', self._show_job_list)
        self.job_entry.bind('<Leave>', self._hide_job_list)
        self.job_listbox.bind('<Enter>', self._show_job_list)
        self.job_listbox.bind('<Leave>', self._hide_job_list)
        self.job_listbox.bind('<<ListboxSelect>>', self._on_job_select)
        
        # Select Data button
        Button(self.window, text="Select Data", command=self._select_data,
               bg="indianred", fg="white", activebackground="lightcoral", activeforeground="white",
               height=1, width=12, font=('calibre', 18)).place(relx=0.7, rely=0.1, anchor=CENTER)
    
    def _create_buttons(self):
        """Create main action buttons."""
        # Make CV button
        Button(self.window, text="Make CV", command=self._make_cv,
               bg="orange", fg="white", activebackground="wheat", activeforeground="white",
               height=2, width=15, font=('calibre', 20)).place(relx=0.7, rely=0.22, anchor=CENTER)
        
        # Choose File button
        Button(self.window, text="Choose File", command=self._open_file,
               bg="purple", fg="white", activebackground="plum", activeforeground="white",
               height=2, width=10, font=('calibre', 20)).place(relx=0.5, rely=0.4, anchor=CENTER)
    
    def _create_file_list(self):
        """Create the file list with scrollbar."""
        frame = Frame(self.window, relief="raised", bg="darkgray", width=600, height=300,
                      padx=10, borderwidth=1)
        frame.place(relx=0.5, rely=0.7, anchor=CENTER)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.listbox = Listbox(frame, height=15, width=60, selectmode="extended",
                               fg="dodgerblue", font=('calibre', 12))
        scrollbar = Scrollbar(frame, orient='vertical', command=self.listbox.yview)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.grid(column=0, row=0, sticky='nwes')
        scrollbar.grid(column=1, row=0, sticky='ns')
        
        # Analyze Data button
        Button(self.window, text="Analyze data", command=self._analyze_data,
               bg="teal", fg="white", activebackground="paleturquoise", activeforeground="white",
               height=3, width=10, font=('calibre', 20)).place(relx=0.8, rely=0.7, anchor=CENTER)
    
    def _create_action_buttons(self):
        """Create bottom action buttons."""
        # Remove button
        Button(self.window, text="Remove", command=self._remove_file,
               bg="sienna", fg="white", activebackground="rosybrown", activeforeground="white",
               height=1, width=10, font=('calibre', 18)).place(relx=0.36, rely=0.95, anchor=CENTER)
        
        # Show Jobs button
        Button(self.window, text="Show Jobs", command=self._show_jobs,
               bg="darkgoldenrod", fg="white", activebackground="gold", activeforeground="white",
               height=1, width=10, font=('calibre', 18)).place(relx=0.48, rely=0.95, anchor=CENTER)
        
        # Show Personality button
        Button(self.window, text="Show Personality", command=self._show_personality,
               bg="paleturquoise", fg="black", activebackground="azure", activeforeground="black",
               height=1, width=15, font=('calibre', 18)).place(relx=0.62, rely=0.95, anchor=CENTER)
    
    def _show_job_list(self, event=None):
        """Show the job sector dropdown."""
        self.job_listbox.place(relx=0.5, rely=0.1, anchor=N)
    
    def _hide_job_list(self, event=None):
        """Hide the job sector dropdown."""
        self.job_listbox.place_forget()
    
    def _on_job_select(self, event=None):
        """Handle job selection from dropdown."""
        selection = self.job_listbox.curselection()
        if selection:
            sector = self.job_listbox.get(selection)
            self.job_entry.delete(0, END)
            self.job_entry.insert(0, sector)
            self._hide_job_list()
    
    def _select_data(self):
        """Open the data selection dialog."""
        self.filter_criteria = select_data_dialog(self.window)
    
    def _make_cv(self):
        """Open the CV creation form."""
        create_cv_form(self.window, self.persons, self.listbox)
    
    def _open_file(self):
        """Open a file dialog to select a CV file."""
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            person = read_cv_file(filepath)
            self.persons.append(person)
            self.listbox.insert(END, filepath)
    
    def _remove_file(self):
        """Remove selected file from the list."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.persons.pop(index)
            self.listbox.delete(index)
    
    def _analyze_data(self):
        """Analyze all loaded CVs for the selected job sector."""
        selection = self.job_listbox.curselection()
        if selection:
            sector = self.job_listbox.get(selection)
        else:
            sector = self.job_var.get()
        
        if sector and self.persons:
            show_results(self.window, self.persons, sector)
    
    def _show_jobs(self):
        """Show suitable jobs for the selected person."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            show_jobs(self.window, self.persons[index])
    
    def _show_personality(self):
        """Show personality analysis for the selected person."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            show_personality(self.window, self.persons[index])
    
    def run(self):
        """Start the main event loop."""
        self.window.mainloop()


def create_main_window():
    """Create and return the main application window."""
    return MainWindow()
