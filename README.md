# wtum_gr11
## Opis projektu
W ramach projektu zostanie stworzony system generujący obrazy w stylu znanego malarza. Do jego stworzenia planujemy wykorzystać różne metody w celu ich porównania. Zakładamy, że obrazy wynikowe będą generowane ze zdjęcia podanego przez użytkownika.

## Narzędzia / technologie

Język programowania, którego planujemy użyć to **python** (w wersji 3+). Do wykonania projektu planujemy użyć trzech narzędzi/bibliotek:

1. **tensorflow** - ładowanie i przetwarzanie zdjęć oraz funkcjonalności uczenia maszynowego
2. **numpy** - struktury/typy danych (zintergowane z tensorflow)
3. **matplotlib** - do wizualizacji wyników

## Dane:
Program powinien otrzymać 2 zestawy danych:
1. obrazy wybranego malarza (w rozmiarze 256x256) - które będą użyte do wytrenowania modelu
2. zdjęcia (w rozmiarze 256x256), które docelowo program ma przerobić na obrazy w stylu wybranego malarza

## Przydział zadań
1. Antek Adaszkiewicz - Generatory
2. Patryk Burzycki - Dyskryminatory
3. Adrian Cieśla - Obróbka zdjec na wejsciu/zapis na wyjscie + wyświetlanie
4. Anita Czech - polaczenie czesci w calosc i nadzorowanie sieci