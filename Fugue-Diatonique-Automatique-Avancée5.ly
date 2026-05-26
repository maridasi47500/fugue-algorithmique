% Bloc généré : inversion+retrograde (4.0s) - Cumul : 4.0s
% Bloc généré : retrograde (4.0s) - Cumul : 8.0s
% Bloc généré : inversion (4.0s) - Cumul : 12.0s
% Bloc généré : inversion+retrograde (4.0s) - Cumul : 16.0s
% Bloc généré : transposition+hauteurs_retrogrades (4.0s) - Cumul : 20.0s
% Bloc généré : inversion+retrograde (4.0s) - Cumul : 24.0s
% Bloc généré : transposition+inversion (4.0s) - Cumul : 28.0s
% Bloc généré : transposition+retrograde (4.0s) - Cumul : 32.0s
%-> Fugue en G major. Durée finale : 32.0s

\version "2.20.0"
\header { title = "Fugue Diatonique Automatique Avancée" }
global = { \key g \major \time 4/4 \tempo 4=100 }
\score {
  \new Staff \with { midiInstrument = "violin" } { \global e'4 fis'4 cis'8 b8 a8 e'8 fis'16 e'16 cis'16 b16 e'16 cis'16 b16 a16 cis'8 b8 a8 gis'8 a4 e'4 | 
  e'4 d'4 g'8 a'8 b'8 e'8 d'16 e'16 g'16 a'16 e'16 g'16 a'16 b'16 g'8 a'8 b'8 c'8 b'4 e'4 | 
  e'4 a4 gis'8 a8 b8 cis'8 a16 b16 cis'16 e'16 b16 cis'16 e'16 f'16 e'8 a8 b8 cis'8 f'4 e'4 | 
  e'4 fis'4 cis'8 b8 a8 e'8 fis'16 e'16 cis'16 b16 e'16 cis'16 b16 a16 cis'8 b8 a8 gis'8 a4 e'4 | 
  a'4 g'4 c''8 d''8 e''8 a'8 g'16 a'16 c''16 d''16 a'16 c''16 d''16 e''16 c''8 d''8 e''8 f'8 e''4 a'4 | 
  e'4 fis'4 cis'8 b8 a8 e'8 fis'16 e'16 cis'16 b16 e'16 cis'16 b16 a16 cis'8 b8 a8 gis'8 a4 e'4 | 
  e4 a,4 gis8 a,8 b,8 cis8 a,16 b,16 cis16 e16 b,16 cis16 e16 f16 e8 a,8 b,8 cis8 f4 e4 | 
  e4 d4 g8 a8 b8 e8 d16 e16 g16 a16 e16 g16 a16 b16 g8 a8 b8 c8 b4 e4 \bar "|." }
  \layout { } \midi { }
}
