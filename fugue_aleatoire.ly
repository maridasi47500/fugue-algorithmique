\version "2.24.0"

\header {
  title = "Fugue Aléatoire pour Violon Seul"
  subtitle = "Générée procéduralement dans le style de Bach"
  composer = "Dés à coudre & Python"
  tagline = ##f
}

violonMusic = \relative c' {
  \clef treble
  \key g \minor
  \time 4/4
  \tempo "Moderato" 4 = 90

  % --- 1. LE SUJET ALÉATOIRE ---
  g8 d g bes a d fis c' | g4 r r2 |
  
  % --- 2. L'EXPOSITION DE LA RÉPONSE (2 voix LilyPond) ---
  <<
    \new Voice {
      \voiceOne
      % Réponse transposée (simulation de quinte)
      a'4 f'8 e d cis d4 |
      g8 f e d c b c4 |
    }
    \new Voice {
      \voiceTwo
      % Basse d'impact au violon
      <g, d'>4 r r2 |
      c4 r r2 |
    }
  >> \oneVoice
  
  % --- 3. LE DIVERTISSEMENT (Bariolage généré note par note) ---
  bes8 d fis'8 d f'8 d g'8 d f'8 d d'8 d bes8 d e'8 d  |
  g'8 d es'8 d c'8 d f'8 d es'8 d g'8 d f'8 d d'8 d  |
  
  % --- 4. ACCORD FINAL ---
  <g,, d' b-'' g''>1\fermata |
}

\score {
  \new Staff \with {
    midiInstrument = "violin"
  } {
    \violonMusic
  }
  \layout { }
  \midi { }
}
