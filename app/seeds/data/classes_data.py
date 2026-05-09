import json

# ──────────────────────────────────────────────
# TEACHERS (10 Teachers)
# ──────────────────────────────────────────────
TEACHERS = [
    {"email": "dr.miller@teacher.example.com",   "display_name": "Dr. Sarah Miller",   "bio": "PhD in Mathematics, 10+ years teaching experience."},
    {"email": "prof.chen@teacher.example.com",   "display_name": "Prof. James Chen",   "bio": "Expert in Computer Science and AI research."},
    {"email": "ms.patel@teacher.example.com",    "display_name": "Ms. Priya Patel",    "bio": "Biology educator with a passion for genetics."},
    {"email": "mr.thompson@teacher.example.com", "display_name": "Mr. Alan Thompson",  "bio": "History and Social Studies specialist."},
    {"email": "dr.garcia@teacher.example.com",   "display_name": "Dr. Elena Garcia",   "bio": "Physics professor specialized in Quantum Mechanics."},
    {"email": "ms.lee@teacher.example.com",      "display_name": "Ms. Jennifer Lee",   "bio": "English Literature enthusiast and creative writer."},
    {"email": "mr.smith@teacher.example.com",    "display_name": "Mr. Robert Smith",   "bio": "Economics and Business Management expert."},
    {"email": "dr.kim@teacher.example.com",      "display_name": "Dr. David Kim",      "bio": "Chemistry researcher focused on Organic Synthesis."},
    {"email": "ms.davis@teacher.example.com",    "display_name": "Ms. Susan Davis",    "bio": "Psychology professor exploring behavioral patterns."},
    {"email": "mr.wilson@teacher.example.com",   "display_name": "Mr. Mark Wilson",    "bio": "Geography and Environmental Science teacher."},
]

DEMO_TEACHER_EMAIL = "teacher@example.com"
TEACHERS.append({"email": DEMO_TEACHER_EMAIL, "display_name": "Teacher Demo", "bio": "Main Demo Teacher Account"})

# ──────────────────────────────────────────────
# CLASSES (10 Classes)
# ──────────────────────────────────────────────
CLASSES = [
    {"code": "MATH101", "title": "Fundamentals of Mathematics", "description": "Algebra, geometry, and calculus concepts.", "teacher_email": DEMO_TEACHER_EMAIL, "student_indices": list(range(0, 15))},
    {"code": "CS201", "title": "Introduction to Computer Science", "description": "Programming fundamentals and algorithms.", "teacher_email": DEMO_TEACHER_EMAIL, "student_indices": list(range(10, 30))},
    {"code": "BIO301", "title": "General Biology", "description": "Cell biology, genetics, and ecology.", "teacher_email": "ms.patel@teacher.example.com", "student_indices": list(range(25, 40))},
    {"code": "HIST401", "title": "World History", "description": "Human civilizations survey.", "teacher_email": "mr.thompson@teacher.example.com", "student_indices": list(range(35, 55))},
    {"code": "PHYS501", "title": "Modern Physics", "description": "Relativity and quantum mechanics.", "teacher_email": DEMO_TEACHER_EMAIL, "student_indices": list(range(50, 65))},
    {"code": "LIT601", "title": "English Literature", "description": "Classic and contemporary works.", "teacher_email": "ms.lee@teacher.example.com", "student_indices": list(range(60, 80))},
    {"code": "ECON701", "title": "Principles of Economics", "description": "Micro and Macro economics.", "teacher_email": DEMO_TEACHER_EMAIL, "student_indices": list(range(75, 90))},
    {"code": "CHEM801", "title": "Organic Chemistry", "description": "Carbon compounds and reactions.", "teacher_email": "dr.kim@teacher.example.com", "student_indices": list(range(85, 100))},
    {"code": "PSY901", "title": "Intro to Psychology", "description": "Study of mind and behavior.", "teacher_email": "ms.davis@teacher.example.com", "student_indices": list(range(0, 20))},
    {"code": "GEO1001", "title": "Human Geography", "description": "Human activity and earth's surface.", "teacher_email": DEMO_TEACHER_EMAIL, "student_indices": list(range(10, 30))},
]

# ──────────────────────────────────────────────
# LESSONS with 5-7 questions each
# ──────────────────────────────────────────────

def _lesson(title, summary, blocks):
    return {"title": title, "summary": summary, "content_json": json.dumps(blocks)}

def _mcq(question, options, answer_idx):
    return {
        "type": "multiple_choice",
        "title": question,
        "options": [
            {"label": chr(65 + i), "value": opt, "is_correct": i == answer_idx}
            for i, opt in enumerate(options)
        ]
    }

