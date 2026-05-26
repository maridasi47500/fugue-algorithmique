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
        # Intervalles des gammes
        intervalles = [0, 2, 4, 5, 7, 9, 11] if self.mode == "major" else [0, 2, 3, 5, 7, 8, 10]
        
        # Trouver la tonique de base
        tonique_base = self.p_map.get(self.tonalite[0], 0)
        if "is" in self.tonalite: tonique_base += 1
        if "es" in self.tonalite: tonique_base -= 1
        
        # Choix intelligent des altérations selon la tonalité
        # Si la tonalité utilise des bémols (Fa majeur, Ré mineur, etc.)
        use_flats = self.tonalite in ['f', 'bes', 'es', 'as', 'des', 'g_minor', 'c_minor', 'f_minor', 'd'] and self.mode == "minor"
        
        notes_ly_locales = []
        pitches_midi = []
        
        for degre in intervalles:
            pitch = (tonique_base + degre) % 12
            pitches_midi.append(pitch)
            
            # Nom de la note LilyPond
            nom_base = self.chroma[pitch]
            if use_flats:
                # Convertir les dièses en bémols équivalents si nécessaire
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
        
        # Si la note est hors-gamme (à cause d'une inversion/transposition), on prend la plus proche
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
                
            pitch_chroma = n.pitch % 12
            
            # 1. Si la note appartient à la gamme de base, on prend son nom officiel dans la gamme
            if pitch_chroma in self.gamme_midi:
                idx = self.gamme_midi.index(pitch_chroma)
                nom = self.gamme_ly[idx]
            else:
                # 2. Si la note vient d'une transposition/inversion libre, on utilise la liste chromatique par défaut
                nom = self.chroma[pitch_chroma]
                
            oct_val = (n.pitch // 12) - 5
            oct_str = "'" * oct_val if oct_val >= 0 else "," * abs(oct_val)
            res.append(f"{nom}{oct_str}{n.duration}")
        return " ".join(res)

    # --- TRANSFORMATIONS ---
    def transposition(self, notes, intervalle=None):
        # Transposition par degrés de la gamme (ici conversion simple mais sécurisée par la correction)
        if intervalle is None: intervalle = random.choice([-12, -7, -5, 5, 7, 12])
        return [Note((n.pitch + intervalle) if n.pitch != -1 else -1, n.duration) for n in notes]

    def augmentation(self, notes):
        m = {"2":"1", "4":"2", "8":"4", "16":"8", "4.":"2.", "8.":"4."}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def diminution(self, notes):
        m = {"1":"2", "2":"4", "4":"8", "8":"16"}
        return [Note(n.pitch, m.get(n.duration, n.duration)) for n in notes]

    def inversion(self, notes):
        valide_pitches = [n.pitch for n in notes if n.pitch != -1]
        pivot = valide_pitches[0] if valide_pitches else 60
        return [Note((pivot - (n.pitch - pivot)) if n.pitch != -1 else -1, n.duration) for n in notes]

    def retrograde(self, notes): return notes[::-1]
    def hauteurs_retrogrades(self, notes):
        p = [n.pitch for n in notes][::-1]
        return [Note(p[i], notes[i].duration) for i in range(len(notes))]
    def durees_retrogrades(self, notes):
        d = [n.duration for n in notes][::-1]
        return [Note(notes[i].pitch, d[i]) for i in range(len(notes))]

    def superposer_echo(self, voix_h):
        res = []
        # Intervalles consonants par rapport à la gamme (tierce, quarte, quinte, sixte, octave)
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

    def calculer_duree_sequence(self, notes, bpm):
        total_noires = 0.0
        traduction_noires = {"1": 4.0, "2": 2.0, "4": 1.0, "8": 0.5, "16": 0.25, "2.": 3.0, "4.": 1.5, "8.": 0.75}
        for n in notes:
            total_noires += traduction_noires.get(n.duration, 1.0)
        return total_noires * (60.0 / bpm)

    def composer(self, theme_ly, bpm, poids_fonctions, duree_cible_secondes):
        sujet = self.parse_ly(theme_ly)
        pool_fonctions_base = []
        mapping_fonctions = {
            "transposition": self.transposition, "augmentation": self.augmentation,
            "diminution": self.diminution, "inversion": self.inversion, "retrograde": self.retrograde,
            "hauteurs_retrogrades": self.hauteurs_retrogrades, "durees_retrogrades": self.durees_retrogrades
        }
        for nom_f, nb in poids_fonctions.items():
            if nom_f in mapping_fonctions: pool_fonctions_base.extend([mapping_fonctions[nom_f]] * nb)
        
        random.shuffle(pool_fonctions_base)
        partition = []
        duree_accumulee = 0.0
        
        for transf in pool_fonctions_base:
            # AJUSTEMENT : On vérifie SI on a déjà dépassé le temps AVANT d'ajouter un bloc entier
            if duree_accumulee >= duree_cible_secondes: 
                break
                
            sequence = transf(sujet)
            duree_seq = self.calculer_duree_sequence(sequence, bpm)
            
            # On ajoute TOUJOURS la séquence entière pour ne pas couper le rythme au milieu
            duree_accumulee += duree_seq
            partition.append(self.superposer_echo(sequence) if random.random() > 0.75 else self.to_ly_abs(sequence))
            
        print(f"%-> Fugue en {self.tonalite.upper()} {self.mode}. Durée finale : {round(duree_accumulee, 2)}s")
        return " | \n  ".join(partition)

# --- CONFIGURATION TOUTES TONALITÉS ---
# Change ici pour tester n'importe quelle tonalité !
# Exemples : ("c", "major"), ("g", "minor"), ("a", "minor"), ("f", "major")...
TONALITE = "a" 
MODE = "minor"
BPM = 120
DUREE_SOUHAITEE = 30 

theme_input = "r8 d'8 e'8 f'8 e'8 f'8 g'8 f'8 g'8 a'8 bes'8 r8" 

configuration_fonctions = {
    "transposition": 3, "augmentation": 1, "diminution": 1,
    "inversion": 1, "retrograde": 1, "hauteurs_retrogrades": 1, "durees_retrogrades": 1
}

generateur = GenerateurFugue(tonalite=TONALITE, mode=MODE)
musique = generateur.composer(theme_input, bpm=BPM, poids_fonctions=configuration_fonctions, duree_cible_secondes=DUREE_SOUHAITEE)

# --- CODE LILYPOND ---
print(f"""
\\version "2.20.0"
\\header {{ title = "Fugue Diatonique Automatique" }}
global = {{ \\key {generateur.tonalite} \\{generateur.mode} \\time 4/4 \\tempo 4={BPM} }}
\\score {{
  \\new Staff \\with {{ midiInstrument = "violin" }} {{ \\global {musique} \\bar "|." }}
  \\layout {{ }} \\midi {{ }}
}}
""")
