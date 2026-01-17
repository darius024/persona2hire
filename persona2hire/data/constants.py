"""Constants for job functions, qualifications, languages, and universities."""

# Job function levels (seniority hierarchy)
Functions = {
    0: ["assistant", "intern", "trainee", "apprentice", "worker", "labourer", "employee"],
    1: ["representative", "specialist", "coordinator", "analyst", "administrator", "generalist", "consultant",
        "associate", "technician", "agent", "surveyor", "engineer"],
    2: ["manager", "head", "hod"],
    3: ["director", "vp"],
    4: ["coo", "cfo", "cto", "cmo", "chro", "cpo", "chief", "vice president", "officer"],
    5: ["chief executive officer", "ceo", "president"],
    6: ["chairman"]
}

# Qualification levels
Qualifications = {
    1: ["gcse", "grades d-g", "l1", "level 1", "foundation", "entry level", "traineeship", "nvq level 1"],
    2: ["grades a-c", "l2", "level 2", "intermediate apprenticeship", "nvq level 2"],
    3: ["a-level", "a2", "as", "t-level", "l3", "level 3", "certificate", "advanced apprenticeship", "nvq level 3"],
    4: ["bachelor", "university degree", "undergraduate degree", "ba", "bsc", "foundation degree", "fda", "fdsc", "hnd",
        "hnc", "higher national", "higher apprenticeship", "nvq level 4", "foundation degree"],
    5: ["master", "ma", "msc", "mphil", "nvq level 5", "degree apprenticeship"],
    6: ["phd", "doctorate"]
}

# Language popularity/value ratings
Languages = {
    1: ["romanian", "bulgarian", "hungarian", "korean", "javanese", "tamil", "turkish",
        "bengali", "vietnamese", "marathi", "egyptian", "iranian", "polish", "indonesian", "gujarati", "malayalam",
        "yoruba", "hausa", "ukrainian", "igbo", "sindhi", "dutch", "amharic", "magahi", "thai", "saraiki", "somali",
        "sinhalese", "nigerian", "bavarian", "greek", "kazakh", "deccan", "zulu", "tunisian", "rundi", "czech",
        "sylheti", "xiang", "sundanese", "kannada", "tagalog", "gan", "cebuano", "khmer", "turkmen", "croatian",
        "kurdish", "marwari", "haryanvi", "dhundhari", "hmong", "belarusian", "mossi"],
    2: ["hindi", "bengali", "arabic", "french", "german", "russian", "portuguese", "punjabi", "japanese", "italian",
        "latin", "telugu"],
    3: ["english", "mandarin", "chinese", "spanish"]
}

# Top universities (can be populated for bonus scoring)
Top50Universities = {}

Top100Universities = {}
