import cv2
import mediapipe as mp
import math as m
import serial as s

kamera=cv2.VideoCapture(1)
cizim_modul=mp.solutions.drawing_utils
el_modul=mp.solutions.hands
arduino=s.Serial('com5',9600)

def sinyal_yolla(x):
    if x>185:
        arduino.write(b'A')
    elif 140<=x<=185:
        arduino.write(b'B')
    elif 90<=x<=140:
        arduino.write(b'C')
    elif 50<=x<=90:
        arduino.write(b'D')
    elif 25<=x<=50:
        arduino.write(b'E')
    elif 25>x:
        arduino.write(b'F')

with el_modul.Hands(static_image_mode=True) as eller:
    while True:
        kontrol, resim=kamera.read()
        sonuc=eller.process(cv2.cvtColor(resim,cv2.COLOR_BGR2RGB))

        yukseklik,genislik,_=resim.shape
        if sonuc.multi_hand_landmarks != None:
            for elLandmark in sonuc.multi_hand_landmarks:
                for kordinat in el_modul.HandLandmark:
                    kordinat1=elLandmark.landmark[4]
                    kordinat2=elLandmark.landmark[20]
                    cv2.circle(resim,(int(kordinat1.x*genislik),int(kordinat1.y*yukseklik)),4,(255,0,0),4)
                    cv2.circle(resim, (int(kordinat2.x * genislik), int(kordinat2.y * yukseklik)), 4, (255, 0, 0), 4)
                    mesafe=int(m.sqrt(m.pow((kordinat2.x-kordinat1.x)*genislik,2)+m.pow((kordinat2.y-kordinat1.y)*yukseklik,2)))
                    sinyal_yolla(mesafe)
                    cv2.putText(resim,"Mesafe:"+f"{int(mesafe)}",(50,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                    cv2.line(resim,(int(kordinat1.x*genislik),int(kordinat1.y*yukseklik)),(int(kordinat2.x*genislik),int(kordinat2.y*yukseklik)),(0,255,0),3)
        cv2.imshow("Goruntu",resim)
        cv2.waitKey(250)