def _tf(question, is_true):
    return _mcq(question, ["True", "False"], 0 if is_true else 1)

LESSONS_BY_CLASS = {
    "MATH101": [
        _lesson("Algebra Basics", "Variables and equations.", [
            {"type": "text", "content": "## Algebra Fundamentals\nSolving for `x` in linear equations."},
            _mcq("Solve 3x + 5 = 20", ["x=3", "x=5", "x=15", "x=7"], 1),
            _mcq("What is x in 2x - 10 = 0?", ["2", "5", "10", "0"], 1),
            _mcq("If x/4 = 8, what is x?", ["2", "12", "32", "16"], 2),
            _mcq("Simplify 2x + 3x - x", ["4x", "5x", "6x", "3x"], 0),
            _mcq("Which is a variable?", ["5", "π", "x", "+"], 2),
            _mcq("Value of 5^2?", ["10", "25", "15", "50"], 1),
            _tf("Is x + 5 = 10 a linear equation?", True),
            _tf("Is 2x = 4 equivalent to x = 8?", False)
        ])
    ],
    "CS201": [
        _lesson("Python Essentials", "Core syntax and data types.", [
            {"type": "text", "content": "## Python Programming\nPython is a high-level language."},
            _mcq("Output of print(2 + 3)?", ["23", "5", "Error", "None"], 1),
            _mcq("Which is a list?", ["(1,2)", "{1,2}", "[1,2]", "<1,2>"], 2),
            _mcq("Keyword for functions?", ["func", "define", "def", "fn"], 2),
            _mcq("Python file extension?", [".py", ".pt", ".python", ".txt"], 0),
            _mcq("Which is an integer?", ["'5'", "5.0", "5", "True"], 2),
            _mcq("Symbol for comments?", ["//", "/*", "#", "--"], 2),
            _tf("Python is a compiled language.", False),
            _tf("Python uses indentation for blocks.", True)
        ])
    ],
    "BIO301": [
        _lesson("Cell Structure", "The building blocks of life.", [
            {"type": "text", "content": "## Cell Biology\nOrganelles and their functions."},
            _mcq("Powerhouse of the cell?", ["Nucleus", "Ribosome", "Mitochondria", "Vacuole"], 2),
            _mcq("Where is DNA stored?", ["Nucleus", "Cytoplasm", "Wall", "Membrane"], 0),
            _mcq("Plant cells have this but animals don't:", ["Nucleus", "Cell Wall", "Ribosome", "Mitochondria"], 1),
            _mcq("Basic unit of life?", ["Atom", "Molecule", "Cell", "Tissue"], 2),
            _mcq("Process of cell division?", ["Meiosis", "Mitosis", "Osmosis", "Diffusion"], 1),
            _mcq("Organelle for photosynthesis?", ["Lysosome", "Chloroplast", "Golgi", "ER"], 1),
            _tf("Mitochondria is found in animal cells.", True),
            _tf("Plant cells lack a nucleus.", False)
        ])
    ],
    "HIST401": [
        _lesson("World War I", "Causes and consequences.", [
            {"type": "text", "content": "## The Great War\n1914-1918 conflict."},
            _mcq("When did WWI start?", ["1912", "1914", "1918", "1939"], 1),
            _mcq("Archduke assassinated in?", ["Paris", "Berlin", "Sarajevo", "London"], 2),
            _mcq("Treaty that ended WWI?", ["Paris", "Versailles", "Berlin", "London"], 1),
            _mcq("Central Powers included?", ["UK", "Germany", "France", "USA"], 1),
            _mcq("New tech in WWI?", ["Drones", "Tanks", "Nuclear", "Space"], 1),
            _mcq("How many years did it last?", ["2", "4", "6", "10"], 1)
        ])
    ],
    "PHYS501": [
        _lesson("Quantum Mechanics", "The subatomic world.", [
            {"type": "text", "content": "## Quantum Theory\nProbability and particles."},
            _mcq("Unit of energy?", ["Volt", "Joule", "Amp", "Watt"], 1),
            _mcq("Speed of light (c) is approx?", ["3k m/s", "300k km/s", "30m m/s", "1k km/s"], 1),
            _mcq("Light behaves as?", ["Wave", "Particle", "Both", "Neither"], 2),
            _mcq("Who found E=mc^2?", ["Newton", "Einstein", "Bohr", "Heisenberg"], 1),
            _mcq("Negatively charged particle?", ["Proton", "Neutron", "Electron", "Photon"], 2),
            _mcq("Location of protons?", ["Shells", "Nucleus", "Orbit", "Cloud"], 1)
        ])
    ],
    "LIT601": [
        _lesson("Poetry Analysis", "Rhythm and rhyme.", [
            {"type": "text", "content": "## Literary Devices\nMetaphors, Similes, and Imagery."},
            _mcq("A comparison using 'like' or 'as'?", ["Metaphor", "Simile", "Idiom", "Irony"], 1),
            _mcq("Repetition of initial sounds?", ["Rhyme", "Alliteration", "Stanza", "Verse"], 1),
            _mcq("A 14-line poem is a?", ["Haiku", "Sonnet", "Epic", "Lyric"], 1),
            _mcq("Opposite of what is expected?", ["Metaphor", "Irony", "Tone", "Theme"], 1),
            _mcq("Writer of a poem?", ["Author", "Poet", "Narrator", "Speaker"], 1),
            _mcq("Unit of poetry lines?", ["Paragraph", "Stanza", "Chapter", "Scene"], 1)
        ])
    ],
    "ECON701": [
        _lesson("Macroeconomics", "Global financial systems.", [
            {"type": "text", "content": "## Macro Basics\nGDP, Inflation, and Employment."},
            _mcq("What does GDP stand for?", ["Gross Domestic Product", "Gold Data Price", "General Debt Plan", "Gross Daily Profit"], 0),
            _mcq("Rise in general prices?", ["Deflation", "Inflation", "Stagflation", "Recession"], 1),
            _mcq("Central bank of USA?", ["World Bank", "IMF", "Federal Reserve", "Treasury"], 2),
            _mcq("Tax on imports?", ["Subsidy", "Tariff", "Quota", "Vat"], 1),
            _mcq("Market with one seller?", ["Duopoly", "Oligopoly", "Monopoly", "Perfect"], 2),
            _mcq("Study of individual choices?", ["Macro", "Micro", "Stats", "Banking"], 1)
        ])
    ],
    "CHEM801": [
        _lesson("Atomic Structure", "Elements and compounds.", [
            {"type": "text", "content": "## Chemistry Intro\nPeriodic table and bonding."},
            _mcq("Symbol for Gold?", ["Ag", "Au", "Fe", "Pb"], 1),
            _mcq("H2O is?", ["Oxygen", "Hydrogen", "Water", "Acid"], 2),
            _mcq("pH of 7 is?", ["Acidic", "Basic", "Neutral", "Salty"], 2),
            _mcq("Gas we breathe in?", ["Nitrogen", "Oxygen", "CO2", "Argon"], 1),
            _mcq("Atomic number of Hydrogen?", ["0", "1", "2", "10"], 1),
            _mcq("Sharing electrons is a ___ bond.", ["Ionic", "Covalent", "Metallic", "Hydrogen"], 1)
        ])
    ],
    "PSY901": [
        _lesson("Cognitive Psychology", "Memory and perception.", [
            {"type": "text", "content": "## Mental Processes\nHow we think and remember."},
            _mcq("Short term memory capacity approx?", ["2 items", "7 items", "100 items", "Infinite"], 1),
            _mcq("Study of behavior?", ["Sociology", "Psychology", "History", "Biology"], 1),
            _mcq("Founder of Psychoanalysis?", ["Jung", "Freud", "Skinner", "Piaget"], 1),
            _mcq("Response to a stimulus?", ["Reflex", "Conditioning", "Habit", "Action"], 1),
            _mcq("Nature vs ____?", ["Future", "Nurture", "Reality", "Logic"], 1),
            _mcq("Mental health professional?", ["Lawyer", "Psychologist", "Engineer", "Chef"], 1)
        ])
    ],
    "GEO1001": [
        _lesson("Urbanization", "City growth and impact.", [
            {"type": "text", "content": "## Urban Geography\nMigration and urban development."},
            _mcq("Move from country to city?", ["Ruralization", "Urbanization", "Globalization", "Migration"], 1),
            _mcq("World's largest city by pop?", ["NYC", "London", "Tokyo", "Paris"], 2),
            _mcq("Line dividing Earth horizontally?", ["Equator", "Prime Meridian", "Tropic", "Axis"], 0),
            _mcq("Which continent is also a country?", ["Africa", "Australia", "Europe", "Asia"], 1),
            _mcq("Study of weather?", ["Geography", "Meteorology", "Geology", "Physics"], 1),
            _mcq("Largest ocean?", ["Atlantic", "Indian", "Pacific", "Arctic"], 2)
        ])
    ],
}
