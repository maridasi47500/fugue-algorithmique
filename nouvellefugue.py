import random

def generer_sujet_aleatoire():
    """Génère un motif de sujet aléatoire mais structurellement cohérent en Sol mineur."""
    # Listes de briques mélodiques typiques de Bach (mesures de 4/4)
    debuts = [
        "g4 d' bes8 a g fis",   # Profil classique rythmé
        "g8 d g bes a d fis c'", # Arpège brisé ascendant
        "g4 g'8 f es d c b"     # Descente dramatique
    ]
    fins = [
        "g4 r r2",
        "g8[ fis g a] b4 r",
        "g4 d8[ c] b[ a] g4"
    ]
    
    # Choix aléatoire des morceaux du puzzle
    sujet = f"{random.choice(debuts)} | {random.choice(fins)}"
    return sujet

def generer_bariolage_aleatoire():
    """Génère de façon procédurale une section de bariolage pour violon."""
    # Notes de mélodie possibles dans le haut du violon
    notes_melodie = ["g'", "fis'", "f'", "e'", "es'", "d'", "c'", "bes", "a"]
    corde_a_vide = "d" # Le Ré est parfait pour le bariolage au violon
    
    corps_bariolage = ""
    # On génère 16 doubles-croches aléatoires alternées avec la corde à vide
    for _ in range(8):
        note_choisie = random.choice(notes_melodie)
        corps_bariolage += f"{note_choisie}8 {corde_a_vide} "
        
    return corps_bariolage

def creer_code_lilypond():
    sujet = generer_sujet_aleatoire()
    bariolage_1 = generer_bariolage_aleatoire()
    bariolage_2 = generer_bariolage_aleatoire()
    
    # Choix d'un accord final riche parmi ceux possibles au violon
    accords_finaux = [
        "<g,, d' b-'' g''>1\\fermata", # Sol mineur complet
        "<g,, d' b-'>1\\fermata",      # Plus épuré
        "<g,, d' b'' g''>1\\fermata"   # Tierce majeure (Tierce de Picardie !)
    ]
    accord_final = random.choice(accords_finaux)

    code_ly = f"""\\version "2.24.0"

\\header {{
  title = "Fugue Aléatoire pour Violon Seul"
  subtitle = "Générée procéduralement dans le style de Bach"
  composer = "Dés à coudre & Python"
  tagline = ##f
}}

violonMusic = \\relative c' {{
  \\clef treble
  \\key g \\minor
  \\time 4/4
  \\tempo "Moderato" 4 = 90

  % --- 1. LE SUJET ALÉATOIRE ---
  {sujet} |
  
  % --- 2. L'EXPOSITION DE LA RÉPONSE (2 voix LilyPond) ---
  <<
    \\new Voice {{
      \\voiceOne
      % Réponse transposée (simulation de quinte)
      a'4 f'8 e d cis d4 |
      g8 f e d c b c4 |
    }}
    \\new Voice {{
      \\voiceTwo
      % Basse d'impact au violon
      <g, d'>4 r r2 |
      c4 r r2 |
    }}
  >> \\oneVoice
  
  % --- 3. LE DIVERTISSEMENT (Bariolage généré note par note) ---
  {bariolage_1} |
  {bariolage_2} |
  
  % --- 4. ACCORD FINAL ---
  {accord_final} |
}}

\\score {{
  \\new Staff \\with {{
    midiInstrument = "violin"
  }} {{
    \\violonMusic
  }}
  \\layout {{ }}
  \\midi {{ }}
}}
"""
    return code_ly

if __name__ == "__main__":
    nom_fichier = "fugue_aleatoire.ly"
    
    # Génération et écriture du fichier
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(creer_code_lilypond())
        
    print(f"🎲 Une nouvelle fugue unique vient d'être compilée dans '{nom_fichier}' !")
    print("Relancez le script pour obtenir une variation complètement différente.")
    print("-> Copiez le texte du fichier sur https://www.lilybin.com pour voir la partition et l'écouter.")
