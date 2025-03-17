# Cambiar esta URL por la de nuestro endpoint
import os
from datetime import datetime

import requests


import re

URL = 'https://pruebavision22.cognitiveservices.azure.com/computervision/imageanalysis:analyze'

KEY = '8HAXyEDdxF4DfHWlGq984Xy6bxDsnI67UX7983NM4mwCtFrCEKwRJQQJ99BBAC5RqLJXJ3w3AAAFACOGAsUt'

def leer_matricula(ruta_imagen):

    patron_matricula = r'\b\d{4} ?[A-Z]{3}\b'


    with open(ruta_imagen, "rb") as img:
        imagen = img.read()

    cabeceras = {"Ocp-Apim-Subscription-Key": KEY,
        "Content-Type": "application/octet-stream" }
    respuesta = requests.post(URL +
        "?api-version=2024-02-01&features=read",
        data=imagen, headers=cabeceras)



    if respuesta.status_code != 200:
        print(['error al llamar a azure',respuesta.status_code],respuesta.text)
        return ""

    respuesta_json = respuesta.json()
    # print(respuesta_json)  #si no da error imprimira el resultado por consola



    try:
        lista_bloques = respuesta_json['readResult']['blocks']
        #print("Descripción:", lista_bloques)
        for bloque in lista_bloques:
            #print(bloque)
            #print(bloque['lines'])
            for linea in bloque['lines']:
                texto=linea['text']
                #print(texto)
                # Buscar todas las coincidencias
                coincidencias = re.findall(patron_matricula, texto)
                if coincidencias:
                    return coincidencias[0].replace(" ","")
        return ""

    except Exception as e:
        print(e)
        return ""

def leer_matriculas_entrada(coches):
    ruta_carpeta="entrada"
    ficheros=os.listdir(ruta_carpeta)#devuelve una lista con el nombre de las imagenes

    for fichero in ficheros:
        ruta_imagen=os.path.join(ruta_carpeta,fichero)
        #print('ruta imagen',ruta_imagen)

        matricula=leer_matricula(ruta_imagen)

        if matricula == "":
            print('No hay matricula detectada')#de esta nabera dectariamos si no detectarta matricula pero no nos ha pasado
        else:
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            coches[matricula]=fecha_hora_actual
            #print('Matricula detectada',matricula)
            #print(f'Fecha y hora actual: {fecha_hora_actual}') #una vez que vemos que funciona lo dejamos comentado
            os.remove(ruta_imagen)#eliminamos la imagen por lo que mas me vale acordarme de copiarla y no moverla a entradas

    return coches


def actualizar_entradas(coches):

    with open("entradas.txt","w") as archivo:
        for matricula,fecha_hora in coches.items():
            archivo.write(f'{matricula};{fecha_hora}\n')#utilamos el ; como separador



def leer_entradas():
    fichero_entradas="entradas.txt"
    coches={}#creamos el diccionario

    if not os.path.exists(fichero_entradas):
        with open(fichero_entradas, "w") as archivo:
            pass


    with open(fichero_entradas, "r") as archivo:
        lineas = archivo.readlines()#lee todas las lineas del archivo y las devuelve como una lista de string

        for linea in lineas:#recorremos la lista
            linea = linea.strip()  # Quitamos espacios y saltos de línea
            if ";" in linea:  #Entendemos que es una line valida si contiene un ; y se procesa
                matricula, fecha_hora = linea.split(";")
                coches[matricula] = fecha_hora  #guardamos en el diccionario clave=matricula y valor=fecha_hora

    return coches

def leer_matriculas_salida(coches):
    ruta_carpeta="salida"
    ficheros=os.listdir(ruta_carpeta)

    salidas={}

    for fichero in ficheros:
        ruta_imagen=os.path.join(ruta_carpeta,fichero)
        #print('ruta imagen',ruta_imagen)
        matricula=leer_matricula(ruta_imagen)
        if matricula == "":
            print('No hay matricula detectada')
        elif matricula in coches:#vamos a comprobar si la matricula esta en entradas
            hora_entrada=coches[matricula]
            hora_salida=datetime.now().strftime("%d/%m/%Y %H:%M")


            formato="%d/%m/%Y %H:%M"
            tiempo_entrada=datetime.strptime(hora_entrada,formato)
            tiempo_salida=datetime.strptime(hora_salida,formato)
            total_minutos=int((tiempo_salida-tiempo_entrada).total_seconds()//60)

            tarifa=total_minutos*(6/60)
            tarifa=round(tarifa,2)#redondeamoa a 2 decimales por si acaso

            '''se que e los apuntes nos diste el consejo de hacerlo asi, pero lo vi mas complicado que dividir el total por el precio hora minutos

            diferencia = tiempo_salida - tiempo_entradaprint("Horas de diferencia:", diferencia.total_seconds() // 3600)'''

            salidas[matricula]=[hora_entrada,hora_salida,tarifa]
            print(f'matricula {matricula} registrada en salidas.txt con tarifa {tarifa}')

            del coches[matricula]#lo borramos pero no haria falta por que ya borramos cuando acccedemoa a entradas

            os.remove(ruta_imagen)

        else:
            print(f'La matricula {matricula} no esta en entradas, pero se ha detectado la salida por lo que se le cobrara el maximo 100€')
            hora_salida = datetime.now().strftime("%d/%m/%Y %H:%M")
            tarifa = 100.00  # Penalización de 100€
            salidas[matricula] = ("DESCONOCIDA", hora_salida, tarifa)
            os.remove(ruta_imagen)

    return coches, salidas


def actualizar_salidas(salidas):
    with open("salidas.txt","a") as archivo:#ponemo a para que agrege al final del archivo
        for matricula,(hora_entrada,hora_salida,tarifa) in salidas.items():
            archivo.write(f'{matricula};{hora_entrada};{hora_salida};{tarifa}\n')



if __name__ == '__main__':



    coches = leer_entradas()



    coches_nuevas_entradas = leer_matriculas_entrada(coches)



    coches_nuevas_salidas, salidas_detectadas = leer_matriculas_salida(coches_nuevas_entradas)



    actualizar_entradas(coches_nuevas_salidas)



    actualizar_salidas(salidas_detectadas)


















