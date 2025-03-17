# Cambiar esta URL por la de nuestro endpoint
import requests
import re

import re


patron_matricula = r'\b\d{4} ?[A-Z]{3}\b'




URL = 'https://pruebavision22.cognitiveservices.azure.com/computervision/imageanalysis:analyze'

KEY = '8HAXyEDdxF4DfHWlGq984Xy6bxDsnI67UX7983NM4mwCtFrCEKwRJQQJ99BBAC5RqLJXJ3w3AAAFACOGAsUt'

with open("coche3.jpg", "rb") as img:
    imagen = img.read()

cabeceras = {"Ocp-Apim-Subscription-Key": KEY,
    "Content-Type": "application/octet-stream" }
respuesta = requests.post(URL +
    "?api-version=2024-02-01&features=read",
    data=imagen, headers=cabeceras)
respuesta_json = respuesta.json()
print(respuesta_json)



lista_bloques = respuesta_json['readResult']['blocks']
print("Descripción:", lista_bloques)
for bloque in lista_bloques:
    #print(bloque)
    #print(bloque['lines'])

    for linea in bloque['lines']:
        texto=linea['text']
        #print(texto)
        # Buscar todas las coincidencias
        matriculas= re.findall(patron_matricula, texto)
        print(matriculas)
        break







