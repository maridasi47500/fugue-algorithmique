% Bloc généré : hauteurs_retrogrades+inversion (2.4s) - Cumul : 2.4s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 4.8s
% Bloc généré : retrograde (2.4s) - Cumul : 7.2s
% Bloc généré : transposition+hauteurs_retrogrades (2.4s) - Cumul : 9.6s
% Bloc généré : transposition+inversion (2.4s) - Cumul : 12.0s
% Bloc généré : inversion (2.4s) - Cumul : 14.4s
% Bloc généré : transposition+augmentation (4.8s) - Cumul : 19.2s
% Bloc généré : transposition+retrograde (2.4s) - Cumul : 21.6s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 24.0s
% Bloc généré : diminution (1.2s) - Cumul : 25.2s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 27.6s
%-> Fugue en C minor. Durée finale : 27.6s

\version "2.20.0"
\header { title = "Fugue Diatonique Automatique Avancée" }
global = { \key c \minor \time 4/4 \tempo 4=100 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global f'8 gis'8 bes'8 c''8 c''8 dis''8 f''8 bes'8 | 
  d''8 e''8 fis''8 gis''8 a''8 b''8 cis'''8 fis''8 | 
  d''8 c''8 bes'8 gis'8 g'8 f'8 dis'8 bes'8 | 
  d'8 c'8 bes8 gis8 g8 f8 dis8 bes8 | 
  bes8 f'8 dis'8 cis'8 c'8 bes8 gis8 fis8 | 
  bes'8 f''8 dis''8 cis''8 c''8 bes'8 gis'8 fis'8 | 
  <c dis'>4 <c gis>4 <d bes>4 <f c'>4 <bes cis'>4 <f dis'>4 <c' f'>4 <c' g'>4 | 
  d'8 c'8 bes8 gis8 g8 f8 dis8 bes8 | 
  d''8 e''8 fis''8 gis''8 a''8 b''8 cis'''8 fis''8 | 
  bes'16 dis'16 f'16 g'16 gis'16 bes'16 c''16 d''16 | 
  d''8 e''8 fis''8 gis''8 a''8 b''8 cis'''8 fis''8 \bar "|." }
  \layout { } \midi { }
}
