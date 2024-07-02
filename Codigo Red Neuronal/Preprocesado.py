#Librerias
import cv2
import os
import os.path
import pandas as pd
import numpy as np
import pickle

#####IMPORTANTE PONER LA DIRECCIÓN EN LA QUE SE ENCUENTRAN LAS IMAGENES#######
#direccion de la carpeta
folder = "C:/Users/Usuario/Desktop/Red Neuro/F jpg"
#lista en la que se guardaran las imagenes modificadas
images = []

# Funcion que realiza una seleccion del corcho por color y la usa como mascara para eliminar el fondo de la imagen
def corcho_selec(x,rgb):
    #Aqui se definen los balores maximos que puede tener un pixel, por encima de los valores seleccionados se elimina 
    lower_val = np.array([0,0,0])
    upper_val = np.array([rgb,rgb,rgb])
    mask = cv2.inRange(x, lower_val, upper_val)
    #Relleno de los agujeros
    contour,hier = cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        cv2.drawContours(mask,[cnt],0,255,-1)
    #inversion para que las zonas que queremos mantener sean blancas
    mask = cv2.bitwise_not(mask)        
 #uso de la mascara para que solo el corcho mantega el color original y el resto se quede negro                                           
    output = x.copy()
    output[mask.astype(bool), :] = 0
    #la imagen procesada se añade a la lista
    images.append(output)


#Bucle en el que se leen los archibos jpg y se le realizan las transformaciónes
for nombreImg in os.listdir(folder):
    img = cv2.imread(os.path.join(folder,nombreImg))
    if img is not None:
        #lectura de la imagen 
        nombreImg=nombreImg.replace('F.jpg', '')
        #El nombre de todas las imagenes es su núemro identificativo .jpg, por tanto la variable nuemro se usara para guardar este número identificativo para más adelante
        numero=int(nombreImg)
        #reduccion de tamaño de la imagen a 2048 pixeles
        down_points = (2048, 2048)
        img = cv2.resize(img, down_points, interpolation= cv2.INTER_AREA)
        #Aqui se dividen las imagenes en grupos, dado que, a pesar de nuestros esfuerzos por mantener una iluminacion identica en todas las fotos, 
        #algunas imagene tienen iluminaciones ligeramente diferentes entre si. Para asegurar que solo se elimina el fondo se han dividido en grupos con margenes distintos.
        if numero<58:
            corcho_selec(img,100)
        #Repetir el proceso en los otros grupos con margenes distintos
        elif numero==120:
             corcho_selec(img,75)
        elif numero<123:
            corcho_selec(img,85)
        elif numero<127:
            corcho_selec(img,100)
        elif numero<133:
            corcho_selec(img,74)
        elif numero<150:
            corcho_selec(img,70)
        elif numero<175:
            corcho_selec(img,80)
        elif numero==175:
            corcho_selec(img,70)
        elif numero== 187:           
            corcho_selec(img,70)      
        elif numero== 194:           
            corcho_selec(img,70)        
        elif numero < 200:            
            corcho_selec(img,80)            
        elif numero== 212:   
            corcho_selec(img,63)     
        elif numero== 215:           
            corcho_selec(img,63)         
        elif numero < 220:
            corcho_selec(img,70)
        elif numero== 241:           
            corcho_selec(img,80)   
        elif numero== 246:           
            corcho_selec(img,80)       
        elif numero== 262:           
            corcho_selec(img,80)           
        elif numero== 264:           
            corcho_selec(img,80)        
        elif numero < 270:
            corcho_selec(img,63)     
        elif numero== 275:           
            corcho_selec(img,80)                       
        elif numero < 316:
            corcho_selec(img,70)

#Lectura de el csv con la informacion de las capacidades antioxidantes. 
Frap=pd.read_csv("Frap.csv",sep=";",decimal=',')
#convertimos la columna "72h" que contiene los valores obtenidos en el Frap al medirse 72 horas despues de la medición
h72 = Frap["72h"].tolist()

#lista en la que se almacenaran los valores de images y su respectivo valor de capacidad antioxidante.
datos=[]
for x in range(315): 
    Temp=[]
    Temp.append(images[x])  
    Temp.append(h72[x])
    datos.append(Temp)
with open("datos", "wb") as fp:   
    pickle.dump(datos, fp)
#Usamos pickle para guardar los datos en lugar de pandas puesto que pandas tiende a destrodar los numpy.ndarray. cuando se carga 