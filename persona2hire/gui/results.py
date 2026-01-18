"""Result display windows for jobs and personality analysis."""

from tkinter import *
from tkinter import ttk
import webbrowser

from ..analysis.job_analyzer import analyze_jobs, get_score_breakdown
from ..analysis.personality_analyzer import (
    analyze_personality,
    get_personality_percentages,
    get_big_five_profile,
    get_career_suggestions,
)
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

    if not persons_list:
        _show_message(parent, "No Candidates", "Please load some CV files first.")
        return

    if not selected_sector:
        _show_message(parent, "No Sector", "Please select a job sector first.")
        return

    results_window = Toplevel(parent)
    results_window.title(f"Results - {selected_sector}")
    results_window.configure(bg="dimgray")
    results_window.state("zoomed")

    # Calculate scores for each person
    for person in persons_list:
        person["PersonalityTypeMB"] = analyze_personality(person)
        person["Score"] = analyze_job(person, selected_sector)

    # Sort by score
    sorted_list = sorted(persons_list, key=lambda x: x.get("Score", 0), reverse=True)

    # Title
    Label(
        results_window,
        text=f"Candidates for {selected_sector}",
        bg="silver",
        fg="black",
        font=("calibre", 26, "bold"),
    ).place(relx=0.5, rely=0.08, anchor=CENTER)

    # Create treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("calibre", 14, "bold"))
    style.configure("Treeview", font=("calibre", 12), rowheight=30)

    columns = ("rank", "candidate", "score", "personality")
    treeview = ttk.Treeview(
        results_window,
        columns=columns,
        show="headings",
        height=15,
        selectmode="extended",
    )
    treeview.place(relx=0.5, rely=0.45, anchor=CENTER)

    treeview.heading("rank", text="#")
    treeview.heading("candidate", text="Candidate Name")
    treeview.heading("score", text="Score")
    treeview.heading("personality", text="Personality")

    treeview.column("rank", anchor=CENTER, width=50, stretch=NO)
    treeview.column("candidate", anchor=W, width=300, stretch=NO)
    treeview.column("score", anchor=CENTER, width=150, stretch=NO)
    treeview.column("personality", anchor=CENTER, width=150, stretch=NO)

    # Populate treeview (show top 10)
    for i, person in enumerate(sorted_list[:10], 1):
        name = f"{person.get('FirstName', '')} {person.get('LastName', '')}".strip()
        if not name:
            name = "Unknown"
        score = person.get("Score", 0)
        personality = person.get("PersonalityTypeMB", "N/A")

        treeview.insert("", END, values=(i, name, f"{score:.1f}/100", personality))

    # Score breakdown for selected candidate
    def on_select(event):
        selection = treeview.selection()
        if selection:
            item = treeview.item(selection[0])
            rank = int(item["values"][0]) - 1
            if 0 <= rank < len(sorted_list):
                person = sorted_list[rank]
                _show_score_breakdown(results_window, person, selected_sector)

    treeview.bind("<<TreeviewSelect>>", on_select)

    # Instructions
    Label(
        results_window,
        text="Click on a candidate to see their score breakdown",
        bg="dimgray",
        fg="white",
        font=("calibre", 12, "italic"),
    ).place(relx=0.5, rely=0.75, anchor=CENTER)


