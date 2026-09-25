"""
HealthConnect ML Engine: Clinical Dataset, Knowledge Base & Symptom Metadata
Supports 41 diseases and 132 clinically mapped symptoms.
"""

SYMPTOMS = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering',
    'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue',
    'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_urination', 'fatigue',
    'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
    'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration',
    'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain',
    'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure',
    'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
    'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose',
    'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements',
    'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness',
    'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels',
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
    'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
    'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
    'foul_smell_of_urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
    'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite',
    'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
    'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
    'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload_secondary', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
    'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
    'red_sore_around_nose', 'yellow_crust_ooze'
]

SYMPTOM_CATEGORIES = {
    "General & Systemic": [
        "fatigue", "high_fever", "mild_fever", "chills", "shivering", "sweating",
        "weight_gain", "weight_loss", "lethargy", "restlessness", "malaise",
        "dehydration", "toxic_look_(typhos)", "mood_swings", "depression", "irritability", "anxiety"
    ],
    "Head, ENT & Eyes": [
        "headache", "dizziness", "continuous_sneezing", "runny_nose", "congestion",
        "sinus_pressure", "throat_irritation", "patches_in_throat", "loss_of_smell",
        "redness_of_eyes", "watering_from_eyes", "sunken_eyes", "pain_behind_the_eyes",
        "blurred_and_distorted_vision", "visual_disturbances", "ulcers_on_tongue", "drying_and_tingling_lips"
    ],
    "Chest & Cardiovascular": [
        "chest_pain", "breathlessness", "fast_heart_rate", "palpitations", "cough",
        "phlegm", "mucoid_sputum", "rusty_sputum", "blood_in_sputum"
    ],
    "Digestive & Abdomen": [
        "stomach_pain", "acidity", "vomiting", "indigestion", "nausea",
        "loss_of_appetite", "abdominal_pain", "diarrhoea", "constipation",
        "belly_pain", "passage_of_gases", "distention_of_abdomen", "stomach_bleeding",
        "swelling_of_stomach", "excessive_hunger", "increased_appetite"
    ],
    "Skin & Dermatological": [
        "itching", "skin_rash", "nodal_skin_eruptions", "yellowish_skin", "yellowing_of_eyes",
        "red_spots_over_body", "dischromic_patches", "pus_filled_pimples", "blackheads",
        "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
        "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze", "internal_itching", "bruising"
    ],
    "Musculoskeletal & Mobility": [
        "joint_pain", "muscle_pain", "back_pain", "neck_pain", "stiff_neck",
        "knee_pain", "hip_joint_pain", "swelling_joints", "movement_stiffness",
        "painful_walking", "muscle_weakness", "muscle_wasting", "cramps",
        "weakness_in_limbs", "swollen_legs", "swollen_extremeties"
    ],
    "Neurological & Critical": [
        "slurred_speech", "spinning_movements", "loss_of_balance", "unsteadiness",
        "weakness_of_one_body_side", "altered_sensorium", "lack_of_concentration", "coma"
    ],
    "Urinary & Endocrine": [
        "burning_micturition", "spotting_urination", "dark_urine", "yellow_urine",
        "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine", "polyuria",
        "irregular_sugar_level", "cold_hands_and_feets", "enlarged_thyroid", "puffy_face_and_eyes",
        "brittle_nails", "abnormal_menstruation"
    ]
}

