import os
import sys
import cv2
import numpy as np

# Ścieżka do katalogu ze zbiorem danych
data_dir = sys.argv[1]

# Ścieżka do pliku bboxes.txt oraz bboxes_gt.txt
bbox_file = os.path.join(data_dir, 'bboxes.txt')
result_bbox_file = os.path.join(data_dir, 'bboxes_gt.txt')

counter_absolute = 0
counter_correct = 0

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


# Słownik, w którym kluczem jest nazwa zdjęcia, a wartością odpowiedzi
results_dict = {}
with open(result_bbox_file, 'r') as f:
    lines = f.readlines()
    i = 0
    while i < len(lines):
        # Wczytaj nazwę zdjęcia i liczbę bboxów
        filename = lines[i].strip()
        num_boxes = int(lines[i+1])
        i += 2
        
        # Wczytaj odpowiedzi i dodaj je do listy
        results = []
        for j in range(num_boxes):
            result = lines[i+j].split()[0]
            results.append(result)
        i += num_boxes
        
        # Dodaj listę odpowiedzi do słownika
        results_dict[filename] = results

# Stwórz wektor zawierający wszystkie nazwy zdjęć posegregowane względem swojego numeru
photos = list(bboxes.keys())
photos.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

# Wyświetl output dla pierwszego zdjęcia
prev = photos[0]
prev_photo = cv2.imread(os.path.join(data_dir, 'frames', prev))
result_string = ''
for i in range(len(bboxes[prev])):
    counter_absolute = counter_absolute + 1
    if str(results_dict[prev][i]) == str(-1):
        counter_correct = counter_correct + 1
    result_string = result_string + '-1 '
print(result_string)

# Iteruj po zdjęciach
for i in range(1, len(photos)):
    curr_photo = cv2.imread(os.path.join(data_dir, 'frames', photos[i]))
    curr_gray = cv2.cvtColor(curr_photo, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_photo, cv2.COLOR_BGR2GRAY)
    # W każdym zdjęciu iteruj po Bboxach
    result_string = ''
    for j in range(len(bboxes[photos[i]])):
        prob = []
        # Dla każdego Bboxa w curr iteruj po Bboxach w prev
        for k in range(len(bboxes[prev])):
            # Dla każdego Bboxa z prev oblicz prawdopodobieństwo że odpowiada on rozważanemu Bboxowi z curr na podstawie:
            # - Intersection over Union
            # - Podobieńśtwa obrazu
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
            bbox1 = curr_photo[int(y1):int(y1+h1), int(x1):int(x1+w1), :]
            bbox2 = prev_photo[int(y2):int(y2+h2), int(x2):int(x2+w2), :]
            bbox1 = cv2.resize(bbox1, (600, 600))
            bbox2 = cv2.resize(bbox2, (600, 600))
            prob_similarity = cv2.matchTemplate(bbox1, bbox2, cv2.TM_CCOEFF_NORMED)

            # Oblicz prawdopodobieństwo ostateczne z wykorzystaniem wag
            # prob.append(0.3 * prob_IoU + 0.5 * prob_similarity + 0.2 * prob_mv)
            prob.append(0.3 * prob_IoU + 0.7 * prob_similarity)

        # Mając wyliczony wektor z prawdopodobieństwami odpowiadania sobie poszczególnych Bboxów znajdź największe prawdopodobieńśtwo
        max_prob = 0
        max_prob_index = 0
        for k in range(len(prob)):
            if prob[k] > max_prob:
                max_prob = prob[k]
                max_prob_index = k
        # Jeżeli jest ono bardzo małe, znaczy to że jest to nowy Bbox (wyświetl -1)
        counter_absolute = counter_absolute + 1
        if(max_prob < 0.2):
            if str(results_dict[photos[i]][j]) == str(-1):
                counter_correct = counter_correct + 1
            result_string = result_string + '-1 '
        # Jeżeli jest ono większe, wyświetl index Bboxa znaelzionego Bboxa z poprzedniej klatki
        else:
            if str(results_dict[photos[i]][j]) == str(max_prob_index):
                counter_correct = counter_correct + 1
            result_string = result_string + str(max_prob_index) + ' '
    
    print(result_string)
    prev = photos[i]
    prev_photo = curr_photo

# accuracy = float(counter_correct) / float(counter_absolute)
# print(accuracy)