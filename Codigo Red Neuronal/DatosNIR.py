#LIBRERIAS 
#==================================================================================================================================
import pandas as pd
import os
#Leemos los archivos .txt que contienen los datos y los pasamos a un dataframe
#==================================================================================================================================
folder_origen="C:/Users/Usuario/Desktop/RESULTADOS/NIR F"
i=True
for nombreImg in os.listdir(folder_origen):
    if ".txt" in nombreImg: 
        #leemos el archivo .txt
        nir = pd.read_csv((os.path.join(folder_origen,nombreImg)),sep=",",header=None)
        #generamos la transpuesta del dataframe para que las longitudes de onda pasen de ser filas a columnas
        nir=nir.T
        #Cambaimos el nombre de las columnas para que este sea igual a la longitud de onda
        nir.columns = nir.iloc[0]
        #Nos quedamos solamente con la fila 1, que es la que contiene los resultados que dio el corcho como respuesta a la longitud de onda especifica
        nir = nir[1:]
        if i is True:
            #Si este es el primer dataframe que se hace, se utiliza con el dataframe principal al que se le concatenar el resto 
            data=nir
            i=False
        else:
        #Concatenamos los datos al dataframe.
            data = pd.concat([data,nir])
#Creamos el Dataframe de los NIR
#==================================================================================================================================
folder_destino = "C:/Users/Usuario/Desktop/Red Neuro/F jpg/nir.csv"
#Reiniciamos el indice puesto que tras las concatenaciones el idice de todas las filas es 1 
data=data.reset_index(drop=True)
data.to_csv(folder_destino,index=False) 