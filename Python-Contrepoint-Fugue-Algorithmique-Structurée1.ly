\version "2.20.0"
\header { title = "Fugue Diatonique Automatique Avancée" }
global = { \key a \minor \time 4/4 \tempo 4=120 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global r8 a'8 g'8 fis'8 g'8 fis'8 e'8 fis'8 e'8 d'8 cis'8 r8 | 
  r8 d''8 c''8 b'8 c''8 b'8 a'8 b'8 a'8 g'8 fis'8 r8 | 
  r8 a8 b8 c'8 b8 c'8 d'8 c'8 d'8 e'8 f'8 r8 | 
  r4 <f' a'>4 <a' b'>4 <f' c''>4 <a' b'>4 <e' c''>4 <a' d''>4 <d' c''>4 <a' d''>4 <b' e''>4 <b' e''>4 r4 | 
  r8 a8 b8 c'8 b8 c'8 d'8 c'8 d'8 e'8 f'8 r8 | 
  r8 <b, g>8 <d a>8 <c bes>8 <c a>8 <f bes>8 <d c'>8 <a, bes>8 <a c'>8 <f d'>8 <b dis'>8 r8 | 
  r8 g8 a8 bes8 a8 bes8 c'8 bes8 c'8 d'8 dis'8 r8 | 
  r4 g'4 a'4 bes'4 a'4 bes'4 c''4 bes'4 c''4 d''4 d''4 r4 \bar "|." }
  \layout { } \midi { }
}


