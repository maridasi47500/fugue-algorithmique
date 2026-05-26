\version "2.20.0"
\header { title = "Fugue Diatonique Automatique" }
global = { \key a \minor \time 4/4 \tempo 4=120 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global r8 g8 a8 bes8 a8 bes8 c'8 bes8 c'8 d'8 dis'8 r8 | 
  r8 bes'8 a'8 g'8 f'8 g'8 f'8 e'8 f'8 e'8 d'8 r8 | 
  r8 bes'8 a'8 g'8 f'8 g'8 f'8 e'8 f'8 e'8 d'8 r8 | 
  r16 d'16 e'16 f'16 e'16 f'16 g'16 f'16 g'16 a'16 bes'16 r16 | 
  r8 d'8 c'8 b8 c'8 b8 a8 b8 a8 g8 fis8 r8 | 
  r4 d'4 e'4 f'4 e'4 f'4 g'4 f'4 g'4 a'4 bes'4 r4 | 
  r8 <b g'>8 <f' a'>8 <f' bes'>8 <c' a'>8 <d' bes'>8 <e' c''>8 <c' bes'>8 <e' c''>8 <a' d''>8 <d'' dis''>8 r8 | 
  r8 d'8 e'8 f'8 e'8 f'8 g'8 f'8 g'8 a'8 bes'8 r8 | 
  r4 d'4 e'4 f'4 e'4 f'4 g'4 f'4 g'4 a'4 bes'4 r4 \bar "|." }
  \layout { } \midi { }
}