def _show_score_breakdown(parent, person: dict, sector: str):
    """Show detailed score breakdown in a popup."""
    breakdown = get_score_breakdown(person, sector)

    name = f"{person.get('FirstName', '')} {person.get('LastName', '')}".strip()

    popup = Toplevel(parent)
    popup.title(f"Score Breakdown - {name}")
    popup.configure(bg="white")
    popup.geometry("400x350")

    # Center the popup
    popup.transient(parent)

    Label(
        popup,
        text=f"Score Breakdown for {name}",
        bg="white",
        fg="black",
        font=("calibre", 14, "bold"),
    ).pack(pady=15)

    frame = Frame(popup, bg="white")
    frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

    categories = [
        ("Education", "education", "max_education"),
        ("Work Experience", "work_experience", "max_work_experience"),
        ("Skills Match", "skills", "max_skills"),
        ("Languages", "languages", "max_languages"),
        ("Soft Skills", "soft_skills", "max_soft_skills"),
        ("Additional", "additional", "max_additional"),
    ]

    for i, (label, key, max_key) in enumerate(categories):
        score = breakdown.get(key, 0)
        max_score = breakdown.get(max_key, 1)

        Label(
            frame,
            text=f"{label}:",
            bg="white",
            fg="black",
            font=("calibre", 12),
            anchor="w",
        ).grid(row=i, column=0, sticky="w", pady=5)

        Label(
            frame,
            text=f"{score:.1f} / {max_score}",
            bg="white",
            fg="darkblue",
            font=("calibre", 12, "bold"),
            anchor="e",
        ).grid(row=i, column=1, sticky="e", pady=5, padx=20)

    # Total
    total = sum(breakdown.get(cat[1], 0) for cat in categories)
    Label(
        frame,
        text="TOTAL:",
        bg="white",
        fg="black",
        font=("calibre", 14, "bold"),
        anchor="w",
    ).grid(row=len(categories), column=0, sticky="w", pady=15)

    Label(
        frame,
        text=f"{total:.1f} / 100",
        bg="white",
        fg="green",
        font=("calibre", 14, "bold"),
        anchor="e",
    ).grid(row=len(categories), column=1, sticky="e", pady=15, padx=20)

    Button(
        popup,
        text="Close",
        command=popup.destroy,
        bg="gray",
        fg="white",
        font=("calibre", 12),
    ).pack(pady=15)


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
    name = f"{person.get('FirstName', '')} {person.get('LastName', '')}".strip()

    # Title
    Label(
        jobs_window,
        text=f"Job Analysis for {name}",
        bg="silver",
        fg="black",
        font=("calibre", 26, "bold"),
    ).place(relx=0.5, rely=0.08, anchor=CENTER)

    # Subtitle
    Label(
        jobs_window,
        text="Top matching job sectors:",
        bg="gainsboro",
        fg="black",
        font=("calibre", 16),
    ).place(relx=0.5, rely=0.15, anchor=CENTER)

    # Create treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Calibri", 14, "bold"))
    style.configure("Treeview", font=("Calibri", 12), rowheight=28)

    treeview = ttk.Treeview(
        jobs_window,
        columns=("rank", "job", "score"),
        show="headings",
        height=15,
        selectmode="extended",
    )
    treeview.place(relx=0.5, rely=0.5, anchor=CENTER)

    treeview.heading("rank", text="#")
    treeview.heading("job", text="Job Sector")
    treeview.heading("score", text="Match Score")

    treeview.column("rank", anchor=CENTER, width=50, stretch=NO)
    treeview.column("job", anchor=W, width=400, stretch=YES)
    treeview.column("score", anchor=CENTER, width=150, stretch=NO)

    # Populate treeview (show top 10)
    for i, (sector, score) in enumerate(job_list[:10], 1):
        treeview.insert("", END, values=(i, sector, f"{score:.1f}/100"))


