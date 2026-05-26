% Bloc généré : transposition+retrograde (2.4s) - Cumul : 2.4s
% Bloc généré : transposition+hauteurs_retrogrades (2.4s) - Cumul : 4.8s
% Bloc généré : transposition+augmentation (4.8s) - Cumul : 9.6s
% Bloc généré : hauteurs_retrogrades+inversion (2.4s) - Cumul : 12.0s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 14.4s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 16.8s
% Bloc généré : inversion+retrograde (2.4s) - Cumul : 19.2s
% Bloc généré : retrograde (2.4s) - Cumul : 21.6s
% Bloc généré : transposition+inversion (2.4s) - Cumul : 24.0s
% Bloc généré : inversion (2.4s) - Cumul : 26.4s
% Bloc généré : diminution (1.2s) - Cumul : 27.6s
%-> Fugue en D major. Durée finale : 27.6s

\version "2.20.0"
\header { title = "Fugue Diatonique Automatique Avancée" }
global = { \key d \major \time 6/8 \tempo 4.=100 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global a'8 fis'8 d'8 a'8 e'8 cis'8 a'8 fis'8 d'8 a'8 g'8 e'8 | 
  e''8 cis''8 a'8 e''8 b'8 gis'8 e''8 cis''8 a'8 e''8 d''8 b'8 | 
  <d' a'>4 <g' c''>4 <fis' d''>4 <d' g'>4 <b b'>4 <d' d''>4 <cis' fis'>4 <a a'>4 <d' d''>4 g'4 <g' b'>4 <a' d''>4 | 
  b8 d'8 fis'8 b8 e'8 g'8 b8 d'8 fis'8 b8 cis'8 e'8 | 
  a'8 c''8 e''8 a'8 d''8 f''8 a'8 c''8 e''8 a'8 b'8 d''8 | 
  a'8 c''8 e''8 a'8 d''8 f''8 a'8 c''8 e''8 a'8 b'8 d''8 | 
  a'8 c''8 e''8 a'8 d''8 f''8 a'8 c''8 e''8 a'8 b'8 d''8 | 
  a'8 fis'8 d'8 a'8 e'8 cis'8 a'8 fis'8 d'8 a'8 g'8 e'8 | 
  a'8 fis'8 e'8 b'8 g'8 e'8 c''8 a'8 e'8 b'8 g'8 e'8 | 
  e'8 cis'8 b8 fis'8 d'8 b8 g'8 e'8 b8 fis'8 d'8 b8 | 
  e'16 g'16 a'16 d'16 fis'16 a'16 cis'16 e'16 a'16 d'16 fis'16 a'16 \bar "|." }
  \layout { } \midi { }
}
