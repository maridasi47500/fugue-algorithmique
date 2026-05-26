\version "2.20.0"

\header {
  title = "Sujet de Fugue Génératif"
  subtitle = "Tonalité et motifs tirés au sort"
  composer = "Dés numériques & Python"
  comment = "Tonalité générée : Mi Majeur"
  tagline = ##f
}


\layout {
  \context {
    \Score
    \remove "Bar_number_engraver"
  }
  \context {
    \Voice
    \consists "Melody_engraver"
    \override Stem #'neutral-direction = #'()
  }
}

global = {

  \clef treble
  \key e \major
  \time 4/4
  \tempo "Andante" 4 = 80
}
violin = \absolute {
  \global

  
  % [Tête du Sujet]
  b'4 e'4 gis'8 a' b' ees' |
  
  % [Queue du Sujet]
  b'16 a' gis' e' a' gis' e' ees' e'8 b'8 |
  
  % [Cadence & Résolution]
  a'8 gis' ees'4 e'4 r4 \bar "||"
}

\score {
  \new Staff \with {
    instrumentName = "Violon"
    midiInstrument = "violin"
  } \violin
  \layout { }
  \midi { }
}