def show_personality(parent, person: dict):
    """
    Show personality analysis for a person.

    Args:
        parent: Parent Tkinter window
        person: Person dictionary to analyze
    """
    personality_window = Toplevel(parent)
    personality_window.title("Personality Analysis")
    personality_window.configure(bg="midnightblue")
    personality_window.state("zoomed")

    name = f"{person.get('FirstName', '')} {person.get('LastName', '')}".strip()

    # Analyze personality
    type_mb = analyze_personality(person)
    person["PersonalityTypeMB"] = type_mb

    # Get MBTI percentages
    percentages = get_personality_percentages(person)

    # Get Big Five profile
    big_five = get_big_five_profile(person)

    # Get personality info
    if type_mb in PersonalityTypes:
        personality_info = PersonalityTypes[type_mb]
        type_name = personality_info.get("Name", "")
        description = personality_info["Description"]
        website = personality_info["WebSite"]
        strengths_list = personality_info.get("Strengths", [])
        weaknesses_list = personality_info.get("Weaknesses", [])
        careers = personality_info.get("Careers", [])
    else:
        type_name = ""
        description = "Personality type could not be determined."
        website = "https://www.16personalities.com/"
        strengths_list = []
        weaknesses_list = []
        careers = []

    # Title
    Label(
        personality_window,
        text=f"Personality Analysis - {name}",
        bg="midnightblue",
        fg="white",
        font=("calibre", 24, "bold"),
    ).place(relx=0.5, rely=0.06, anchor=CENTER)

    # ===== MBTI Section =====
    mbti_frame = Frame(personality_window, bg="lightsteelblue", padx=20, pady=15)
    mbti_frame.place(relx=0.25, rely=0.15, anchor=N, width=400)

    Label(
        mbti_frame,
        text="Myers-Briggs Type (MBTI)",
        bg="lightsteelblue",
        fg="black",
        font=("calibre", 16, "bold"),
    ).pack(anchor="w")

    # Type with name
    type_display = f"{type_mb} - {type_name}" if type_name else type_mb
    Label(
        mbti_frame,
        text=type_display,
        bg="lightsteelblue",
        fg="darkblue",
        font=("calibre", 22, "bold"),
    ).pack(pady=10)

    # MBTI dimension bars
    dimensions = [
        ("I", "E", "Introversion", "Extroversion"),
        ("S", "N", "Sensing", "Intuition"),
        ("T", "F", "Thinking", "Feeling"),
        ("J", "P", "Judging", "Perceiving"),
    ]

    for left, right, left_name, right_name in dimensions:
        dim_frame = Frame(mbti_frame, bg="lightsteelblue")
        dim_frame.pack(fill=X, pady=3)

        left_pct = percentages.get(left, 50)
        right_pct = percentages.get(right, 50)

        Label(
            dim_frame,
            text=f"{left} {left_pct:.0f}%",
            bg="lightsteelblue",
            fg="black" if left_pct > right_pct else "gray",
            font=("calibre", 10, "bold" if left_pct > right_pct else "normal"),
            width=10,
            anchor="e",
        ).pack(side=LEFT)

        Label(
            dim_frame,
            text=f"{right_pct:.0f}% {right}",
            bg="lightsteelblue",
            fg="black" if right_pct > left_pct else "gray",
            font=("calibre", 10, "bold" if right_pct > left_pct else "normal"),
            width=10,
            anchor="w",
        ).pack(side=RIGHT)

    # ===== Big Five Section =====
    big_five_frame = Frame(personality_window, bg="lavender", padx=20, pady=15)
    big_five_frame.place(relx=0.75, rely=0.15, anchor=N, width=400)

    Label(
        big_five_frame,
        text="Big Five (OCEAN)",
        bg="lavender",
        fg="black",
        font=("calibre", 16, "bold"),
    ).pack(anchor="w")

    trait_names = {
        "openness": "Openness",
        "conscientiousness": "Conscientiousness",
        "extroversion": "Extroversion",
        "agreeableness": "Agreeableness",
        "neuroticism": "Neuroticism",
    }

    for trait, display_name in trait_names.items():
        score = big_five.get(trait, 0)
        trait_frame = Frame(big_five_frame, bg="lavender")
        trait_frame.pack(fill=X, pady=3)

        # Determine color based on score
        if score > 30:
            color = "green"
        elif score < -30:
            color = "red"
        else:
            color = "black"

        Label(
            trait_frame,
            text=f"{display_name}:",
            bg="lavender",
            fg="black",
            font=("calibre", 11),
            width=18,
            anchor="w",
        ).pack(side=LEFT)

        # Score indicator
        score_text = f"+{score:.0f}" if score > 0 else f"{score:.0f}"
        Label(
            trait_frame,
            text=score_text,
            bg="lavender",
            fg=color,
            font=("calibre", 11, "bold"),
            width=6,
            anchor="e",
        ).pack(side=RIGHT)

    # ===== Description Section =====
    desc_frame = Frame(personality_window, bg="bisque", padx=15, pady=10)
    desc_frame.place(relx=0.5, rely=0.52, anchor=N, width=900)

    Label(
        desc_frame,
        text="Description",
        bg="bisque",
        fg="black",
        font=("calibre", 14, "bold"),
    ).pack(anchor="w")

    text_description = Text(
        desc_frame,
        height=4,
        width=100,
        bg="white",
        fg="black",
        font=("calibre", 11),
        wrap=WORD,
    )
    text_description.pack(pady=5, fill=X)
    text_description.insert(END, description)
    text_description.config(state=DISABLED)

    # ===== Strengths & Weaknesses =====
    sw_frame = Frame(personality_window, bg="midnightblue")
    sw_frame.place(relx=0.5, rely=0.72, anchor=N)

    # Strengths
    strengths_frame = Frame(sw_frame, bg="palegreen", padx=15, pady=10)
    strengths_frame.pack(side=LEFT, padx=10)

    Label(
        strengths_frame,
        text="Strengths",
        bg="palegreen",
        fg="darkgreen",
        font=("calibre", 12, "bold"),
    ).pack()

    strengths_text = ", ".join(strengths_list) if strengths_list else "N/A"
    Label(
        strengths_frame,
        text=strengths_text,
        bg="palegreen",
        fg="black",
        font=("calibre", 11),
        wraplength=350,
    ).pack()

    # Weaknesses
    weaknesses_frame = Frame(sw_frame, bg="mistyrose", padx=15, pady=10)
    weaknesses_frame.pack(side=LEFT, padx=10)

    Label(
        weaknesses_frame,
        text="Weaknesses",
        bg="mistyrose",
        fg="darkred",
        font=("calibre", 12, "bold"),
    ).pack()

    weaknesses_text = ", ".join(weaknesses_list) if weaknesses_list else "N/A"
    Label(
        weaknesses_frame,
        text=weaknesses_text,
        bg="mistyrose",
        fg="black",
        font=("calibre", 11),
        wraplength=350,
    ).pack()

    # ===== Career Suggestions =====
    if careers:
        career_frame = Frame(personality_window, bg="lightyellow", padx=15, pady=8)
        career_frame.place(relx=0.5, rely=0.84, anchor=N)

        Label(
            career_frame,
            text="Suggested Careers: ",
            bg="lightyellow",
            fg="black",
            font=("calibre", 12, "bold"),
        ).pack(side=LEFT)

        Label(
            career_frame,
            text=", ".join(careers),
            bg="lightyellow",
            fg="darkblue",
            font=("calibre", 11),
        ).pack(side=LEFT)

    # ===== Website Link =====
    def open_website():
        webbrowser.open(website, new=1)

    Button(
        personality_window,
        text="Learn More About Your Personality Type",
        command=open_website,
        bg="salmon",
        fg="white",
        activebackground="lightsalmon",
        activeforeground="white",
        height=1,
        font=("calibre", 14),
    ).place(relx=0.5, rely=0.93, anchor=CENTER)


def _show_message(parent, title: str, message: str):
    """Show a simple message dialog."""
    popup = Toplevel(parent)
    popup.title(title)
    popup.configure(bg="white")
    popup.geometry("300x150")
    popup.transient(parent)

    Label(
        popup,
        text=message,
        bg="white",
        fg="black",
        font=("calibre", 12),
        wraplength=250,
    ).pack(pady=30)

    Button(
        popup,
        text="OK",
        command=popup.destroy,
        bg="gray",
        fg="white",
        font=("calibre", 12),
    ).pack()