# Clinical Disease Profiles: primary and characteristic symptoms
DISEASE_SYMPTOM_MAP = {
    "Fungal infection": [
        "itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"
    ],
    "Allergy": [
        "continuous_sneezing", "shivering", "chills", "watering_from_eyes", "redness_of_eyes"
    ],
    "GERD": [
        "acidity", "ulcers_on_tongue", "stomach_pain", "cough", "chest_pain"
    ],
    "Chronic cholestasis": [
        "itching", "vomiting", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes"
    ],
    "Drug Reaction": [
        "itching", "skin_rash", "stomach_pain", "burning_micturition", "spotting_urination"
    ],
    "Peptic ulcer diseae": [
        "vomiting", "indigestion", "loss_of_appetite", "abdominal_pain", "passage_of_gases", "internal_itching"
    ],
    "AIDS": [
        "muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts"
    ],
    "Diabetes": [
        "fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "obesity", "excessive_hunger", "increased_appetite", "polyuria"
    ],
    "Gastroenteritis": [
        "vomiting", "sunken_eyes", "dehydration", "diarrhoea"
    ],
    "Bronchial Asthma": [
        "fatigue", "cough", "high_fever", "breathlessness", "family_history", "mucoid_sputum"
    ],
    "Hypertension": [
        "headache", "chest_pain", "dizziness", "loss_of_balance", "lack_of_concentration"
    ],
    "Migraine": [
        "acidity", "indigestion", "headache", "blurred_and_distorted_vision", "excessive_hunger", "stiff_neck", "depression", "irritability", "visual_disturbances"
    ],
    "Cervical spondylosis": [
        "back_pain", "neck_pain", "dizziness", "loss_of_balance"
    ],
    "Paralysis (brain hemorrhage)": [
        "vomiting", "headache", "weakness_of_one_body_side", "altered_sensorium"
    ],
    "Jaundice": [
        "itching", "vomiting", "fatigue", "weight_loss", "high_fever", "yellowish_skin", "dark_urine", "abdominal_pain"
    ],
    "Malaria": [
        "chills", "vomiting", "high_fever", "sweating", "headache", "nausea", "muscle_pain"
    ],
    "Chicken pox": [
        "itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache", "loss_of_appetite", "mild_fever", "swelled_lymph_nodes", "malaise", "red_spots_over_body"
    ],
    "Dengue": [
        "skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "muscle_pain", "red_spots_over_body"
    ],
    "Typhoid": [
        "chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation", "abdominal_pain", "diarrhoea", "toxic_look_(typhos)", "belly_pain"
    ],
    "hepatitis A": [
        "joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes", "muscle_pain"
    ],
    "Hepatitis B": [
        "itching", "fatigue", "lethargy", "yellowish_skin", "dark_urine", "loss_of_appetite", "abdominal_pain", "yellow_urine", "yellowing_of_eyes", "receiving_blood_transfusion", "receiving_unsterile_injections"
    ],
    "Hepatitis C": [
        "fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes", "family_history"
    ],
    "Hepatitis D": [
        "joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"
    ],
    "Hepatitis E": [
        "joint_pain", "vomiting", "fatigue", "high_fever", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "acute_liver_failure", "coma", "stomach_bleeding"
    ],
    "Alcoholic hepatitis": [
        "vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload"
    ],
    "Tuberculosis": [
        "chills", "vomiting", "fatigue", "weight_loss", "cough", "high_fever", "breathlessness", "sweating", "loss_of_appetite", "mild_fever", "phlegm", "swelled_lymph_nodes", "malaise", "blood_in_sputum"
    ],
    "Common Cold": [
        "continuous_sneezing", "chills", "fatigue", "cough", "high_fever", "headache", "swelled_lymph_nodes", "malaise", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "loss_of_smell", "muscle_pain"
    ],
    "Pneumonia": [
        "chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "malaise", "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum"
    ],
    "Dimorphic hemmorhoids(piles)": [
        "constipation", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus"
    ],
    "Heart attack": [
        "vomiting", "breathlessness", "sweating", "chest_pain", "fast_heart_rate"
    ],
    "Varicose veins": [
        "fatigue", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf"
    ],
    "Hypothyroidism": [
        "fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "lethargy", "dizziness", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "depression", "irritability", "abnormal_menstruation"
    ],
    "Hyperthyroidism": [
        "fatigue", "mood_swings", "weight_loss", "restlessness", "sweating", "diarrhoea", "fast_heart_rate", "excessive_hunger", "muscle_weakness", "irritability", "abnormal_menstruation"
    ],
    "Hypoglycemia": [
        "vomiting", "fatigue", "anxiety", "sweating", "headache", "nausea", "blurred_and_distorted_vision", "excessive_hunger", "drying_and_tingling_lips", "slurred_speech", "irritability", "palpitations"
    ],
    "Osteoarthristis": [
        "joint_pain", "neck_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking"
    ],
    "Arthritis": [
        "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "painful_walking"
    ],
    "(vertigo) Paroymsal  Positional Vertigo": [
        "vomiting", "headache", "nausea", "spinning_movements", "loss_of_balance", "unsteadiness"
    ],
    "Acne": [
        "skin_rash", "pus_filled_pimples", "blackheads", "scurring"
    ],
    "Urinary tract infection": [
        "burning_micturition", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine"
    ],
    "Psoriasis": [
        "skin_rash", "joint_pain", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails"
    ],
    "Impetigo": [
        "skin_rash", "high_fever", "blister", "red_sore_around_nose", "yellow_crust_ooze"
    ]
}

