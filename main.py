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
filenames = list(bboxes.keys())
filenames.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

# Wczytaj zdjęcia i wykorzystaj listy bounding boxów do przetwarzania zdjęć
for filename in filenames:
    # Wczytaj zdjęcie
    img_file = os.path.join(data_dir, 'frames', filename)
    img = cv2.imread(img_file)

    # Wykorzystaj bounding boxy do przetwarzania zdjęcia
    for box in bboxes[filename]:
        x, y, w, h = box
        # roi = img[int(y):int(y+h), int(x):int(x+w)]
    cv2.imshow('image', img)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()