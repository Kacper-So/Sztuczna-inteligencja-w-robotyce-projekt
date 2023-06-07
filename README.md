# Sztuczna-inteligencja-w-robotyce-projekt
Napisany program przyjmuje jako argument ścieżkę do danych wejściowych w formie przewidzianej w opisie projektu.
Wczytane dane konwertowane są do odpowiednich słowników. Następnie program iteruje po kolejnych klatkach nagranego filmu analizując aktualną oraz poprzednią klatkę.
Dla kolejnych iteracji generowane są macierze o wymiarach {Ilość bboxów w aktualnej klatce}X{Ilość bboxów w poprzedniej klatce}. Wartościami w komórkach tych macierzy są prawdopodobieństwa określające szanse na to, że bbox z aktualnej klatki, jest następstwem bboxa z poprzedniej klatki, gdzie bboxy identyfikowane są przez numer wiersza i kolumny w macierzy.
Prawdopodobieństwa obliczane są na podstawie dwóch wskaźników wziętych z odpowiednią wagą:
1. wartość wynikająca z intersection over union. Określa w jakiej części bboxy pokrywają się powierzchnią między klatkami,
2. wartość wynikająca z dopasowania obrazu za pomocą funkcji matchTemplate z biblioteki opencv,

Wyniki generowane są poprzez określenie maksymalnej wartości w kolumnie macierzy, czyli określenie który bbox poprzedniej klatki jest najprawdopodobniej tym samym obiektem co rozważany bbox z aktualnej klatki.
Jeżeli znalezione prawdopodobieństwo jest niższe niż określona minimalna wartość bbox uznawany jest jako nowy obiekt.
