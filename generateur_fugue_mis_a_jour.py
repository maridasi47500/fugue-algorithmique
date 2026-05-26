import re
import random

class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch  # MIDI
        self.duration = duration # String ("4", "8", "2", "4.", "r8" etc.)

class GenerateurFugue:
    def __init__(self, tonalite="d", mode="minor"):
        self.tonalite = tonalite
        self.mode = mode
        self.notes_ly = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']

    def parse_ly(self, ly_str):
        # Capturer aussi les silences 'r' comme des notes spéciales (pitch fixe ou ignoré pour les hauteurs)
        pattern = r"([a-g]|r)(?:is|es)?([',]*)(\d+\.?)?"
        matches = re.findall(pattern, ly_str)
        notes, last_dur = [], "4"
        p_map = {'c':0, 'd':2, 'e':4, 'f':5, 'g':7, 'a':9, 'b':11, 'r':0}
        for name, octs, dur in matches:
            p = p_map[name[0]]
            if "is" in name: p += 1
            if "es" in name: p -= 1
            pitch = 60 + p + ((octs.count("'") - octs.count(",")) * 12)
            if name == 'r':
                pitch = -1 # Signifie un silence
            if dur: last_dur = dur
            notes.append(Note(pitch, last_dur))
        return notes

    def to_ly_abs(self, notes):
        res = []
        for n in notes:
            if n.pitch == -1:
                res.append(f"r{n.duration}")
                continue
            nom = self.notes_ly[n.pitch % 12]
            oct_val = (n.pitch // 12) - 5
            oct_str = "'" * oct_val if oct_val >= 0 else "," * abs(oct_val)
            res.append(f"{nom}{oct_str}{n.duration}")
        return " ".join(res)

    # --- TRANSFORMATIONS DE BASE ---
    def transposition(self, notes, intervalle=None):
        if intervalle is None: intervalle = random.choice([-12, -5, 5, 7, 12])
        return [Note(n.pitch + intervalle if n.pitch != -1 else -1, n.duration) for n in notes]

    def augmentation(self, notes):
        m = {"2":"1", "4":"2", "8":"4", "16":"8", "4.":"2.", "8.":"4."}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def diminution(self, notes):
        m = {"1":"2", "2":"4", "4":"8", "8":"16"}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def inversion(self, notes):
        # Trouver le premier vrai pitch qui n'est pas un silence pour le pivot
        valide_pitches = [n.pitch for n in notes if n.pitch != -1]
        pivot = valide_pitches[0] if valide_pitches else 60
        return [Note(pivot - (n.pitch - pivot) if n.pitch != -1 else -1, n.duration) for n in notes]

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
        res = []
        intervalles_possibles = [0, 3, 4, 5, 7, 8, 9, 10, 12] 
        for n in voix_h:
            if n.pitch == -1:
                res.append(f"r{n.duration}")
                continue
            intervalle = random.choice(intervalles_possibles)
            p_basse = n.pitch - intervalle
            if p_basse < 55: p_basse = n.pitch 
            
            n_ly = self.to_ly_abs([n]).replace(n.duration, "")
            b_ly = self.to_ly_abs([Note(p_basse, n.duration)]).replace(n.duration, "")
            
            if n.pitch == p_basse: res.append(f"{n_ly}{n.duration}")
            else: res.append(f"<{b_ly} {n_ly}>{n.duration}")
        return " ".join(res)

    # --- CALCUL DE DURÉE ---
    def calculer_duree_sequence(self, notes, bpm):
        """ Calcule la durée d'une séquence de notes en secondes selon le BPM """
        total_noires = 0.0
        traduction_noires = {"1": 4.0, "2": 2.0, "4": 1.0, "8": 0.5, "16": 0.25,
                             "2.": 3.0, "4.": 1.5, "8.": 0.75}
        for n in notes:
            total_noires += traduction_noires.get(n.duration.replace("r", ""), 1.0)
        
        temps_par_noire = 60.0 / bpm
        return total_noires * temps_par_noire

    # --- COMPOSITEUR REVISITÉ ---
    def composer(self, theme_ly, bpm, poids_fonctions, duree_cible_secondes):
        sujet = self.parse_ly(theme_ly)
        
        # 1. Générer le pool de transformations de base demandées par l'utilisateur
        pool_fonctions_base = []
        mapping_fonctions = {
            "transposition": self.transposition,
            "augmentation": self.augmentation,
            "diminution": self.diminution,
            "inversion": self.inversion,
            "retrograde": self.retrograde,
            "hauteurs_retrogrades": self.hauteurs_retrogrades,
            "durees_retrogrades": self.durees_retrogrades
        }
        
        for nom_f, nb in poids_fonctions.items():
            if nom_f in mapping_fonctions:
                pool_fonctions_base.extend([mapping_fonctions[nom_f]] * nb)
        
        random.shuffle(pool_fonctions_base)
        
        # 2. Définir les combinaisons musicales intelligentes
        combinaisons_musicales = [
            lambda n: self.inversion(self.retrograde(n)),             # Inversion-Rétrograde
            lambda n: self.inversion(self.augmentation(n)),           # Inversion Augmentée
            lambda n: self.transposition(self.inversion(n)),          # Transposition de l'inversion
            lambda n: self.transposition(self.retrograde(n)),         # Transposition du rétrograde
            lambda n: self.hauteurs_retrogrades(self.augmentation(n)) # Rétrograde mélodique lent
        ]
        
        partition = []
        duree_accumulee = 0.0
        
        # Appliquer d'abord toutes les fonctions de base demandées
        for transf in pool_fonctions_base:
            sequence = transf(sujet)
            duree_seq = self.calculer_duree_sequence(sequence, bpm)
            
            if duree_accumulee + duree_seq > duree_cible_secondes:
                break
                
            duree_accumulee += duree_seq
            if random.random() > 0.75:
                partition.append(self.superposer_echo(sequence))
            else:
                partition.append(self.to_ly_abs(sequence))
                
        # 3. Si la durée cible n'est pas atteinte, on complète avec les combinaisons de fonctions (1 fois max par combinaison)
        random.shuffle(combinaisons_musicales)
        for combo in combinaisons_musicales:
            if duree_accumulee >= duree_cible_secondes:
                break
                
            sequence = combo(sujet)
            duree_seq = self.calculer_duree_sequence(sequence, bpm)
            
            if duree_accumulee + duree_seq <= duree_cible_secondes + 2: # Marge de 2 secondes
                duree_accumulee += duree_seq
                if random.random() > 0.75:
                    partition.append(self.superposer_echo(sequence))
                else:
                    partition.append(self.to_ly_abs(sequence))

        print(f"-> Durée totale estimée de la pièce : {round(duree_accumulee, 2)} secondes ({len(partition)} blocs utilisés).")
        return " | \n  ".join(partition)

# --- CONFIGURATION ET PARAMÈTRES ---
#theme_input = "r8 d'8 e'8 f'8 g'8 a'8 bes'8 c''8 d''8 g8 a8 bes c'8 bes8 c'8 d'8 e'8" 
theme_input = "r8 d'8 e'8 f'8 g'8 f'8 g'8 a'8 ais'8" 
BPM = 120
DUREE_SOUHAITEE = 45  # Durée de la fugue en secondes

# Ici, tu choisis EXACTEMENT le nombre de fois que chaque fonction de base doit apparaître
configuration_fonctions = {
    "transposition": 3,
    "augmentation": 2,
    "diminution": 2,
    "inversion": 4,
    "retrograde": 2,
    "hauteurs_retrogrades": 1,
    "durees_retrogrades": 1
}

generateur = GenerateurFugue(tonalite="d", mode="minor")
musique = generateur.composer(theme_input, bpm=BPM, poids_fonctions=configuration_fonctions, duree_cible_secondes=DUREE_SOUHAITEE)

# --- SORTIE LILYPOND ---
lilypond_final = f"""\\version "2.24.3"
\\header {{
  title = "Fugue Algorithmique Structurée"
  composer = "Python & Contrepoint"
  tagline = ##f
}}
\\paper {{ #(set-paper-size "a4") }}
\\layout {{
  \\context {{ \\Score \\remove "Bar_number_engraver" }}
  \\context {{ \\Voice \\consists "Melody_engraver" \\override Stem.neutral-direction = #'() }}
}}
global = {{ \\key {generateur.tonalite} \\{generateur.mode} \\time 4/4 \\tempo 4={BPM} }}

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

print("\n--- CODE LILYPOND GÉNÉRÉ ---")
print(lilypond_final)
