"""Personality type definitions based on Myers-Briggs Type Indicator (MBTI)."""

# Big Five personality traits (OCEAN model)
BigFive = {
    "openness": [],
    "conscientiousness": [],
    "extroversion": [],
    "agreeableness": [],
    "neuroticism": []
}

# MBTI Personality Types with descriptions
PersonalityTypes = {
    "ISTJ": {
        "Name": "Logistician",
        "Traits": [],
        "Description": "A Logistician (ISTJ) is someone with the Introverted, Observant, Thinking, and Judging "
                       "personality traits. These people tend to be reserved yet willful, with a rational outlook on "
                       "life. They compose their actions carefully and carry them out with methodical purpose.",
        "Strengths": ["honest", "direct", "strong-willed", "dutiful", "very responsible", "calm", "practical", "jacks-of-all-trades"],
        "Weaknesses": ["stubborn", "insensitive", "always by the book", "judgmental"],
        "WebSite": "https://www.16personalities.com/istj-personality"
    },
    "ISFJ": {
        "Name": "Defender",
        "Traits": [],
        "Description": "A Defender (ISFJ) is someone with the Introverted, Observant, Feeling, and Judging personality traits. These people tend to be warm and unassuming in their own steady way. They're efficient and responsible, giving careful attention to practical details in their daily lives.",
        "Strengths": ["supportive", "reliable", "observant", "enthusiastic", "hardworking", "good practical skills"],
        "Weaknesses": ["overly humble", "taking things personally", "repressing their feelings", "overcommitted", "reluctant to change"],
        "WebSite": "https://www.16personalities.com/isfj-personality"
    },
    "INFJ": {
        "Name": "Advocate",
        "Traits": [],
        "Description": "An Advocate (INFJ) is someone with the Introverted, Intuitive, Feeling, and Judging personality traits. They tend to approach life with deep thoughtfulness and imagination. Their inner vision, personal values, and a quiet, principled version of humanism guide them in all things.",
        "Strengths": ["creative", "insightful", "principled", "passionate", "altruistic"],
        "Weaknesses": ["sensitive to criticism", "reluctant to open up", "perfectionistic", "prone to burnout"],
        "WebSite": "https://www.16personalities.com/infj-personality"
    },
    "INTJ": {
        "Name": "Architect",
        "Traits": [],
        "Description": "An Architect (INTJ) is a person with the Introverted, Intuitive, Thinking, and Judging personality traits. These thoughtful tacticians love perfecting the details of life, applying creativity and rationality to everything they do. Their inner world is often a private, complex one.",
        "Strengths": ["rational", "informed", "independent", "determined", "curious", "original"],
        "Weaknesses": ["arrogant", "dismissive of emotions", "overly critical", "combative", "socially clueless"],
        "WebSite": "https://www.16personalities.com/intj-personality"
    },
    "ISTP": {
        "Name": "Virtuoso",
        "Traits": [],
        "Description": "A Virtuoso (ISTP) is someone with the Introverted, Observant, Thinking, and Prospecting personality traits. They tend to have an individualistic mindset, pursuing goals without needing much external connection. They engage in life with inquisitiveness and personal skill, varying their approach as needed.",
        "Strengths": ["optimistic", "energetic", "creative", "practical", "spontaneous", "rational", "great in a crisis", "relaxed"],
        "Weaknesses": ["stubborn", "insensitive", "private", "reserved", "easily bored", "dislike commitment", "risky behaviour"],
        "WebSite": "https://www.16personalities.com/istp-personality"
    },
    "ISFP": {
        "Name": "Adventurer",
        "Traits": [],
        "Description": "An Adventurer (ISFP) is a person with the Introverted, Observant, Feeling, and Prospecting personality traits. They tend to have open minds, approaching life, new experiences, and people with grounded warmth. Their ability to stay in the moment helps them uncover exciting potentials.",
        "Strengths": ["charming", "sensitive", "imaginative", "passionate", "curious", "artistic"],
        "Weaknesses": ["fiercely independent", "unpredictable", "easily stressed", "overly competitive", "fluctuating self-esteem"],
        "WebSite": "https://www.16personalities.com/isfp-personality"
    },
    "INFP": {
        "Name": "Mediator",
        "Traits": [],
        "Description": "A Mediator (INFP) is someone who possesses the Introverted, Intuitive, Feeling, and Prospecting personality traits. These rare personality types tend to be quiet, open-minded, and imaginative, and they apply a caring and creative approach to everything they do.",
        "Strengths": ["empathetic", "generous", "open-minded", "creative", "passionate", "idealistic"],
        "Weaknesses": ["unrealistic", "self-isolating", "unfocused", "emotionally vulnerable", "self-critical"],
        "WebSite": "https://www.16personalities.com/infp-personality"
    },
    "INTP": {
        "Name": "Logician",
        "Traits": [],
        "Description": "A Logician (INTP) is someone with the Introverted, Intuitive, Thinking, and Prospecting personality traits. These flexible thinkers enjoy taking an unconventional approach to many aspects of life. They often seek out unlikely paths, mixing willingness to experiment with personal creativity.",
        "Strengths": ["analytical", "original", "open-minded", "curious", "objective"],
        "Weaknesses": ["disconnected", "insensitive", "dissatisfied", "impatient", "perfectionistic"],
        "WebSite": "https://www.16personalities.com/intp-personality"
    },
    "ESTP": {
        "Name": "Entrepreneur",
        "Traits": [],
        "Description": "An Entrepreneur (ESTP) is someone with the Extraverted, Observant, Thinking, and Prospecting personality traits. They tend to be energetic and action-oriented, deftly navigating whatever is in front of them. They love uncovering life's opportunities, whether socializing with others or in more personal pursuits.",
        "Strengths": ["bold", "rational", "practical", "original", "perceptive", "direct", "sociable"],
        "Weaknesses": ["insensitive", "impatient", "risk-prone", "unstructured", "defiant"],
        "WebSite": "https://www.16personalities.com/estp-personality"
    },
    "ESFP": {
        "Name": "Entertainer",
        "Traits": [],
        "Description": "An Entertainer (ESFP) is a person with the Extraverted, Observant, Feeling, and Prospecting personality traits. These people love vibrant experiences, engaging in life eagerly and taking pleasure in discovering the unknown. They can be very social, often encouraging others into shared activities.",
        "Strengths": ["bold", "original", "aesthetics and showmanship", "practical", "observant", "excellent people skills"],
        "Weaknesses": ["sensitive", "conflict-averse", "easily bored", "poor long-term planners", "unfocused"],
        "WebSite": "https://www.16personalities.com/esfp-personality"
    },
    "ENFP": {
        "Name": "Campaigner",
        "Traits": [],
        "Description": "A Campaigner (ENFP) is someone with the Extraverted, Intuitive, Feeling, and Prospecting personality traits. These people tend to embrace big ideas and actions that reflect their sense of hope and goodwill toward others. Their vibrant energy can flow in many directions.",
        "Strengths": ["curious", "perceptive", "enthusiastic", "excellent communicators", "festive", "good-natured"],
        "Weaknesses": ["people-pleasing", "unfocused", "disorganized", "overly accommodating", "overly optimistic", "restless"],
        "WebSite": "https://www.16personalities.com/enfp-personality"
    },
    "ENTP": {
        "Name": "Debater",
        "Traits": [],
        "Description": "A Debater (ENTP) is a person with the Extraverted, Intuitive, Thinking, and Prospecting personality traits. They tend to be bold and creative, deconstructing and rebuilding ideas with great mental agility. They pursue their goals vigorously despite any resistance they might encounter.",
        "Strengths": ["knowledgeable", "quick thinkers", "original", "excellent brainstormers", "charismatic", "energetic"],
        "Weaknesses": ["argumentative", "insensitive", "intolerant", "difficult to focus"],
        "WebSite": "https://www.16personalities.com/entp-personality"
    },
    "ESTJ": {
        "Name": "Executive",
        "Traits": [],
        "Description": "An Executive (ESTJ) is someone with the Extraverted, Observant, Thinking, and Judging personality traits. They possess great fortitude, emphatically following their own sensible judgment. They often serve as a stabilizing force among others, able to offer solid direction amid adversity.",
        "Strengths": ["dedicated", "strong-willed", "direct", "honest", "loyal", "patient", "reliable", "excellent organizer"],
        "Weaknesses": ["inflexible", "stubborn", "judgmental", "too focused on social status", "difficult to relax and express emotion"],
        "WebSite": "https://www.16personalities.com/estj-personality"
    },
    "ESFJ": {
        "Name": "Consul",
        "Traits": [],
        "Description": "A Consul (ESFJ) is a person with the Extraverted, Observant, Feeling, and Judging personality traits. They are attentive and people-focused, and they enjoy taking part in their social community. Their achievements are guided by decisive values, and they willingly offer guidance to others.",
        "Strengths": ["strong practical skills", "strong sense of duty", "very loyal", "sensitive", "warm", "good at connecting with others"],
        "Weaknesses": ["inflexible", "reluctant to innovate and improvise", "vulnerable to criticism", "often too needy", "too selfless"],
        "WebSite": "https://www.16personalities.com/esfj-personality"
    },
    "ENFJ": {
        "Name": "Protagonist",
        "Traits": [],
        "Description": "A Protagonist (ENFJ) is a person with the Extraverted, Intuitive, Feeling, and Judging personality traits. These warm, forthright types love helping others, and they tend to have strong ideas and values. They back their perspective with the creative energy to achieve their goals.",
        "Strengths": ["receptive", "reliable", "passionate", "altruistic", "charismatic"],
        "Weaknesses": ["unrealistic", "overly idealistic", "condescending", "intense", "overly empathetic"],
        "WebSite": "https://www.16personalities.com/enfj-personality"
    },
    "ENTJ": {
        "Name": "Commander",
        "Traits": [],
        "Description": "A Commander (ENTJ) is someone with the Extraverted, Intuitive, Thinking, and Judging personality traits. They are decisive people who love momentum and accomplishment. They gather information to construct their creative visions but rarely hesitate for long before acting on them.",
        "Strengths": ["efficient", "energetic", "self-confident", "strong-willed", "strategic thinkers", "charismatic", "inspiring"],
        "Weaknesses": ["stubborn", "dominant", "intolerant", "impatient", "arrogant", "poor handling of emotions", "cold", "ruthless"],
        "WebSite": "https://www.16personalities.com/entj-personality"
    }
}

