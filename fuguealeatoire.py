import re
import random

class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch  # MIDI
        self.duration = duration # String (4, 8, 2, etc.)

class GenerateurFugue:
    def __init__(self, tonalite="d", mode="minor"):
        self.tonalite = tonalite
        self.mode = mode
        self.notes_ly = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']

    def parse_ly(self, ly_str):
        pattern = r"([a-g](?:is|es)?)([',]*)(\d+\.?)?"
        matches = re.findall(pattern, ly_str)
        notes, last_dur = [], "4"
        p_map = {'c':0, 'd':2, 'e':4, 'f':5, 'g':7, 'a':9, 'b':11}
        for name, octs, dur in matches:
            p = p_map[name[0]]
            if "is" in name: p += 1
            if "es" in name: p -= 1
            pitch = 60 + p + ((octs.count("'") - octs.count(",")) * 12)
            if dur: last_dur = dur
            notes.append(Note(pitch, last_dur))
        return notes

    def to_ly_abs(self, notes):
        res = []
        for n in notes:
            nom = self.notes_ly[n.pitch % 12]
            oct_val = (n.pitch // 12) - 5
            oct_str = "'" * oct_val if oct_val >= 0 else "," * abs(oct_val)
            res.append(f"{nom}{oct_str}{n.duration}")
        return " ".join(res)

    # --- TRANSFORMATIONS ---
    def transposition(self, notes, intervalle=None):
        if intervalle is None: intervalle = random.choice([-12, -5, 5, 7, 12])
        return [Note(n.pitch + intervalle, n.duration) for n in notes]

    def augmentation(self, notes):
        m = {"2":"1", "4":"2", "8":"4", "16":"8"}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def diminution(self, notes):
        m = {"1":"2", "2":"4", "4":"8", "8":"16"}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def inversion(self, notes):
        pivot = notes[0].pitch
        return [Note(pivot - (n.pitch - pivot), n.duration) for n in notes]

    def retrograde(self, notes):
        return notes[::-1]

    def hauteurs_retrogrades(self, notes):
        p = [n.pitch for n in notes][::-1]
        return [Note(p[i], notes[i].duration) for i in range(len(notes))]

    def durees_retrogrades(self, notes):
        d = [n.duration for n in notes][::-1]
        return [Note(notes[i].pitch, d[i]) for i in range(len(notes))]

    # --- LOGIQUE VIOLON & DOUBLES CORDES ---
    def superposer_echo(self, voix_h):
        """ Crée des doubles cordes avec un écart aléatoire jouable (quinte, sixte, octave...) """
        res = []
        # Intervalles de doubles cordes classiques au violon (en demi-tons)
        intervalles_possibles = [0, 3, 4, 5, 7, 8, 9, 10, 12] 
        
        for n in voix_h:
            intervalle = random.choice(intervalles_possibles)
            p_basse = n.pitch - intervalle
            # Limite physique : Sol grave du violon (MIDI 55)
            if p_basse < 55: p_basse = n.pitch 
            
            n_ly = self.to_ly_abs([n]).replace(n.duration, "")
            b_ly = self.to_ly_abs([Note(p_basse, n.duration)]).replace(n.duration, "")
            
            if n.pitch == p_basse: res.append(f"{n_ly}{n.duration}")
            else: res.append(f"<{b_ly} {n_ly}>{n.duration}")
        return " ".join(res)

    def composer(self, theme_ly):
        sujet = self.parse_ly(theme_ly)
        fonctions = [self.transposition, self.augmentation, self.diminution, 
                     self.inversion, self.retrograde, self.hauteurs_retrogrades, 
                     self.durees_retrogrades]
        
        # Longueur aléatoire : entre 20 et 40 blocs de transformations
        longueur = random.randint(20, 40)
        partition = []
        
        print(f"Génération d'une partition de {longueur} séquences...")

        for _ in range(longueur):
            # On choisit une transformation au hasard
            transf = random.choice(fonctions)
            # On applique la transformation sur le sujet
            sequence = transf(sujet)
            
            # Aléatoirement, on décide si on joue en notes simples ou en doubles cordes
            if random.random() > 0.7:
                partition.append(self.superposer_echo(sequence))
            else:
                partition.append(self.to_ly_abs(sequence))
        
        return " | \n  ".join(partition)

# --- CONFIGURATION ET SORTIE ---
theme_input = "r8 d'8 e'8 f'8 g'8 a'8 bes'8 c''8 d''8 g8 a8 bes c'8 bes8 c'8 d'8 e'8" # Sujet initial
generateur = GenerateurFugue(tonalite="d", mode="minor")
musique = generateur.composer(theme_input)

lilypond_final = f"""\\version "2.24.3"
\\header {{
  title = "Fugue Aléatoire pour Violon Seul"
  composer = "Script Python"
  tagline = ##f
}}
\\paper {{ #(set-paper-size "a4") }}
\\layout {{
  \\context {{ \\Score \\remove "Bar_number_engraver" }}
  \\context {{ \\Voice \\consists "Melody_engraver" \\override Stem.neutral-direction = #'() }}
}}
global = {{ \\key {generateur.tonalite} \\{generateur.mode} \\time 4/4 \\tempo 4=110 }}

violin = {{
  \\global
  {musique}
  \\bar "|."
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

print("\n--- COPIEZ LE CODE CI-DESSOUS DANS LILYPOND ---")
print(lilypond_final)
