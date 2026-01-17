"""Result display windows for jobs and personality analysis."""

from tkinter import *
from tkinter import ttk
import webbrowser

from ..analysis.job_analyzer import analyze_jobs
from ..analysis.personality_analyzer import analyze_personality
from ..data.personality import PersonalityTypes


def show_results(parent, persons_list: list, selected_sector: str):
    """
    Show ranked list of candidates for a job sector.
    
    Args:
        parent: Parent Tkinter window
        persons_list: List of person dictionaries
        selected_sector: Job sector to analyze for
    """
    from ..analysis.job_analyzer import analyze_job
    
    results_window = Toplevel(parent)
    results_window.title("Results of the Analysis")
    results_window.configure(bg="dimgray")
    results_window.state("zoomed")
    
    # Calculate scores for each person
    for person in persons_list:
        analyze_personality(person)
        person["PersonalityTypeMB"] = analyze_personality(person)
        person["Score"] = analyze_job(person, selected_sector)
    
    # Sort by score
    sorted_list = sorted(persons_list, key=lambda x: x.get("Score", 0), reverse=True)
    
    # Title
    Label(results_window, text="List of Candidates", bg="silver", fg="white",
          font=('calibre', 26, 'bold')).place(relx=0.5, rely=0.1, anchor=S)
    
    # Create treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('calibre', 16, 'bold'))
    style.configure("Treeview", font=('calibre', 14))
    
    treeview = ttk.Treeview(results_window, columns=("candidate", "points"),
                            show='headings', height=20, selectmode="extended")
    treeview.place(relx=0.28, rely=0.3)
    treeview.heading("candidate", text="Candidate Name")
    treeview.heading("points", text="Points")
    treeview.column("# 1", anchor=CENTER, width=400, stretch=NO)
    treeview.column("# 2", anchor=CENTER, width=400, stretch=NO)
    
    # Populate treeview (show top 5)
    for i, person in enumerate(sorted_list[:5], 1):
        name = f"{i}. {person.get('FirstName', '')} {person.get('LastName', '')}"
        treeview.insert('', END, values=(name, int(person.get("Score", 0))))


def show_jobs(parent, person: dict):
    """
    Show suitable jobs for a person.
    
    Args:
        parent: Parent Tkinter window
        person: Person dictionary to analyze
    """
    jobs_window = Toplevel(parent)
    jobs_window.title("Suitable Jobs")
    jobs_window.configure(bg="dimgray")
    jobs_window.state("zoomed")
    
    job_list = analyze_jobs(person)
    
    # Title
    Label(jobs_window, text="Jobs Analysis", bg="silver", fg="white",
          font=('calibre', 26, 'bold')).place(relx=0.5, rely=0.1, anchor=S)
    
    # Subtitle
    Label(jobs_window, text="List of suitable jobs:", bg="gainsboro", fg="black",
          font=('calibre', 18)).place(relx=0.28, rely=0.26)
    
    # Create treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Calibri', 16, 'bold'))
    style.configure("Treeview", font=('Calibri', 14))
    
    treeview = ttk.Treeview(jobs_window, columns=("job", "score"),
                            show='headings', height=20, selectmode="extended")
    treeview.place(relx=0.28, rely=0.3)
    treeview.heading("job", text="Job")
    treeview.heading("score", text="Score")
    treeview.column("# 1", anchor=CENTER, width=400, stretch=YES)
    treeview.column("# 2", anchor=CENTER, width=400, stretch=YES)
    
    # Populate treeview (show top 3)
    for i, (sector, score) in enumerate(job_list[:3], 1):
        treeview.insert('', END, values=(f"{i}. {sector}", int(score)))


def show_personality(parent, person: dict):
    """
    Show personality analysis for a person.
    
    Args:
        parent: Parent Tkinter window
        person: Person dictionary to analyze
    """
    personality_window = Toplevel(parent)
    personality_window.title("Personality Type")
    personality_window.configure(bg='midnightblue')
    personality_window.state("zoomed")
    
    # Analyze personality
    type_mb = analyze_personality(person)
    person["PersonalityTypeMB"] = type_mb
    
    # Get personality info
    if type_mb in PersonalityTypes:
        personality_info = PersonalityTypes[type_mb]
        description = personality_info["Description"]
        website = personality_info["WebSite"]
        strengths_text = ", ".join(personality_info["Strengths"])
        weaknesses_text = ", ".join(personality_info["Weaknesses"])
    else:
        description = "Personality type could not be determined."
        website = "https://www.16personalities.com/"
        strengths_text = "N/A"
        weaknesses_text = "N/A"
    
    type_bf = "conscientiousness"  # Placeholder for Big Five
    
    # Title
    Label(personality_window, text="Personality Analysis", bg="midnightblue", fg="white",
          font=('calibre', 26, 'bold')).place(relx=0.5, rely=0.1, anchor=S)
    
    # Myers-Briggs Type
    Label(personality_window, text="Type of Personality by Myers-Briggs Test:", bg="lightsteelblue",
          fg="black", font=('calibre', 18)).place(relx=0.1, rely=0.25)
    Label(personality_window, text=type_mb, bg="lightsteelblue",
          fg="black", font=('calibre', 18)).place(relx=0.8, rely=0.25)
    
    # Big Five Type
    Label(personality_window, text="Type of Personality by Big Five Test:", bg="lightsteelblue",
          fg="black", font=('calibre', 18)).place(relx=0.1, rely=0.35)
    Label(personality_window, text=type_bf, bg="lightsteelblue",
          fg="black", font=('calibre', 18)).place(relx=0.8, rely=0.35)
    
    # Description
    Label(personality_window, text="Description:", bg="lightsteelblue", fg="white",
          font=('calibre', 18)).place(relx=0.1, rely=0.45)
    text_description = Text(personality_window, height=5, width=90, bg="bisque", fg="black",
                            font=('calibre', 16))
    text_description.place(relx=0.1, rely=0.50)
    text_description.insert(END, description)
    
    # Strengths
    Label(personality_window, text="Strengths:", bg="mediumorchid", fg="white",
          font=('calibre', 16)).place(relx=0.1, rely=0.75)
    Label(personality_window, text=strengths_text, bg="thistle", fg="black",
          font=('calibre', 16)).place(relx=0.2, rely=0.75)
    
    # Weaknesses
    Label(personality_window, text="Weaknesses:", bg="mediumorchid", fg="white",
          font=('calibre', 16)).place(relx=0.1, rely=0.8)
    Label(personality_window, text=weaknesses_text, bg="thistle", fg="black",
          font=('calibre', 16)).place(relx=0.2, rely=0.8)
    
    # Website link
    def open_website():
        webbrowser.open(website, new=1)
    
    Label(personality_window, text="Website:", bg="lightyellow", fg="black",
          font=('calibre', 16)).place(relx=0.1, rely=0.9)
    Button(personality_window, text="Find More About Your Personality", command=open_website,
           bg="salmon", fg="white", activebackground="lightsalmon", activeforeground="white",
           height=1, width=40, font=('calibre', 16)).place(relx=0.2, rely=0.9)
