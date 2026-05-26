\version "2.20.0"
\header { title = "Fugue Diatonique Automatique Avancée" }
global = { \key d \minor \time 4/4 \tempo 4=120 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global <d'' e''>4 <a' f''>4 e''4 <d'' f''>4 <e' e''>4 <f' d''>4 <g' e''>4 <a' f''>4 <g' e''>4 <g' d''>4 <e' c''>4 <g' b'>4 | 
  <g e'>8 <d' f'>8 <c' e'>8 <bes f'>8 <e e'>8 <bes dis'>8 e'8 <bes f'>8 <d' e'>8 <bes d'>8 c'8 <d b>8 | 
  a''4 bes''4 a''4 bes''4 a''4 g''4 a''4 bes''4 a''4 g''4 f''4 e''4 | 
  <bes' e''>8 <f' f''>8 e''8 <d'' f''>8 <g' e''>8 <d'' dis''>8 <c'' e''>8 <f' f''>8 <c'' e''>8 d''8 <a' c''>8 <e' b'>8 | 
  d''8 cis''8 d''8 cis''8 d''8 dis''8 d''8 cis''8 d''8 e''8 fis''8 g''8 | 
  d'8 cis'8 d'8 cis'8 d'8 dis'8 d'8 cis'8 d'8 e'8 fis'8 g'8 | 
  a''8 bes''8 a''8 bes''8 a''8 gis''8 a''8 bes''8 a''8 g''8 f''8 e''8 | 
  <a' a''>8 <g'' bes''>8 <f'' a''>8 <d'' bes''>8 <f'' a''>8 <d'' gis''>8 <d'' a''>8 <bes' bes''>8 a''8 <e'' g''>8 <bes' f''>8 e''8 \bar "|." }
  \layout { } \midi { }
}
