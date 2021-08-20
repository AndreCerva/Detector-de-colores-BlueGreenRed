"""
author: andre
date: 02/05/2021
"""
#Se importan las librerias básicas
import cv2
import numpy as np
#Creamos función que reciba las mascaras B-G-R y el color respectivo que detecta la mascara
def mark(mask,color):
    contorns,_=cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)#Detectamos los contornos de las mask
    for i in contorns:
        area=cv2.contourArea(i)#Calculamos las áreas de los contornos
        if area>3000:#Nos quedamos unicamente con las áres de interes, eliminando ruido
            momentos=cv2.moments(i)
            if momentos['m00']== 0:momentos['m00']=1
            cx=int(momentos['m10']/momentos['m00'])#Obtenemos cordenadas del centro de lo detectado
            cy=int(momentos['m01']/momentos['m00'])
            area=int(momentos['m00'])#Obtenemos el area de lo detectado
            cv2.putText(frame,(f'Area: {area} Pixeles^2'),(cx-60,cy+20),1,0.5,[255,255,255])#Texto
            cv2.circle(frame,(cx,cy),3,[0,255,255],3)#Circulo
            cv2.putText(frame,(f'x={cx} y= {cy}'),(cx-60,cy-20),1,0.5,[255,255,255])#texto
            cv2.circle(frame,(cx,cy),6,color,3)#Circulo
            xr,yr,w,h=cv2.boundingRect(i)#rectangulo
            _,radio = cv2.minEnclosingCircle(i)#circulo
            radio=int(radio)
            cv2.circle(frame,(cx,cy),radio,0,3)#circulo
            cv2.rectangle(frame,(xr,yr),(xr+w,yr+h),color,3)#rectangulo
imag=cv2.VideoCapture(0)#Capturamos video camara principal
blue=[255,0,0]
red=[0,0,255]
green=[0,255,0]
#mascaras hsv
azulclaro = np.array([100,100,20],np.uint8)#h=100,s=100,v=20
azulfuerte = np.array([125,255,255],np.uint8)#h=125,s=255,v=255
verdeclaro = np.array([40,100,20],np.uint8)#h=40,s=100,v=20
verdefuerte = np.array([80,255,255],np.uint8)#h=80,s=255,v=255
rojoclaro=np.array([170,100,100],np.uint8)#h=170,s=100,v=100
rojofuerte=np.array([179,255,255],np.uint8)#h=179,s=255,v=255
while(True):
    ret, frame = imag.read()#Ret valor boleano cuando detecta o no señal, frame la imagen
    if ret==True:
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#se convierte la captura de imagen a hsv
        maskblue=cv2.inRange(hsv,azulclaro,azulfuerte)#se convinan los rangos de colores hsv para b
        maskgreen=cv2.inRange(hsv,verdeclaro,verdefuerte)#se convinan los rangos de colores hsv para g
        maskred=cv2.inRange(hsv,rojoclaro,rojofuerte)#se convinan los rangos de colores hsv para r
        #Se manda a llamar a la función
        mark(maskblue,blue)
        mark(maskgreen,green)
        mark(maskred,red)
        cv2.imshow('FRAME', frame)#Colores detectados
        cv2.imshow('MASKB',maskblue)#Mascara blue detectando
        cv2.imshow('MASKG',maskgreen)#Mascara green detectando
        cv2.imshow('MASKR',maskred)#Mascara red detectando
        if( cv2.waitKey(1) & 0xFF == ord('s')):#Salir precionando la tecla s
            break
    else:
        print('No se pudo acceder a la camara')
imag.release()
cv2.destroyAllWindows()