# Clinical Knowledge Base with Specialists, Precautions, Warning Signs, and Base Severity
DISEASE_KNOWLEDGE_BASE = {
    "Fungal infection": {
        "specialist": "Dermatologist",
        "base_severity": "MILD",
        "description": "Fungal infection is a skin disorder caused by fungal overgrowth, resulting in rashes, scaling, and itching.",
        "precautions": [
            "Keep the infected skin area clean and dry.",
            "Use antifungal cream or dust powder as recommended by a dermatologist.",
            "Avoid sharing towels, clothes, or personal items.",
            "Wear loose, breathable cotton garments."
        ],
        "warning_signs": [
            "Spreading of rash to large body areas",
            "Severe pain or signs of bacterial superinfection like yellow pus",
            "Fever developing alongside the skin lesion"
        ]
    },
    "Allergy": {
        "specialist": "Allergist / Immunologist",
        "base_severity": "MILD",
        "description": "An allergic reaction triggered by environmental allergens, causing sneezing, watery eyes, and mucosal irritation.",
        "precautions": [
            "Identify and avoid known environmental allergens like pollen, dust mites, or pet dander.",
            "Use recommended antihistamines or nasal saline sprays.",
            "Keep windows closed during high pollen counts.",
            "Wash bedding weekly in hot water."
        ],
        "warning_signs": [
            "Swelling of the lips, tongue, or throat",
            "Shortness of breath or wheezing (anaphylaxis)",
            "Dizziness or sudden drop in blood pressure"
        ]
    },
    "GERD": {
        "specialist": "Gastroenterologist",
        "base_severity": "MODERATE",
        "description": "Gastroesophageal Reflux Disease is a digestive disorder where stomach acid flows back into the food pipe.",
        "precautions": [
            "Avoid spicy, greasy, citrus, and caffeinated foods.",
            "Do not lie down immediately within 2-3 hours after eating.",
            "Elevate the head of your bed by 6 inches.",
            "Eat smaller, more frequent meals rather than large feasts."
        ],
        "warning_signs": [
            "Difficulty or pain while swallowing food",
            "Vomiting coffee-ground material or blood",
            "Severe, radiating chest pain mimicking cardiac distress"
        ]
    },
    "Chronic cholestasis": {
        "specialist": "Hepatologist / Gastroenterologist",
        "base_severity": "SEVERE",
        "description": "A chronic liver condition characterized by impairment or cessation of bile flow from the liver into the duodenum.",
        "precautions": [
            "Maintain a low-fat, high-protein balanced diet.",
            "Strictly avoid alcohol and hepatotoxic medications.",
            "Consult a hepatologist for liver function panel testing.",
            "Supplement fat-soluble vitamins (A, D, E, K) under supervision."
        ],
        "warning_signs": [
            "Progressive deep jaundice (yellow eyes and skin)",
            "Unbearable pruritus (intense itching) interrupting sleep",
            "Dark tea-colored urine and pale, clay-colored stools"
        ]
    },
    "Drug Reaction": {
        "specialist": "Dermatologist / Clinical Pharmacologist",
        "base_severity": "SEVERE",
        "description": "An adverse physiological or allergic reaction to a recently administered drug or medication.",
        "precautions": [
            "Immediately stop taking the suspected medication under doctor advice.",
            "Carry a written medical card detailing known drug allergies.",
            "Seek emergency medical evaluation if rash spreads rapidly.",
            "Stay well hydrated and avoid self-medicating."
        ],
        "warning_signs": [
            "Blistering or peeling of skin (Stevens-Johnson syndrome warning)",
            "Facial, tongue, or throat swelling",
            "High fever accompanied by severe full-body rash"
        ]
    },
    "Peptic ulcer diseae": {
        "specialist": "Gastroenterologist",
        "base_severity": "MODERATE",
        "description": "Open sores that develop on the inside lining of the stomach and the upper portion of the small intestine.",
        "precautions": [
            "Avoid NSAID painkillers like ibuprofen and aspirin unless prescribed.",
            "Limit alcohol intake and completely avoid smoking.",
            "Eat bland, low-acid meals at regular intervals.",
            "Consult a specialist for H. pylori screening."
        ],
        "warning_signs": [
            "Sudden, sharp, severe persistent stomach pain",
            "Vomiting dark blood or coffee-ground substance",
            "Black, tarry bowel movements"
        ]
    },
    "AIDS": {
        "specialist": "Infectious Disease Specialist",
        "base_severity": "CRITICAL",
        "description": "Advanced stage of HIV infection that severely damages the immune system's ability to fight infections.",
        "precautions": [
            "Adhere strictly to prescribed Antiretroviral Therapy (ART) regimens.",
            "Practice safe sex and avoid sharing needles or sharp personal items.",
            "Maintain strict hygiene and consume only pasteurized and thoroughly cooked foods.",
            "Undergo routine CD4 counts and viral load monitoring."
        ],
        "warning_signs": [
            "Rapid, unexplained weight loss and prolonged high fever",
            "Persistent severe cough with shortness of breath",
            "Opportunistic fungal infections or severe oral thrush"
        ]
    },
    "Diabetes": {
        "specialist": "Endocrinologist",
        "base_severity": "MODERATE",
        "description": "A metabolic disorder characterized by sustained elevated blood glucose levels due to insulin deficiency or resistance.",
        "precautions": [
            "Monitor fasting and post-prandial blood sugar levels consistently.",
            "Follow a personalized low-glycemic index, high-fiber dietary plan.",
            "Engage in at least 30 minutes of moderate aerobic exercise daily.",
            "Inspect feet daily for cuts, blisters, or calluses."
        ],
        "warning_signs": [
            "Excessive thirst accompanied by confusion or sweet-smelling breath",
            "Non-healing ulcers or sores on the lower limbs",
            "Sudden visual changes or episodes of severe dizziness"
        ]
    },
    "Gastroenteritis": {
        "specialist": "General Physician",
        "base_severity": "MODERATE",
        "description": "Acute inflammation of the gastrointestinal tract, typically caused by viral or bacterial foodborne infection.",
        "precautions": [
            "Drink plenty of oral rehydration solutions (ORS) and electrolyte liquids.",
            "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast).",
            "Wash hands thoroughly with soap before meals and after restroom use.",
            "Avoid dairy products, caffeine, and fatty foods during recovery."
        ],
        "warning_signs": [
            "Signs of severe dehydration: inability to keep liquids down, dry mouth, no urination",
            "Blood in stool or persistent vomiting exceeding 24 hours",
            "High fever exceeding 102°F (39°C)"
        ]
    },
    "Bronchial Asthma": {
        "specialist": "Pulmonologist",
        "base_severity": "SEVERE",
        "description": "A chronic condition that inflames and narrows the airways, causing breathlessness, wheezing, and coughing.",
        "precautions": [
            "Keep quick-relief rescue inhalers (e.g. Salbutamol) accessible at all times.",
            "Avoid known triggers such as tobacco smoke, cold air, dust, and animal fur.",
            "Use a peak flow meter regularly to monitor airway capacity.",
            "Take long-term controller medications as prescribed."
        ],
        "warning_signs": [
            "Severe shortness of breath where speaking full sentences is difficult",
            "Rescue inhaler fails to provide symptom relief within 15 minutes",
            "Bluish tint in lips or fingernails (cyanosis)"
        ]
    },
    "Hypertension": {
        "specialist": "Cardiologist",
        "base_severity": "MODERATE",
        "description": "Long-term medical condition in which blood pressure in the arteries is persistently elevated.",
        "precautions": [
            "Adopt the DASH diet with restricted dietary sodium (less than 2g/day).",
            "Monitor blood pressure daily at the same time.",
            "Exercise regularly and manage stress through relaxation techniques.",
            "Limit alcohol intake and avoid smoking."
        ],
        "warning_signs": [
            "Blood pressure reading exceeding 180/120 mmHg (Hypertensive Crisis)",
            "Severe throbbing headache accompanied by blurred vision",
            "Chest pressure, shortness of breath, or numbness"
        ]
    },
    "Migraine": {
        "specialist": "Neurologist",
        "base_severity": "MODERATE",
        "description": "A neurological condition that causes intense, debilitating throbbing headache episodes often accompanied by sensory sensitivity.",
        "precautions": [
            "Rest in a quiet, dark room during acute headache onset.",
            "Maintain consistent sleep, hydration, and meal schedules.",
            "Identify food triggers like aged cheese, chocolate, artificial sweeteners, or nitrates.",
            "Apply a cold compress to your forehead or neck."
        ],
        "warning_signs": [
            "Thunderclap headache: sudden, explosive onset within seconds",
            "Headache accompanied by high fever, stiff neck, or confusion",
            "Focal weakness, speech impairment, or loss of vision"
        ]
    },
    "Cervical spondylosis": {
        "specialist": "Orthopedic Specialist / Neurologist",
        "base_severity": "MILD",
        "description": "Age-related wear and tear affecting the spinal disks in your neck, leading to stiffness and radiating pain.",
        "precautions": [
            "Perform gentle neck stretches and strengthening exercises daily.",
            "Maintain ergonomic posture while working at computers or reading.",
            "Use an orthopedic cervical support pillow while sleeping.",
            "Avoid holding your phone between your ear and shoulder."
        ],
        "warning_signs": [
            "Numbness, tingling, or weakness radiating into hands or fingers",
            "Loss of bowel or bladder control",
            "Difficulty walking or maintaining balance"
        ]
    },
    "Paralysis (brain hemorrhage)": {
        "specialist": "Neurologist / Neurosurgeon",
        "base_severity": "CRITICAL",
        "description": "Neurological deficit caused by bleeding inside the brain tissue or subarachnoid space, requiring urgent emergency intervention.",
        "precautions": [
            "IMMEDIATE EMERGENCY: Call emergency services without delay.",
            "Keep patient flat with head slightly elevated (30 degrees).",
            "Do NOT administer food, water, or oral medications.",
            "Note the exact time symptoms began for emergency medical teams."
        ],
        "warning_signs": [
            "Sudden unilateral facial drooping or arm weakness (FAST protocol)",
            "Slurred speech or total inability to comprehend words",
            "Loss of consciousness or severe seizures"
        ]
    },
    "Jaundice": {
        "specialist": "Hepatologist / Gastroenterologist",
        "base_severity": "SEVERE",
        "description": "Yellowish discoloration of the skin and mucous membranes caused by high bilirubin levels from liver dysfunction or bile duct blockage.",
        "precautions": [
            "Drink plenty of boiled water and fresh sugarcane or fruit juices.",
            "Avoid all oily, heavy, fried foods and alcohol.",
            "Get liver enzymes (SGOT, SGPT, Bilirubin) tested promptly.",
            "Ensure adequate rest until liver inflammation subsides."
        ],
        "warning_signs": [
            "Extreme drowsiness or disorientation (hepatic encephalopathy)",
            "Vomiting blood or black stools",
            "High fever with chills and severe right upper quadrant abdominal pain"
        ]
    },
    "Malaria": {
        "specialist": "General Physician / Infectious Disease",
        "base_severity": "SEVERE",
        "description": "A life-threatening vector-borne disease caused by Plasmodium parasites transmitted through bites of infected female Anopheles mosquitoes.",
        "precautions": [
            "Take prescribed antimalarial medications (such as ACTs) for full duration.",
            "Use mosquito repellents and sleep under insecticide-treated bed nets.",
            "Eliminate stagnant water collection around living areas.",
            "Maintain fluid and electrolyte balance to manage high fevers."
        ],
        "warning_signs": [
            "Severe chills alternating with high fever spikes and profound sweating",
            "Dark, tea-colored urine (blackwater fever)",
            "Confusion, convulsions, or extreme lethargy"
        ]
    },
    "Chicken pox": {
        "specialist": "Pediatrician / Dermatologist",
        "base_severity": "MILD",
        "description": "A highly contagious viral infection caused by the Varicella-Zoster virus, causing an itchy blister-like rash.",
        "precautions": [
            "Apply calamine lotion and take lukewarm oatmeal baths for itch relief.",
            "Isolate patient to prevent transmission to susceptible individuals.",
            "Keep fingernails trimmed short to prevent secondary bacterial infection from scratching.",
            "Wear loose, soft cotton clothing."
        ],
        "warning_signs": [
            "Rash spreads to the eyes or involves blistering in the throat",
            "Skin lesions become intensely red, swollen, or leak pus",
            "Drowsiness, severe cough, or breathing difficulty"
        ]
    },
    "Dengue": {
        "specialist": "General Physician / Hematologist",
        "base_severity": "SEVERE",
        "description": "A mosquito-borne viral infection caused by Dengue virus, marked by high fever, severe headache, behind-eye pain, and bone-breaking joint ache.",
        "precautions": [
            "Ensure rigorous bed rest and intense hydration with ORS, coconut water, and soups.",
            "Avoid aspirin and ibuprofen as they increase bleeding risks; take paracetamol for fever.",
            "Monitor platelet counts with daily Complete Blood Count (CBC) tests.",
            "Protect against mosquito bites to stop household transmission."
        ],
        "warning_signs": [
            "Severe abdominal pain or persistent vomiting",
            "Bleeding gums, nosebleeds, or mucosal hemorrhages",
            "Sudden drop in platelet counts below 50,000/mcL"
        ]
    },
    "Typhoid": {
        "specialist": "General Physician",
        "base_severity": "SEVERE",
        "description": "Bacterial infection caused by Salmonella typhi, spreading through contaminated food and drinking water.",
        "precautions": [
            "Complete full course of prescribed antibiotics even after fever resolves.",
            "Drink only boiled or commercially bottled sealed water.",
            "Eat soft, easily digestible foods like porridge, boiled potatoes, and soups.",
            "Practice thorough hand washing with soap before eating."
        ],
        "warning_signs": [
            "Step-ladder high fever persisting beyond 5-7 days",
            "Severe abdominal distension and intense pain",
            "Delirium, confusion, or extreme weakness"
        ]
    },
    "hepatitis A": {
        "specialist": "Gastroenterologist",
        "base_severity": "MODERATE",
        "description": "A contagious liver infection caused by the hepatitis A virus, predominantly contracted through ingestion of contaminated food or water.",
        "precautions": [
            "Drink clean, purified water and avoid unhygienic street food.",
            "Consume a high-carbohydrate, low-fat diet with adequate fluids.",
            "Get vaccinated against Hepatitis A if traveling or unimmunized.",
            "Strictly avoid alcohol and non-essential hepatotoxic drugs."
        ],
        "warning_signs": [
            "Intense yellowing of eyes and dark brownish urine",
            "Intractable vomiting and inability to retain fluids",
            "Extreme exhaustion or altered mental status"
        ]
    },
    "Hepatitis B": {
        "specialist": "Hepatologist",
        "base_severity": "SEVERE",
        "description": "A serious liver infection caused by the Hepatitis B virus, transmitted through infected blood, semen, and other bodily fluids.",
        "precautions": [
            "Seek specialist evaluation for antiviral therapy and liver profiling.",
            "Never share razors, toothbrushes, needles, or sharp instruments.",
            "Practice barrier protection during sexual intercourse.",
            "Vaccinate close household and sexual partners."
        ],
        "warning_signs": [
            "Progressive abdominal swelling (ascites)",
            "Bruising or bleeding easily from minor bumps",
            "Confusion, forgetfulness, or unusual sleep cycles"
        ]
    },
    "Hepatitis C": {
        "specialist": "Hepatologist",
        "base_severity": "SEVERE",
        "description": "A viral infection that causes liver inflammation, often leading to serious liver damage if untreated.",
        "precautions": [
            "Consult a hepatologist for direct-acting antiviral (DAA) medications which cure >95% cases.",
            "Avoid all alcoholic beverages to prevent accelerating liver fibrosis.",
            "Undergo screening for liver cirrhosis and hepatocellular carcinoma.",
            "Ensure sterile medical and tattooing procedures."
        ],
        "warning_signs": [
            "Yellowing of skin and eyes alongside swollen lower legs",
            "Vomiting blood or passing tarry black stools",
            "Severe unexplained chronic fatigue and memory fog"
        ]
    },
    "Hepatitis D": {
        "specialist": "Hepatologist",
        "base_severity": "SEVERE",
        "description": "A serious liver disease caused by the Hepatitis D virus, occurring only in individuals who are also infected with Hepatitis B.",
        "precautions": [
            "Maintain regular consultations with a hepatologist specializing in co-infections.",
            "Avoid sharing needles, syringes, or personal grooming items.",
            "Take antiviral treatments as prescribed without missing doses.",
            "Follow a nutrient-rich, liver-friendly dietary protocol."
        ],
        "warning_signs": [
            "Rapidly worsening jaundice and right upper quadrant abdominal tenderness",
            "Fluid buildup in abdomen (ascites) and leg swelling",
            "Signs of acute liver decompensation"
        ]
    },
    "Hepatitis E": {
        "specialist": "Gastroenterologist",
        "base_severity": "SEVERE",
        "description": "A waterborne viral liver infection common in developing regions with inadequate clean water sanitation.",
        "precautions": [
            "Drink only boiled or purified water and avoid uncooked shell fish.",
            "Pregnant women must seek urgent medical evaluation as Hep E carries high maternal risk.",
            "Rest adequately and avoid strenuous physical exertion.",
            "Maintain strict kitchen and bathroom hygiene."
        ],
        "warning_signs": [
            "Pregnancy complicated by fever, jaundice, or severe vomiting",
            "Mental confusion, lethargy, or extreme drowsiness",
            "Hemorrhagic signs or acute liver failure manifestations"
        ]
    },
    "Alcoholic hepatitis": {
        "specialist": "Hepatologist / Addiction Specialist",
        "base_severity": "CRITICAL",
        "description": "Severe inflammation of the liver caused by heavy, long-term alcohol consumption.",
        "precautions": [
            "Immediately and completely cease all alcohol consumption.",
            "Seek medical detoxification and specialized counseling support.",
            "Follow a high-protein, calorie-dense nutritional rehabilitation diet.",
            "Regularly monitor liver enzymes, coagulation parameters, and ultrasound."
        ],
        "warning_signs": [
            "Distended, fluid-filled abdomen (ascites) and painful hepatomegaly",
            "Vomiting blood from esophageal varices",
            "Confusion, tremors, and jaundice (hepatic encephalopathy)"
        ]
    },
    "Tuberculosis": {
        "specialist": "Pulmonologist / Infectious Disease",
        "base_severity": "SEVERE",
        "description": "A contagious bacterial infection caused by Mycobacterium tuberculosis that primarily attacks the lungs.",
        "precautions": [
            "Complete the entire 6-9 month course of Directly Observed Treatment (DOTS) therapy.",
            "Cover your mouth when coughing and wear a mask in public during initial weeks.",
            "Ensure well-ventilated living quarters with plenty of sunlight.",
            "Eat a high-protein diet to rebuild strength and body mass."
        ],
        "warning_signs": [
            "Coughing up blood or blood-tinged phlegm (hemoptysis)",
            "Chest pain when breathing or coughing",
            "Unexplained rapid weight loss and drenching night sweats"
        ]
    },
    "Common Cold": {
        "specialist": "General Physician",
        "base_severity": "MILD",
        "description": "A common, mild viral infectious disease of the upper respiratory tract involving the nose and throat.",
        "precautions": [
            "Get plenty of rest and drink warm fluids (soups, herbal teas, warm water).",
            "Use steam inhalation and saline nasal sprays to relieve nasal congestion.",
            "Gargle with warm salt water to soothe throat irritation.",
            "Wash hands regularly to prevent spreading infection to others."
        ],
        "warning_signs": [
            "Fever exceeding 101.5°F lasting more than 3 consecutive days",
            "Shortness of breath, wheezing, or chest tightness",
            "Severe earache or persistent facial pressure indicating sinus infection"
        ]
    },
    "Pneumonia": {
        "specialist": "Pulmonologist",
        "base_severity": "SEVERE",
        "description": "An inflammatory condition of the lung primarily affecting the microscopic air sacs (alveoli), caused by infection.",
        "precautions": [
            "Take prescribed antibiotics or antivirals strictly according to schedule.",
            "Get plenty of rest and stay well hydrated to loosen chest secretions.",
            "Use a pulse oximeter to track blood oxygen levels (SpO2).",
            "Avoid smoking and secondhand tobacco smoke exposure."
        ],
        "warning_signs": [
            "Blood oxygen saturation (SpO2) dropping below 92%",
            "Severe chest pain worsening with deep breaths or coughing",
            "Bluish color in fingertips, lips, or rapid shallow breathing"
        ]
    },
    "Dimorphic hemmorhoids(piles)": {
        "specialist": "General Surgeon / Proctologist",
        "base_severity": "MILD",
        "description": "Swollen veins in the lower rectum and anus, causing discomfort, bleeding, and irritation during bowel movements.",
        "precautions": [
            "Increase dietary fiber intake by eating whole grains, fruits, and vegetables.",
            "Drink 8-10 glasses of water daily to soften stools and prevent straining.",
            "Take warm sitz baths for 15 minutes twice daily.",
            "Avoid sitting for prolonged periods on the toilet."
        ],
        "warning_signs": [
            "Significant or persistent bright red rectal bleeding",
            "Severe, throbbing anal pain (thrombosed hemorrhoid)",
            "Feeling dizzy or faint after bowel movements"
        ]
    },
    "Heart attack": {
        "specialist": "Cardiologist",
        "base_severity": "CRITICAL",
        "description": "A medical emergency where blood flow to a part of the heart muscle is abruptly blocked, starving tissues of oxygen.",
        "precautions": [
            "CRITICAL EMERGENCY: Call an ambulance immediately (Dial 102/112).",
            "Chew one regular aspirin (300mg) while awaiting emergency services if non-allergic.",
            "Sit or lie down in a semi-upright position; loosen tight collar or clothing.",
            "Do NOT attempt to drive yourself to the emergency hospital."
        ],
        "warning_signs": [
            "Crushing, squeezing central chest pressure radiating to left arm, neck, or jaw",
            "Shortness of breath accompanied by cold sweating and clammy skin",
            "Severe lightheadedness, nausea, or sudden loss of consciousness"
        ]
    },
    "Varicose veins": {
        "specialist": "Vascular Surgeon",
        "base_severity": "MILD",
        "description": "Enlarged, twisted, and swollen superficial veins commonly occurring in the legs due to weakened valve function.",
        "precautions": [
            "Wear graduated medical compression stockings as prescribed.",
            "Elevate your legs above heart level when resting or sitting.",
            "Avoid standing or sitting in one place for prolonged uninterrupted periods.",
            "Engage in low-impact walking exercises to improve venous circulation."
        ],
        "warning_signs": [
            "Sudden severe pain, redness, and warm cord-like swelling along the vein",
            "Skin ulceration or breakdown near the ankle",
            "Sudden bleeding from a ruptured varicose vein"
        ]
    },
    "Hypothyroidism": {
        "specialist": "Endocrinologist",
        "base_severity": "MODERATE",
        "description": "An endocrine condition where the thyroid gland does not produce sufficient thyroid hormones, slowing body metabolism.",
        "precautions": [
            "Take levothyroxine medication on an empty stomach with water 30-60 minutes before breakfast.",
            "Get blood TSH and Free T4 levels tested every 6-12 months.",
            "Eat an iodine-sufficient balanced diet and manage weight through exercise.",
            "Avoid taking calcium or iron supplements within 4 hours of thyroid medicine."
        ],
        "warning_signs": [
            "Profound, disabling chronic fatigue and severe cold intolerance",
            "Severe puffy facial edema and slurred speech",
            "Depression, significant memory impairment, or extreme bradycardia (slow heart rate)"
        ]
    },
    "Hyperthyroidism": {
        "specialist": "Endocrinologist",
        "base_severity": "MODERATE",
        "description": "The overproduction of thyroid hormones by the thyroid gland, leading to an accelerated metabolic rate.",
        "precautions": [
            "Take antithyroid medications (methimazole/PTU) consistently as prescribed.",
            "Limit high-iodine foods such as kelp, seaweed, and iodized seafood.",
            "Avoid stimulants like excess caffeine and energy drinks.",
            "Monitor heart rate and blood pressure regularly."
        ],
        "warning_signs": [
            "Thyroid storm signs: extreme fever, rapid irregular heartbeat (tachycardia), agitation",
            "Bulging of the eyes with pain or double vision (Graves' ophthalmopathy)",
            "Tremors so severe they impede holding cups or writing"
        ]
    },
    "Hypoglycemia": {
        "specialist": "Endocrinologist / General Physician",
        "base_severity": "SEVERE",
        "description": "A condition characterized by abnormally low blood glucose levels (under 70 mg/dL), commonly affecting diabetic patients.",
        "precautions": [
            "Follow the 15-15 Rule: Consume 15g fast-acting sugar (fruit juice or candy), recheck in 15 minutes.",
            "Always carry glucose tablets or hard candies with you.",
            "Never skip meals, especially when taking insulin or sulfonylurea drugs.",
            "Wear a medical identification bracelet stating diabetes status."
        ],
        "warning_signs": [
            "Severe confusion, abnormal behavior, or slurred speech",
            "Seizures or convulsions",
            "Loss of consciousness requiring emergency glucagon injection"
        ]
    },
    "Osteoarthristis": {
        "specialist": "Orthopedic Specialist / Rheumatologist",
        "base_severity": "MILD",
        "description": "Degenerative joint disease caused by breakdown of joint cartilage and underlying bone, resulting in joint stiffness and pain.",
        "precautions": [
            "Maintain a healthy weight to reduce mechanical load on weight-bearing joints.",
            "Engage in low-impact activities like swimming, cycling, and water aerobics.",
            "Use supportive walking aids or braces to stabilize knees when needed.",
            "Apply heat packs to relax stiff joints and cold packs to relieve swelling."
        ],
        "warning_signs": [
            "Sudden inability to bear weight on the affected knee or hip",
            "Joint locking or catching during movement",
            "Joint becomes hot, intensely swollen, and red (infection warning)"
        ]
    },
    "Arthritis": {
        "specialist": "Rheumatologist",
        "base_severity": "MODERATE",
        "description": "Inflammation of one or more joints, causing pain, swelling, stiffness, and diminished range of motion.",
        "precautions": [
            "Take disease-modifying antirheumatic drugs (DMARDs) or NSAIDs as directed.",
            "Practice range-of-motion stretching exercises every morning.",
            "Incorporate anti-inflammatory foods rich in omega-3 fatty acids.",
            "Avoid repetitive high-impact stress on inflamed joints."
        ],
        "warning_signs": [
            "Severe morning joint stiffness lasting longer than an hour",
            "Development of subcutaneous rheumatoid nodules or joint deformities",
            "Unexplained fever, systemic weight loss, or eye inflammation"
        ]
    },
    "(vertigo) Paroymsal  Positional Vertigo": {
        "specialist": "ENT Specialist / Neurologist",
        "base_severity": "MILD",
        "description": "An inner ear disorder causing brief episodes of mild to intense spinning dizziness triggered by specific head movements.",
        "precautions": [
            "Learn and perform the Epley canalith repositioning maneuver with guidance.",
            "Avoid sudden, rapid head movements or bending deeply backward.",
            "Sleep with your head elevated on two or more pillows.",
            "Sit on the edge of the bed for a minute before standing up in the morning."
        ],
        "warning_signs": [
            "Dizziness accompanied by double vision, slurred speech, or limb weakness",
            "Sudden profound hearing loss or persistent high-pitched ringing (tinnitus)",
            "Inability to stand or walk without falling"
        ]
    },
    "Acne": {
        "specialist": "Dermatologist",
        "base_severity": "MILD",
        "description": "A common skin condition that occurs when hair follicles become plugged with oil and dead skin cells.",
        "precautions": [
            "Wash face twice daily with a gentle, non-comedogenic cleanser.",
            "Avoid squeezing, picking, or popping pimples to prevent scarring and infection.",
            "Use oil-free, water-based cosmetic products and moisturizers.",
            "Keep hair clean and off your face."
        ],
        "warning_signs": [
            "Deep, painful cystic nodules that fail to respond to topical products",
            "Signs of severe inflammation spreading across large facial areas",
            "Severe emotional distress or social anxiety related to skin appearance"
        ]
    },
    "Urinary tract infection": {
        "specialist": "Urologist / General Physician",
        "base_severity": "MODERATE",
        "description": "An infection in any part of your urinary system (kidneys, ureters, bladder, and urethra), commonly caused by bacteria.",
        "precautions": [
            "Drink plenty of water to flush bacteria out of the urinary tract.",
            "Urinate promptly when you feel the urge; do not hold urine for hours.",
            "Wipe from front to back after bowel movements to prevent bacterial spread.",
            "Complete full course of antibiotics prescribed by your physician."
        ],
        "warning_signs": [
            "High fever, chills, and severe flank or lower back pain (pyelonephritis)",
            "Visible red or cloudy blood in urine",
            "Severe nausea and persistent vomiting"
        ]
    },
    "Psoriasis": {
        "specialist": "Dermatologist",
        "base_severity": "MODERATE",
        "description": "A chronic autoimmune skin disease that speeds up the growth cycle of skin cells, creating scaly, silvery plaques.",
        "precautions": [
            "Keep skin consistently moisturized with heavy ointments or petroleum jelly.",
            "Get brief, supervised exposure to natural sunlight.",
            "Avoid known triggers such as stress, smoking, and skin injuries (Koebner phenomenon).",
            "Use prescribed topical corticosteroids or biologic therapies."
        ],
        "warning_signs": [
            "Erythrodermic flare: widespread fiery redness covering more than 90% of body",
            "Development of swollen, painful, stiff joints (Psoriatic Arthritis)",
            "Secondary bacterial infection of cracked skin plaques"
        ]
    },
    "Impetigo": {
        "specialist": "Dermatologist / Pediatrician",
        "base_severity": "MILD",
        "description": "A common and highly contagious superficial bacterial skin infection, causing honey-colored crusts around the mouth and nose.",
        "precautions": [
            "Gently wash sores with antibacterial soap and warm water.",
            "Apply prescribed topical antibiotic ointment (such as mupirocin) using a clean swab.",
            "Wash patient's clothes, towels, and bed linens daily in hot water.",
            "Do not share personal items with family members until lesions heal."
        ],
        "warning_signs": [
            "Sores spread rapidly or become unusually swollen, tender, and warm",
            "Development of fever or swollen regional lymph glands",
            "Dark, tea-colored urine developing 1-2 weeks after impetigo (post-strep nephritis)"
        ]
    }
}

