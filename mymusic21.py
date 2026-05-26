from music21 import stream, note, chord, meter, key, duration, environment

def creer_fugue_violon():
    # 1. Initialisation de la partition pour Violon
    score = stream.Score()
    part = stream.Part()
    part.id = 'Violon'
    
    # Configuration de la mesure (4/4) et de la tonalité (Sol mineur)
    part.append(meter.TimeSignature('4/4'))
    part.append(key.KeySignature(-2)) # 2 bémols à la clé = Sol mineur / Si bémol Majeur
    
    # -------------------------------------------------------------------------
    # ÉTAPE 1 : Le Sujet (Solo, sans accompagnement, profil rythmique clair)
    # Inspiré du sujet de la BWV 1001 de Bach (court et incisif)
    # -------------------------------------------------------------------------
    sujet_notes = [
        ('G4', 'quarter'),  # Sol
        ('D5', 'quarter'),  # Ré
        ('B-4', 'eighth'),  # Si bémol
        ('A4', 'eighth'),   # La
        ('G4', 'eighth'),   # Sol
        ('F#4', 'eighth'),  # Fa dièse (note sensible)
        ('G4', 'quarter'),  # Sol
    ]
    
    for pitch, dur in sujet_notes:
        n = note.Note(pitch)
        n.duration = duration.Duration(dur)
        part.append(n)
        
    # -------------------------------------------------------------------------
    # ÉTAPE 2 : La Réponse (à la quinte) + Illusion polyphonique
    # Pendant que la voix supérieure commence la réponse en Ré mineur, 
    # on simule une basse en utilisant un accord sur le premier temps.
    # -------------------------------------------------------------------------
    
    # Mesure 3 : Accord d'entrée pour poser la basse, suivi de la Réponse
    # Accord Sol-Ré-Sib (Typique du violon chez Bach)
    accord_initial = chord.Chord(['G3', 'D4', 'B-4'])
    accord_initial.duration = duration.Duration('quarter')
    part.append(accord_initial)
    
    # Suite de la réponse à la quinte (en Ré mineur / majeur de Bach)
    reponse_notes = [
        ('A4', 'quarter'),   # La
        ('F5', 'eighth'),    # Fa
        ('E5', 'eighth'),    # Mi
        ('D5', 'eighth'),    # Ré
        ('C#5', 'eighth'),   # Do dièse
        ('D5', 'quarter'),   # Ré
    ]
    
    for pitch, dur in reponse_notes:
        n = note.Note(pitch)
        n.duration = duration.Duration(dur)
        part.append(n)

    # -------------------------------------------------------------------------
    # ÉTAPE 3 : Le Divertissement / Bariolage (Illusion d'optique acoustique)
    # On alterne rapidement entre une note de mélodie et une corde à vide (Ré4)
    # -------------------------------------------------------------------------
    bariolage_notes = [
        ('G5', 'eighth'), ('D4', 'eighth'),  # Note de mélodie + Corde à vide Ré
        ('F#5', 'eighth'), ('D4', 'eighth'),
        ('G5', 'eighth'), ('D4', 'eighth'),
        ('A5', 'eighth'), ('D4', 'eighth'),
        ('B-5', 'eighth'), ('D4', 'eighth'),
        ('A5', 'eighth'), ('D4', 'eighth'),
        ('G5', 'eighth'), ('D4', 'eighth'),
        ('F#5', 'eighth'), ('D4', 'eighth'),
    ]
    
    for pitch, dur in bariolage_notes:
        n = note.Note(pitch)
        n.duration = duration.Duration(dur)
        part.append(n)

    # Note finale de résolution
    note_finale = chord.Chord(['G3', 'D4', 'B-4', 'G5']) # Splendide accord final à 4 cordes
    note_finale.duration = duration.Duration('half')
    part.append(note_finale)

    score.append(part)
    return score

if __name__ == '__main__':
    print("Composition de la fugue de Bach pour violon seul en cours...")
    fugue = creer_fugue_violon()
    
    # Sauvegarde en fichier MIDI (pour l'écouter)
    fichier_midi = 'fugue_violon_bach.mid'
    fugue.write('midi', fp=fichier_midi)
    print(f"-> Fichier MIDI enregistré : {fichier_midi}")
    
    # Sauvegarde en MusicXML (pour l'ouvrir dans MuseScore / Sibelius)
    fichier_xml = 'fugue_violon_bach.musicxml'
    fugue.write('musicxml', fp=fichier_xml)
    print(f"-> Fichier MusicXML enregistré : {fichier_xml}")
    print("Vous pouvez maintenant ouvrir le fichier .musicxml dans votre éditeur de partition préféré !")
