# wtum_gr11
## Opis projektu
W ramach projektu zostanie stworzony system generujący obrazy w stylu znanego malarza. Do jego stworzenia planujemy wykorzystać różne metody w celu ich porównania. Zakładamy, że obrazy wynikowe będą generowane ze zdjęcia podanego przez użytkownika.

## Narzędzia / technologie

Język programowania, którego planujemy użyć to **python** (w wersji 3+). Do wykonania projektu planujemy użyć trzech narzędzi/bibliotek:

1. **tensorflow** - ładowanie i przetwarzanie zdjęć oraz funkcjonalności uczenia maszynowego
2. **numpy** - struktury/typy danych (zintergowane z tensorflow)
3. **matplotlib** - do wizualizacji wyników

## Dane
Program powinien otrzymać 2 zestawy danych:
1. obrazy wybranego malarza (w rozmiarze 256x256) - które będą użyte do wytrenowania modelu
2. zdjęcia (w rozmiarze 256x256), które docelowo program ma przerobić na obrazy w stylu wybranego malarza

## Przydział zadań
Adrian:
- dokończenie aplikacji okienkowej
- obróbka(skalowanie) zdjęć wgrywanych do aplikacji
- przygotowanie datasetu do GANa
- wizualizacja wyników (GAN i szumy)

Patryk:
- generator GAN
- funkcje strat GAN
- wytrenowanie GAN

Anita:
- dyskryminator GAN
- funkcje strat GAN
- wytrenowanie GAN

Michał:
- zbudowanie + wytrenowanie modelu do odszumiania

Antek:
- generacja szumów danych
- odszumianie

wszyscy:
- stworzenie raportu, porównanie ywników, wnioski (każdy o swojej części)

jak starczy czasu:
- dodanie generowania z szumów zdjęć i generowanie z nich za pomocą GANa obrazów artysty i porównanie wyników z 
  podstawowym modelem diffiusion (wizualne porównania)
- ocena wyników diffiusion poprzez dyskryminator z GANa