# Critical Emergency Triage Symptom Clusters
EMERGENCY_RULES = [
    {
        "name": "Acute Cardiac / Coronary Event",
        "required_symptoms": ["chest_pain"],
        "co_symptoms": ["breathlessness", "sweating", "fast_heart_rate", "palpitations", "dizziness"],
        "min_co_symptoms": 1,
        "message": "Immediate Emergency Alert: Severe chest pain with cardiac distress indicators. Seek emergency medical attention (ER/Ambulance) immediately."
    },
    {
        "name": "Acute Cerebrovascular / Stroke Event",
        "required_symptoms": ["weakness_of_one_body_side"],
        "co_symptoms": ["slurred_speech", "altered_sensorium", "loss_of_balance", "headache", "vomiting"],
        "min_co_symptoms": 0,
        "message": "Critical Emergency Alert: Acute unilateral weakness or stroke indicators detected. Call emergency medical services immediately (FAST Protocol)."
    },
    {
        "name": "Severe Respiratory Distress",
        "required_symptoms": ["breathlessness"],
        "co_symptoms": ["fast_heart_rate", "sweating", "chest_pain", "blood_in_sputum"],
        "min_co_symptoms": 2,
        "message": "Emergency Alert: Acute severe respiratory compromise. Emergency oxygenation and medical evaluation required immediately."
    },
    {
        "name": "Critical Unconsciousness / Coma",
        "required_symptoms": ["coma"],
        "co_symptoms": [],
        "min_co_symptoms": 0,
        "message": "Critical Emergency: Patient is unresponsive. Call emergency ambulance immediately."
    },
    {
        "name": "Acute Severe Gastrointestinal Hemorrhage",
        "required_symptoms": ["stomach_bleeding"],
        "co_symptoms": [],
        "min_co_symptoms": 0,
        "message": "Urgent Emergency: Internal gastrointestinal bleeding detected. Immediate hospitalization required."
    }
]
