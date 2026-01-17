"""CV creation form window."""

from tkinter import *


def create_cv_form(parent, persons_list: list, listbox: Listbox, on_cv_created=None):
    """
    Create and display the CV form window.
    
    Args:
        parent: Parent Tkinter window
        persons_list: List to append new person data to
        listbox: Listbox widget to update with new CV
        on_cv_created: Optional callback when CV is created
    """
    from ..cv.writer import write_cv_file
    
    cv_window = Toplevel(parent)
    cv_window.title("New CV")
    cv_window.configure(bg='white')
    cv_window.state("zoomed")
    
    entry_data = []
    
    def upload_cv():
        """Collect form data and create CV."""
        cv_data = {
            "FirstName": entry_data[0].get(),
            "LastName": entry_data[1].get(),
            "StreetName": entry_data[2].get(),
            "HouseNumber": entry_data[3].get(),
            "City": entry_data[4].get(),
            "Country": entry_data[5].get(),
            "TelephoneNumber": entry_data[6].get(),
            "EmailAddress": entry_data[7].get(),
            "Sex": entry_data[8].get(),
            "DateOfBirth": entry_data[9].get(),
            "Nationality": entry_data[10].get(),
            "Workplace1": entry_data[11].get(),
            "Dates1": entry_data[12].get(),
            "Occupation1": entry_data[13].get(),
            "MainActivities1": entry_data[14].get(),
            "Workplace2": entry_data[15].get(),
            "Dates2": entry_data[16].get(),
            "Occupation2": entry_data[17].get(),
            "MainActivities2": entry_data[18].get(),
            "Workplace3": entry_data[19].get(),
            "Dates3": entry_data[20].get(),
            "Occupation3": entry_data[21].get(),
            "MainActivities3": entry_data[22].get(),
            "HighSchool": entry_data[23].get(),
            "College/University": entry_data[24].get(),
            "SubjectsStudied": entry_data[25].get(),
            "YearsStudied": entry_data[26].get(),
            "QualificationsAwarded": entry_data[27].get(),
            "Master1": entry_data[28].get(),
            "Master2": entry_data[29].get(),
            "CommunicationSkills": entry_data[30].get(),
            "OrganizationalManagerialSkills": entry_data[31].get(),
            "JobRelatedSkills": entry_data[32].get(),
            "ComputerSkills": entry_data[33].get(),
            "OtherSkills": entry_data[34].get(),
            "DrivingLicense": entry_data[35].get(),
            "MotherLanguage": entry_data[36].get(),
            "ModernLanguage1": entry_data[37].get(),
            "Level1": entry_data[38].get(),
            "ModernLanguage2": entry_data[39].get(),
            "Level2": entry_data[40].get(),
            "Publications": entry_data[41].get(),
            "Presentations": entry_data[42].get(),
            "Projects": entry_data[43].get(),
            "Conferences": entry_data[44].get(),
            "HonoursAndAwards": entry_data[45].get(),
            "Memberships": entry_data[46].get(),
            "ShortDescription": entry_data[47].get(),
            "Hobbies": entry_data[48].get(),
            "PersonalityTypeMB": "",
            "PersonalityTypeBF": "",
            "Score": 0
        }
        persons_list.append(cv_data)
        cv_window.destroy()
        
        # Write CV file and update listbox
        file_path = write_cv_file(cv_data)
        listbox.insert(END, file_path)
        
        if on_cv_created:
            on_cv_created(cv_data)
    
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    def make_label_entry(frame, text, row, column, entry_width):
        """Create a label and optional entry field."""
        label = Label(frame, text=text, bg="darkorange", fg="white",
                      height=1, font=('calibre', 14))
        label.grid(row=row, column=column, sticky='e', padx=10, pady=10, ipady=3)
        
        if entry_width != 0:
            name = StringVar()
            entry_data.append(name)
            entry = Entry(frame, textvariable=name, width=entry_width, font=('calibre', 12))
            entry.grid(row=row, column=column + 1, columnspan=3, sticky='w', padx=30, pady=10, ipady=3)
    
    # Frame of the whole CV window
    frame_window = Frame(cv_window, bg="indianred")
    frame_window.rowconfigure(0, weight=1)
    frame_window.columnconfigure(0, weight=1)
    frame_window.pack(expand=True, fill=BOTH)
    
    # Canvas + Scrollbar
    canvas = Canvas(frame_window, bg="firebrick")
    canvas.grid(row=0, column=0, sticky='nwes')
    scrollbar = Scrollbar(frame_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    
    # Frame in Canvas
    frame = Frame(canvas, relief="groove", bg="palegoldenrod")
    
    # Title Frame
    frame_title = Frame(frame, bg="darkgray", height=200)
    frame_title.pack(side=TOP, fill=BOTH, expand=True)
    label = Label(frame_title, text="Curriculum Vitae", bg="slategray", fg="white", height=1,
                  font=('helvetica', 26, "bold", "underline"))
    label.place(relx=0.5, rely=0.1, anchor='n')
    
    # CV Frame
    frame_cv = Frame(frame, relief="groove", bg="palegoldenrod")
    frame_cv.pack(side=TOP, fill=BOTH, expand=True)
    
    # Bottom Frame
    frame_bottom = Frame(frame, bg="orange", height=300)
    frame_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    button_upload = Button(frame_bottom, text="Upload CV", command=upload_cv,
                           bg="saddlebrown", fg="white", activebackground="sandybrown", activeforeground="white",
                           height=3, width=10, font=('calibre', 20))
    button_upload.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Configure grid columns
    for i in range(9):
        frame_cv.columnconfigure(i, weight=1)
    
    canvas.create_window((0, 0), window=frame, anchor='nw')
    
    # Create form fields
    make_label_entry(frame_cv, "First-Name : ", 0, 0, 25)
    make_label_entry(frame_cv, "Last-Name : ", 1, 0, 25)
    make_label_entry(frame_cv, "Address : ", 2, 0, 0)
    make_label_entry(frame_cv, "Street Name : ", 3, 1, 60)
    make_label_entry(frame_cv, "House Number : ", 4, 1, 10)
    make_label_entry(frame_cv, "City : ", 5, 1, 30)
    make_label_entry(frame_cv, "Country : ", 6, 1, 30)
    make_label_entry(frame_cv, "Telephone Number : ", 7, 0, 25)
    make_label_entry(frame_cv, "E-mail Address : ", 8, 0, 25)
    make_label_entry(frame_cv, "Sex : ", 9, 0, 10)
    make_label_entry(frame_cv, "Date of Birth : ", 10, 0, 20)
    make_label_entry(frame_cv, "Nationality : ", 11, 0, 20)
    make_label_entry(frame_cv, "Work Experience : ", 12, 0, 0)
    make_label_entry(frame_cv, "Workplace 1 : ", 13, 1, 40)
    make_label_entry(frame_cv, "Dates : ", 14, 2, 20)
    make_label_entry(frame_cv, "Occupation : ", 15, 2, 40)
    make_label_entry(frame_cv, "Main activities : ", 16, 2, 50)
    make_label_entry(frame_cv, "Workplace 2 : ", 17, 1, 40)
    make_label_entry(frame_cv, "Dates : ", 18, 2, 20)
    make_label_entry(frame_cv, "Occupation : ", 19, 2, 40)
    make_label_entry(frame_cv, "Main activities : ", 20, 2, 50)
    make_label_entry(frame_cv, "Workplace 3 : ", 21, 1, 40)
    make_label_entry(frame_cv, "Dates : ", 22, 2, 20)
    make_label_entry(frame_cv, "Occupation : ", 23, 2, 40)
    make_label_entry(frame_cv, "Main activities : ", 24, 2, 50)
    make_label_entry(frame_cv, "Education and Training : ", 25, 0, 0)
    make_label_entry(frame_cv, "High school : ", 26, 1, 40)
    make_label_entry(frame_cv, "College/University : ", 27, 1, 40)
    make_label_entry(frame_cv, "Subjects studied : ", 28, 1, 50)
    make_label_entry(frame_cv, "Years studied : ", 29, 1, 50)
    make_label_entry(frame_cv, "Qualifications awarded : ", 30, 1, 50)
    make_label_entry(frame_cv, "Master 1 : ", 31, 1, 50)
    make_label_entry(frame_cv, "Master 2 : ", 32, 1, 50)
    make_label_entry(frame_cv, "Personal Skills : ", 33, 0, 0)
    make_label_entry(frame_cv, "Communication skills : ", 34, 1, 60)
    make_label_entry(frame_cv, "Organizational / managerial skills : ", 35, 1, 60)
    make_label_entry(frame_cv, "Job-related skills : ", 36, 1, 60)
    make_label_entry(frame_cv, "Computer skills : ", 37, 1, 60)
    make_label_entry(frame_cv, "Other skills : ", 38, 1, 60)
    make_label_entry(frame_cv, "Driving license : ", 39, 1, 15)
    make_label_entry(frame_cv, "Languages : ", 40, 0, 0)
    make_label_entry(frame_cv, "Mother Language : ", 41, 1, 30)
    make_label_entry(frame_cv, "Other Languages : ", 42, 1, 0)
    make_label_entry(frame_cv, "Modern Language 1 : ", 43, 2, 30)
    make_label_entry(frame_cv, "Level1 : ", 44, 3, 10)
    make_label_entry(frame_cv, "Modern Language 2 : ", 45, 2, 30)
    make_label_entry(frame_cv, "Level2 : ", 46, 3, 10)
    make_label_entry(frame_cv, "Additional Information: ", 47, 0, 0)
    make_label_entry(frame_cv, "Publications : ", 48, 1, 60)
    make_label_entry(frame_cv, "Presentations : ", 49, 1, 60)
    make_label_entry(frame_cv, "Projects : ", 50, 1, 60)
    make_label_entry(frame_cv, "Conferences : ", 51, 1, 60)
    make_label_entry(frame_cv, "Honours and awards : ", 52, 1, 60)
    make_label_entry(frame_cv, "Memberships : ", 53, 1, 60)
    make_label_entry(frame_cv, "Short Description : ", 54, 0, 100)
    make_label_entry(frame_cv, "Hobbies : ", 55, 0, 100)
    
    frame.update_idletasks()
    canvas.configure(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))
    canvas.bind("<Enter>", bind_to_mousewheel)
    canvas.bind("<Leave>", unbind_from_mousewheel)
