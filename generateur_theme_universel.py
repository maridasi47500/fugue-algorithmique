import random

# --- DICTIONNAIRE DES TONALITÉS (Calcul des altérations pour LilyPond) ---
TONALITES = {
    # Majeurs
    "c_major":   {"nom": "Do Majeur",     "key": "c \\major",   "root": 0, "is_minor": False},
    "g_major":   {"nom": "Sol Majeur",    "key": "g \\major",   "root": 7, "is_minor": False},
    "d_major":   {"nom": "Ré Majeur",     "key": "d \\major",   "root": 2, "is_minor": False},
    "a_major":   {"nom": "La Majeur",     "key": "a \\major",   "root": 9, "is_minor": False},
    "e_major":   {"nom": "Mi Majeur",     "key": "e \\major",   "root": 4, "is_minor": False},
    "f_major":   {"nom": "Fa Majeur",     "key": "f \\major",   "root": 5, "is_minor": False},
    "b_flat_major": {"nom": "Si bémol Maj", "key": "bes \\major", "root": 10, "is_minor": False},
    "e_flat_major": {"nom": "Mi bémol Maj", "key": "ees \\major", "root": 3, "is_minor": False},
    
    # Mineurs
    "a_minor":   {"nom": "La mineur",     "key": "a \\minor",   "root": 9, "is_minor": True},
    "e_minor":   {"nom": "Mi mineur",     "key": "e \\minor",   "root": 4, "is_minor": True},
    "b_minor":   {"nom": "Si mineur",     "key": "b \\minor",   "root": 11, "is_minor": True},
    "f_sharp_minor": {"nom": "Fa dièse min", "key": "fis \\minor", "root": 6, "is_minor": True},
    "d_minor":   {"nom": "Ré mineur",     "key": "d \\minor",   "root": 2, "is_minor": True},
    "g_minor":   {"nom": "Sol mineur",    "key": "g \\minor",   "root": 7, "is_minor": True},
    "c_minor":   {"nom": "Do mineur",     "key": "c \\minor",   "root": 0, "is_minor": True},
    "f_minor":   {"nom": "Fa mineur",     "key": "f \\minor",   "root": 5, "is_minor": True}
}

# Traduction des demi-tons en notation LilyPond (base en Ré pour le violon/clavier central)
NOTE_MAPPING = {
    0: "c'", 1: "cis'", 2: "d'", 3: "ees'", 4: "e'", 5: "f'",
    6: "fis'", 7: "g'", 8: "gis'", 9: "a'", 10: "bes'", 11: "b'"
}

def obtenir_note(root_value, intervalle_demi_tons):
    """Calcule la note exacte selon l'intervalle par rapport à la tonique."""
    note_index = (root_value + intervalle_demi_tons) % 12
    return NOTE_MAPPING[note_index]

def generer_theme_strict(tonalite_data):
    root = tonalite_data["root"]
    is_min = tonalite_data["is_minor"]
    
    # Définition mathématique des degrés de la gamme
    I = obtenir_note(root, 0)   # Tonique
    III = obtenir_note(root, 3 if is_min else 4) # Tierce (mineure ou majeure)
    IV = obtenir_note(root, 5)  # Sous-dominante
    V = obtenir_note(root, 7)   # Dominante
    VI = obtenir_note(root, 8 if is_min else 9)
    
    # La Note Sensible (VII) : indispensable chez Bach, toujours majeure en mineur !
    SENSIBLE = obtenir_note(root, 11) 
    
    # Octaves supérieures pour fluidifier la mélodie
    I_haut = I + "'"
    V_haut = V + "'"
    IV_haut = IV + "'"
    
    # --- STRUCTURE ALÉATOIRE DES BLOCS DE L'ANATOMIE BAROQUE ---
    
    # 1. Profil de la Tête (Sauts d'intervalles)
    tetes = [
        f"{I}4 {V}4 {VI}8 {V} {IV} {III}",  # Début classique (I -> V)
        f"{I}4 {I_haut}4 {SENSIBLE}8 {I_haut} {V}4", # Saut d'octave dramatique
        f"{V}4 {I}4 {III}8 {IV} {V} {SENSIBLE}" # Attaque sur la dominante
    ]
    tete = random.choice(tetes)
    
    # 2. Profil de la Queue (Mouvement conjoint rapide)
    queues = [
        f"{IV}16 {III} {I} {V} {SENSIBLE} {I} {III} {IV} {V}8 {III}8",
        f"{V}16 {IV} {III} {I} {IV} {III} {I} {SENSIBLE} {I}8 {V}8",
        f"{I_haut}16 {SENSIBLE} {V} {IV} {III} {IV} {V} {I} {IV}8 {SENSIBLE}8"
    ]
    queue = random.choice(queues)
    
    # 3. Profil de la Cadence (Préparation et Résolution)
    cadences = [
        f"{IV}8 {III} {SENSIBLE}4 {I}4 r4",
        f"{VI}8 {V} {SENSIBLE}4 {I}2",
        f"{I_haut}8 {V} {SENSIBLE}4 {I}4 r4"
    ]
    cadence = random.choice(cadences)

    # Assemblage du code LilyPond final
    code_ly = f"""\\version "2.20.0"

\\header {{
  title = "Sujet de Fugue Génératif"
  subtitle = "Tonalité et motifs tirés au sort"
  composer = "Dés numériques & Python"
  comment = "Tonalité générée : {tonalite_data['nom']}"
  tagline = ##f
}}


\\layout {{
  \\context {{
    \\Score
    \\remove "Bar_number_engraver"
  }}
  \\context {{
    \\Voice
    \\consists "Melody_engraver"
    \\override Stem #'neutral-direction = #'()
  }}
}}

global = {{

  \\clef treble
  \\key {tonalite_data['key']}
  \\time 4/4
  \\tempo "Andante" 4 = 80
}}
violin = \\absolute {{
  \\global

  
  % [Tête du Sujet]
  {tete} |
  
  % [Queue du Sujet]
  {queue} |
  
  % [Cadence & Résolution]
  {cadence} \\bar "||"
}}

\\score {{
  \\new Staff \\with {{
    instrumentName = "Violon"
    midiInstrument = "violin"
  }} \\violin
  \\layout {{ }}
  \\midi {{ }}
}}

"""
    return code_ly

if __name__ == "__main__":
    # Sélection aléatoire d'une tonalité parmi les 16 programmées
    id_tonalite = random.choice(list(TONALITES.keys()))
    tonalite_choisie = TONALITES[id_tonalite]
    
    nom_fichier = "theme_aleatoire_universel.ly"
    
    # Écriture du fichier .ly
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(generer_theme_strict(tonalite_choisie))
        
    print(f"🎲 Tonalité sélectionnée : {tonalite_choisie['nom']}")
    print(f"🎵 Le thème de fugue a été écrit dans '{nom_fichier}' !")
    print("-> Copiez le texte de ce fichier sur https://www.lilybin.com pour voir la partition dessinée et l'écouter.")