# MBTI Domains for personality analysis
Domains = {
    "I": {
        "introverted": {
            "words": ["introverted", "shy", "quiet", "reticent", "introspective", "reclusive", "thinker", "anxious", "reserved"],
            "score": 0
        },
        "loneliness": {
            "words": ["lonely", "independent", "isolated", "desolate", "reclusive"],
            "score": 0
        },
        "listener": {
            "words": ["listener", "open-minded", "observer", "perceptive", "compassionate", "empathic"],
            "score": 0
        },
        "reserved": {
            "words": ["reserved", "quiet", "anxious", "antisocial"],
            "score": 0
        },
        "SCORE": 0
    },
    "E": {
        "extroverted": {
            "words": ["extroverted", "outgoing", "sociable", "talkative", "friendly"],
            "score": 0
        },
        "outgoing": {
            "words": ["outgoing", "out-going", "affectionate", "demonstrative"],
            "score": 0
        },
        "sociable": {
            "words": ["sociable", "talkative", "friendly", "companionable", "approachable", "cordial"],
            "score": 0
        },
        "enthusiastic": {
            "words": ["enthusiastic", "keen", "eager", "passionate", "avid", "energetic", "feeling"],
            "score": 0
        },
        "SCORE": 0
    },
    "S": {
        "analytical": {
            "words": ["analytical", "logical", "scientific", "methodical"],
            "score": 0
        },
        "realistic": {
            "words": ["realistic", "practical", "pragmatic", "truthful", "rational", "real"],
            "score": 0
        },
        "systematic": {
            "words": ["systematic", "structured", "organized", "planned", "well-ordered"],
            "score": 0
        },
        "practical": {
            "words": ["practical", "empirical", "actual", "active", "applied", "experiential", "effective", "qualified"],
            "score": 0
        },
        "SCORE": 0
    },
    "N": {
        "creative": {
            "words": ["creative", "artistic", "visionary", "imaginative", "inspired", "talented", "original"],
            "score": 0
        },
        "idealistic": {
            "words": ["idealistic", "utopian", "romantic", "unrealistic", "optimistic", "idealized", "dreamer"],
            "score": 0
        },
        "visionary": {
            "words": ["visionary", "imaginative", "inventive", "ingenious", "insightful", "introspective", "ambitious"],
            "score": 0
        },
        "inventive": {
            "words": ["inventive", "creative", "original", "skilful", "innovative", "ingenious", "artistic"],
            "score": 0
        },
        "SCORE": 0
    },
    "T": {
        "intellectual": {
            "words": ["smart", "clever", "wise", "intelligent"],
            "score": 0
        },
        "logical": {
            "words": ["logical", "smart", "analytical", "rational", "intelligent", "valid", "coherent", "organized"],
            "score": 0
        },
        "rational": {
            "words": ["rational", "reasoned", "logical", "coherent", "sensible", "deliberate", "balanced", "judicious"],
            "score": 0
        },
        "judgemental": {
            "words": ["judgemental", "narrow-minded", "judgy", "critical", "negative", "subjective"],
            "score": 0
        },
        "SCORE": 0
    },
    "F": {
        "empathetic": {
            "words": ["affectionate", "understanding", "intuitive", "spiritual", "open", "listener", "comprehensive"],
            "score": 0
        },
        "considerate": {
            "words": ["considerate", "attentive", "thoughtful", "mindful", "obliging", "amiable", "generous", "discreet", "solicitous", "alert", "careful", "cautious"],
            "score": 0
        },
        "sensitive": {
            "words": ["sensitive", "afraid", "emotive", "anxious", "influenceable"],
            "score": 0
        },
        "conscientious": {
            "words": ["conscientious", "considerate", "attentive", "thoughtful", "mindful", "obliging", "amiable", "generous", "discreet", "solicitous", "alert", "careful", "cautious"],
            "score": 0
        },
        "SCORE": 0
    },
    "J": {
        "reserved": {
            "words": ["reserved", "restrained", "reticent", "private", "cautious"],
            "score": 0
        },
        "organized": {
            "words": ["organized", "organizer", "systematic", "arranged", "coordinated", "oriented", "disciplined",
                      "precise", "regular", "meticulous", "controlled", "reasonable"],
            "score": 0
        },
        "logical": {
            "words": ["logical", "smart", "analytical", "rational", "intelligent", "valid", "coherent", "organized"],
            "score": 0
        },
        "stubborn": {
            "words": ["stubborn", "headstrong", "subjective", "firm", "determined", "inflexible"],
            "score": 0
        },
        "SCORE": 0
    },
    "P": {
        "flexible": {
            "words": ["adaptable", "open", "fearless", "brave", "creative", "innovator"],
            "score": 0
        },
        "spontaneous": {
            "words": ["unpredictable", "impulsive", "spontaneous", "happy", "flexible"],
            "score": 0
        },
        "action-oriented": {
            "words": ["action-oriented", "active", "applied", "practical", "proactive", "enterprising", "pragmatist", "advanced", "interactive"],
            "score": 0
        },
        "open-minded": {
            "words": ["curious", "non-judgemental", "open", "respectable", "lovable", "appreciative"],
            "score": 0
        },
        "SCORE": 0
    }
}

# Hobbies for personality inference
Hobbies = {
    "words": ["reading", "travelling", "animal", "gardening", "board games", "knitting", "embroidery", "upcycling",
              "drawing", "painting", "writing", "photography", "graphic design", "volunteer", "cooking", "baking",
              "watching", "films", "documentaries", "walking", "pet", "dancing", "wood crafting", "pottery", "sculpting",
              "chess", "language learning", "acting", "squash", "blog", "social media", "sing", "card games",
              "listening to music", "going out"],
    "domain": [],
    "trait": [],
    "sports": ["basketball", "golf", "running", "walking", "soccer", "volleyball", "badminton", "yoga", "pilates",
               "swimming", "skating", "rugby", "darts", "football", "barre", "tai chi", "stretching", "bowling",
               "hockey", "surfing", "tennis", "baseball", "gymnastics", "climbing", "karate", "horse", "snowboarding",
               "cycling", "archery", "boxing"]
}
