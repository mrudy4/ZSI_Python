import numpy as np
import cv2
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

'''
 cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

'''

# obiekt capture będzie wskazywał kamerę podłączoną do komputera 
capture = cv2.VideoCapture(0)

# zdefiniowanie kodeka
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# utworzenie obiektu do nagrywania filmu
film = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

while capture.isOpened():
    # z otwartego wcześniej źródła spróbujemy wczytać kolejną klatkę obrazu
    ret,image = capture.read()

    image[:,:,2] = cv2.add(image[:,:,1],35)
    
    # jeśli udało się wczytać kolejną klatkę obrazu
    # wyświetlimy ją na w osobnym oknie - tak jak wcześniej wyświetlaliśmy zwykły obraz
    if ret == True:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Wyświetlenie liczby wykrytych twarzy
        message = f"Liczba wykrytych twarzy: {len(faces)}"
        cv2.putText(image, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        for (x,y,w,h) in faces:

            # wyyrysowanie odnalezionych twarzy      
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            film.write(image)
            cv2.imshow('Obraz z kamery', image)
            # wybranie fragmentu obrazu z wykrytą twarzą
            roi_szarosci = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
    
            # wyszukanie oczu w obrębie wykrytej twarzy
            eyes = eye_cascade.detectMultiScale(roi_szarosci)



            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
            
        # przerwij wykonywanie programu po nacisnieciu klaswisza 'x'
        if cv2.waitKey(25) & 0xFF == ord('x'):
            obraz = cv2.imwrite('obrazekTwarz.jpg',image)
            break
            
            
    # zakończenie pętli gdy nie udało się wczytać następnej klatki z kamery
    else: 
         break

# ważne aby zwolnić dostęp do filmu i do kamery
film.release()
capture.release()

# warto również zamknąć okna które zostały otwarte podczas wykonywania programu
cv2.destroyAllWindows()