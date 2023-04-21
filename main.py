import os
import sys
import cv2

# Ścieżka do katalogu ze zbiorem danych
data_dir = sys.argv[1]

# Ścieżka do pliku bboxes.txt
bbox_file = os.path.join(data_dir, 'bboxes.txt')

# Słownik, w którym kluczem jest nazwa zdjęcia, a wartością lista bboxów
bboxes = {}
with open(bbox_file, 'r') as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        # Wczytaj nazwę zdjęcia i liczbę bboxów
        filename = lines[i].strip()
        num_boxes = int(lines[i+1])
        i += 2
        
        # Wczytaj bboxy i dodaj je do listy
        boxes = []
        for j in range(num_boxes):
            x, y, w, h = map(float, lines[i+j].split())
            boxes.append((x, y, w, h))
        i += num_boxes
        
        # Dodaj listę bboxów do słownika
        bboxes[filename] = boxes

# Stwórz wektor zawierający wszystkie nazwy zdjęć posegregowane względem swojego numeru
photos = list(bboxes.keys())
photos.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

# Wyświetl output dla pierwszego zdjęcia
prev = photos[0]
prev_photo = cv2.imread(data_dir, 'frames', prev)
for i in range(len(bboxes[prev])):
    print(-1)

# Iteruj po zdjęciach
for i in range(1, len(photos)):
    curr_photo = cv2.imread(data_dir, 'frames', photos[i])
    # W każdym zdjęciu iteruj po Bboxach
    for j in range(len(bboxes[photos[i]])):
        prob = []
        # Dla każdego Bboxa w curr iteruj po Bboxach w prev
        for k in range(len(bboxes[prev])):
            # Dla każdego Bboxa z prev oblicz prawdopodobieństwo że odpowiada on rozważanemu Bboxowi z curr na podstawie:
            # - Intersection over Union
            # - Podobieńśtwa obrazu
            # - 
            # Zbierz dane o aktualnie rozważanych Bboxach
            x1, y1, w1, h1 = bboxes[photos[i]][j]
            x2, y2, w2, h2 = bboxes[prev][k]

            # Oblicz prawdopodobieństwa na podstawie IoU
            prob_IoU = 0.
            xA = max(x1, x2)
            yA = max(y1, y2)
            xB = min(x1 + w1, x2 + w2)
            yB = min(y1 + h1, y2 + h2)
            interArea = max(0, xB - xA) * max(0, yB - yA)
            boxAArea = w1 * h1
            boxBArea = w2 * h2
            prob_IoU = interArea / float(boxAArea + boxBArea - interArea)
            
            # Oblicz prawdopodobieńśtwo na podstawie podobieńśtwa obrazu
            prob_similarity = 0.            
            # Oblicz prawdopodobieńśtwo na podstawie
            prob_mv = 0.

            # Oblicz prawdopodobieństwo ostateczne z wykorzystaniem wag
            prob.append(0.1 * prob_IoU + 0.2 * prob_similarity + 0.7 * prob_mv)

        # Mając wyliczony wektor z prawdopodobieństwami odpowiadania sobie poszczególnych Bboxów znajdź największe prawdopodobieńśtwo
        max_prob_index = 0
        for k in range(len(prob)):
            if prob[k] > max_prob:
                max_prob = prob[k]
                max_prob_index = k
        # Jeżeli jest ono bardzo małe, znaczy to że jest to nowy Bbox (wyświetl -1)
        if(max_prob < 0.2):
            print(-1, end='')
            print(' ', end='')
        # Jeżeli jest ono większe, wyświetl index Bboxa znaelzionego Bboxa z poprzedniej klatki
        else:
            print(k, end='')
            print(' ', end='')
    print()
    prev = photos[i]
    prev_photo = curr_photo

cv2.destroyAllWindows()