import re
import random

class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch  # Valeur MIDI
        self.duration = duration

class GenerateurFugue:
    def __init__(self, tonalite="d", mode="minor"):
        self.tonalite = tonalite.lower()
        self.mode = mode.lower()
        
        # Base chromatique pour les calculs de base
        self.chroma = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'bes', 'b']
        self.p_map = {'c':0, 'd':2, 'e':4, 'f':5, 'g':7, 'a':9, 'b':11, 'r':0}
        
        # Générer l'armure et les notes de la gamme choisie
        self.gamme_midi, self.gamme_ly = self._generer_gamme()

    def _generer_gamme(self):
        """ Génère les pitches MIDI (0-11) et les noms LilyPond corrects pour la tonalité """
        intervalles = [0, 2, 4, 5, 7, 9, 11] if self.mode == "major" else [0, 2, 3, 5, 7, 8, 10]
        
        tonique_base = self.p_map.get(self.tonalite[0], 0)
        if "is" in self.tonalite: tonique_base += 1
        if "es" in self.tonalite: tonique_base -= 1
        
        use_flats = self.tonalite in ['f', 'bes', 'es', 'as', 'des', 'g_minor', 'c_minor', 'f_minor', 'd'] and self.mode == "minor"
        
        notes_ly_locales = []
        pitches_midi = []
        
        for degre in intervalles:
            pitch = (tonique_base + degre) % 12
            pitches_midi.append(pitch)
            
            nom_base = self.chroma[pitch]
            if use_flats:
                trad_bemols = {'cis':'des', 'dis':'es', 'fis':'ges', 'gis':'as', 'b':'ces'}
                if nom_base in trad_bemols:
                    nom_base = trad_bemols[nom_base]
            notes_ly_locales.append(nom_base)
            
        return pitches_midi, notes_ly_locales

    def corriger_pitch_diatonique(self, pitch):
        """ Force une note MIDI à atterrir sur la note de la gamme la plus proche """
        if pitch == -1: return -1
        octave = pitch // 12
        note_chroma = pitch % 12
        
        if note_chroma in self.gamme_midi:
            return pitch
        
        proche = min(self.gamme_midi, key=lambda x: min(abs(x - note_chroma), 12 - abs(x - note_chroma)))
        return (octave * 12) + proche

    def parse_ly(self, ly_str):
        pattern = r"([a-g]|r)(is|es)?([',]*)(\d+\.?)?"
        matches = re.findall(pattern, ly_str)
        notes, last_dur = [], "4"
        
        for name, alteration, octs, dur in matches:
            if name == 'r':
                pitch = -1
            else:
                p = self.p_map[name]
                if alteration == "is": p += 1
                if alteration == "es": p -= 1
                if name == 'b' and alteration == 'es': p = 10
                
                pitch = 60 + p + ((octs.count("'") - octs.count(",")) * 12)
                
            if dur: last_dur = dur
            notes.append(Note(pitch, last_dur))
        return notes


    def to_ly_abs(self, notes):
        res = []
        for n in notes:
            if n.pitch == -1:
                res.append(f"r{n.duration}")
                continue
                
            # --- GARDE-FOU: SÉCURITÉ OCTAVE INFÉRIEURE VIOLON ---
            # Le Sol grave du violon est le pitch MIDI 55 (g).
            # Si le pitch est inférieur à 55, on le remonte par tranches de 12 demi-tons (1 octave)
            pitch_ajuste = n.pitch
            while pitch_ajuste < 55:
                pitch_ajuste += 12  # Remonte d'une octave mathématiquement (ce qui ajoutera un "'" plus bas)
            
            pitch_chroma = pitch_ajuste % 12
            
            # 1. Si la note appartient à la gamme de base
            if pitch_chroma in self.gamme_midi:
                idx = self.gamme_midi.index(pitch_chroma)
                nom = self.gamme_ly[idx]
            else:
                # 2. Si la note vient d'une transposition/inversion libre
                nom = self.chroma[pitch_chroma]
                
            # Calcul de l'octave par rapport au Do central (MIDI 60)
            oct_val = (pitch_ajuste // 12) - 5
            oct_str = "'" * oct_val if oct_val >= 0 else "," * abs(oct_val)
            
            res.append(f"{nom}{oct_str}{n.duration}")
        return " ".join(res)
    # --- TRANSFORMATIONS ---
    def transposition(self, notes, intervalle=None):
        if intervalle is None: intervalle = random.choice([-12, -7, -5, 5, 7, 12])
        return [Note((n.pitch + intervalle) if n.pitch != -1 else -1, n.duration) for n in notes]

    def augmentation(self, notes):
        m = {"2":"1", "4":"2", "8":"4", "16":"8", "4.":"2.", "8.":"4."}
        return [Note(self.corriger_pitch_diatonique(n.pitch), m.get(n.duration, n.duration)) for n in notes]

    def diminution(self, notes):
        m = {"1.":"2.", "2.":"4.", "4.":"8.", "8.":"16.","1":"2", "2":"4", "4":"8", "8":"16"}
        return [Note(self.corriger_pitch_diatonique(n.pitch), m.get(n.duration, n.duration)) for n in notes]

    def inversion(self, notes):
        valide_pitches = [n.pitch for n in notes if n.pitch != -1]
        pivot = valide_pitches[0] if valide_pitches else 60
        return [Note((pivot - (n.pitch - pivot)) if n.pitch != -1 else -1, n.duration) for n in notes]

    def retrograde(self, notes): 
        return [Note(self.corriger_pitch_diatonique(n.pitch), n.duration) for n in notes[::-1]]
        
    def hauteurs_retrogrades(self, notes):
        p = [self.corriger_pitch_diatonique(n.pitch) for n in notes][::-1]
        return [Note(p[i], notes[i].duration) for i in range(len(notes))]
        
    def durees_retrogrades(self, notes):
        return [Note(self.corriger_pitch_diatonique(notes[i].pitch), notes[i].duration) for i in range(len(notes))]

    def superposer_echo(self, voix_h):
        res = []
        intervalles_possibles = [0, 3, 4, 5, 7, 8, 9, 12] 
        for n in voix_h:
            if n.pitch == -1:
                res.append(f"r{n.duration}")
                continue
            intervalle = random.choice(intervalles_possibles)
            p_basse = self.corriger_pitch_diatonique(n.pitch - intervalle)
            if p_basse < 55: p_basse = n.pitch 
            
            n_ly = self.to_ly_abs([n]).replace(n.duration, "")
            b_ly = self.to_ly_abs([Note(p_basse, n.duration)]).replace(n.duration, "")
            
            if n.pitch == p_basse: res.append(f"{n_ly}{n.duration}")
            else: res.append(f"<{b_ly} {n_ly}>{n.duration}")
        return " ".join(res)

    def calculer_duree_sequence(self, notes, bpm, unite_bpm="4"):
        total_noires = 0.0
        traduction_noires = {"1": 4.0, "2": 2.0, "4": 1.0, "8": 0.5, "16": 0.25, "2.": 3.0, "4.": 1.5, "8.": 0.75}
        for n in notes:
            total_noires += traduction_noires.get(n.duration, 1.0)
        valeur_pulsation = traduction_noires.get(unite_bpm, 1.0)
        return total_noires * ((60.0 / bpm) / valeur_pulsation)

    def composer(self, theme_ly, bpm, poids_fonctions, poids_combinaisons, duree_cible_secondes, unite_bpm):
        sujet = self.parse_ly(theme_ly)
        
        mapping_fonctions = {
            "transposition": self.transposition, "augmentation": self.augmentation,
            "diminution": self.diminution, "inversion": self.inversion, "retrograde": self.retrograde,
            "hauteurs_retrogrades": self.hauteurs_retrogrades, "durees_retrogrades": self.durees_retrogrades
        }
        
        pool_blocks = []
        
        # 1. Enregistrement des fonctions simples
        for nom_f, nb in poids_fonctions.items():
            if nom_f in mapping_fonctions:
                for _ in range(nb):
                    pool_blocks.append({
                        "name": nom_f,
                        "func": mapping_fonctions[nom_f]
                    })
                
        # 2. Enregistrement des combinaisons (tuples)
        for (f1, f2), nb in poids_combinaisons.items():
            if f1 in mapping_fonctions and f2 in mapping_fonctions:
                for _ in range(nb):
                    func_combo = lambda n, func1=mapping_fonctions[f1], func2=mapping_fonctions[f2]: func1(func2(n))
                    pool_blocks.append({
                        "name": f"{f1}+{f2}",
                        "func": func_combo
                    })
        
        random.shuffle(pool_blocks)
        
        partition = []
        duree_accumulee = 0.0
        
        for block in pool_blocks:
            # Simulation préalable pour le chrono intelligent
            sequence_test = block["func"](sujet)
            duree_bloc = self.calculer_duree_sequence(sequence_test, bpm, unite_bpm)
            
            if duree_accumulee + duree_bloc > duree_cible_secondes + 2:
                # Recherche d'un bloc de secours plus court
                bloc_de_secours = None
                for b_secours in pool_blocks:
                    if b_secours not in partition:
                        seq_secours = b_secours["func"](sujet)
                        duree_secours = self.calculer_duree_sequence(seq_secours, bpm, unite_bpm)
                        if duree_accumulee + duree_secours <= duree_cible_secondes + 2:
                            bloc_de_secours = b_secours
                            break
                
                if bloc_de_secours:
                    block = bloc_de_secours
                    sequence_test = block["func"](sujet)
                    duree_bloc = self.calculer_duree_sequence(sequence_test, bpm, unite_bpm)
                else:
                    break
            
            # Application réelle du bloc
            sequence = block["func"](sujet)
            duree_accumulee += duree_bloc
            
            print(f"% Bloc généré : {block['name']} ({round(duree_bloc, 2)}s) - Cumul : {round(duree_accumulee, 2)}s")
            
            # --- CONDITION INTELLIGENTE POUR LES DOUBLES CORDES ---
            # Si le mot "augmentation" n'estpas dans le nom du bloc (simple ou combiné),
            # on interdit les doubles cordes
            if "augmentation" not in block["name"]:
                partition.append(self.to_ly_abs(sequence))
            else:
                # Sinon, on garde ton hasard habituel (25% de chances de faire un écho)
                partition.append(self.superposer_echo(sequence) if random.random() > 0.75 else self.to_ly_abs(sequence))
            
        print(f"%-> Fugue en {self.tonalite.upper()} {self.mode}. Durée finale : {round(duree_accumulee, 2)}s")
        return " | \n  ".join(partition)

# --- CONFIGURATION TOUTES TONALITÉS ---
TONALITE = "g" 
MODE = "major"
BPM = 100 
DUREE_SOUHAITEE = 30 
TIME = "6/8"
TEMPO="4."

#theme_input = "r8 d'8 e'8 f'8 e'8 f'8 g'8 f'8 g'8 a'8 bes'8 r8" 
#theme_input = "a'8 bes'8 a'8 bes'8 a'8 gis'8 a'8 bes'8 a'8 g'8 f'8 e'8" 
#theme_input = "ees''4. d''8 c''4 bes'4. a'8 g'4 fis'4. g'8 a'4 g'4. bes'8 c''4" 
#theme_input = "bes8 a8 bes8 d'8 c'8 bes8 c'8 ees'8"
#theme_input = "e'8 g'8 a'8 d'8 fis'8 a'8 cis'8 e'8 a'8 d'8 fis'8 a'8"
theme_input = "e'4 b'4 c'8 b' a' g' b'16 a' g' e' a' g' e' ees' e'8 b'8 a'8 g' ees'4 e'4"

# NOMBRE DE FOIS POUR LES FONCTIONS SIMPLES
configuration_fonctions = {
    "transposition": 0, 
    "augmentation": 0, 
    "diminution": 0,
    "inversion": 1, 
    "retrograde": 1, 
    "hauteurs_retrogrades": 0, 
    "durees_retrogrades": 0
}

# NOMBRE DE FOIS POUR LES DOUBLE-TRANSFORMATIONS
# Syntaxe : ("première_action", "deuxième_action"): nombre_de_fois
configuration_combinaisons = {
    ("inversion", "retrograde"): 3,       # L'inversion-rétrograde célèbre de Bach
    ("hauteurs_retrogrades", "inversion"): 1,       # L'inversion-rétrograde célèbre de Bach
    ("transposition", "inversion"): 1,   # Inverse le thème et le transpose (idéal pour les réponses de fugue)
    ("transposition", "augmentation"): 1,   # Inverse le thème et le transpose (idéal pour les réponses de fugue)
    ("transposition", "inversion"): 1,   # Inverse le thème et le transpose (idéal pour les réponses de fugue)
    ("transposition", "retrograde"): 1,   # Inverse le thème et le transpose (idéal pour les réponses de fugue)
    ("transposition", "hauteurs_retrogrades"): 1,   # Inverse le thème et le transpose (idéal pour les réponses de fugue)
    ("retrograde", "augmentation"): 0   # Joue à l'envers deux fois plus lentement
}

generateur = GenerateurFugue(tonalite=TONALITE, mode=MODE)
musique = generateur.composer(
    theme_ly=theme_input, 
    bpm=BPM, 
    poids_fonctions=configuration_fonctions, 
    poids_combinaisons=configuration_combinaisons, 
    duree_cible_secondes=DUREE_SOUHAITEE,
    unite_bpm=TEMPO
)

# --- CODE LILYPOND ---
print(f"""
\\version "2.20.0"
\\header {{ title = "Fugue Diatonique Automatique Avancée" }}
global = {{ \\key {generateur.tonalite} \\{generateur.mode} \\time {TIME} \\tempo {TEMPO}={BPM} }}
\\score {{
  \\new Staff \\with {{ midiInstrument = "violin" }} {{ \\global {musique} \\bar "|." }}
  \\layout {{ }} \\midi {{ }}
}}
""")
