import os.path
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as dialog
from gestor_parking import main
from PIL import ImageTk,Image


CARPETA_IMAGENES="entrada"
CARPETA_IMAGENES_SALIDA="salida"

ventana=tk.Tk() #creamos la ventana principal
ventana.title("Parking") #le damos un titulo
ventana.geometry("900x500") #le damos un tamaño
ventana.minsize(900,500)


ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=2)
ventana.columnconfigure(2, weight=1)

ventana.configure(bg="#f0f0f0")  # Fondo general claro


marco_izquidado=tk.Frame(ventana, bg="#f0f0f0")#creamos un marco
marco_izquidado.grid(row=0, column=0, sticky="nsew")#con sticky le decimos que se adapte al tamaño de la ventana

contenedor_botonoes=tk.Frame(marco_izquidado, bg="#f0f0f0")#creamos un marco
contenedor_botonoes.pack(expand=True)

marco_centro=tk.Frame(ventana, bg="white")#creamos un marco
marco_centro.grid(row=0, column=1, sticky="nsew")#con sticky le decimos que se adapte al tamaño de la ventana

marco_derecho=tk.Frame(ventana, bg="#e6f2ff")#creamos un marco
marco_derecho.grid(row=0, column=2, sticky="nsew")#con sticky le decimos que se adapte al tamaño de la ventana

def ejecutar_programa():
    main()
    mostrar_imagenes()
    mostrar_salidas_derecha()


def seleccionar_imagen():
    ruta_imagen = dialog.askopenfilename(
        title="Seleccionar imagen",

    )
    if ruta_imagen:
       nombre_archivo = os.path.basename(ruta_imagen)#obtenemos el nombre del archivo
       ruta_destino=os.path.join(CARPETA_IMAGENES,nombre_archivo)#creamos la ruta
       shutil.copy(ruta_imagen,ruta_destino)#copiamos la imagen

def seleccionar_imagen_salida():
    ruta_imagen = dialog.askopenfilename(
        title="Seleccionar imagen",

    )
    if ruta_imagen:
       nombre_archivo = os.path.basename(ruta_imagen)#obtenemos el nombre del archivo
       ruta_destino=os.path.join(CARPETA_IMAGENES_SALIDA,nombre_archivo)#creamos la ruta
       shutil.copy(ruta_imagen,ruta_destino)#copiamos la imagen

IMAGENES=[]#creamos una lista para evitar que se borre la referencia de las fotos
def mostrar_imagenes():
    global IMAGENES
    IMAGENES=[]

    for imagenes_viejas in marco_centro.winfo_children():
        print("borrando imagenes")
        imagenes_viejas.destroy()#borramos las imagenes anteriores

    carpeta_copia_ = "entradas_copia"
    os.makedirs(carpeta_copia_, exist_ok=True)  # si no existe crea la carptera

    for fichero in os.listdir(carpeta_copia_):
        ruta_imagen= os.path.join(carpeta_copia_,fichero)
        try:
            imagen = Image.open(ruta_imagen)#abrimos la imagen
            imagen=imagen.resize((200,200))#redimensionamos la imagen
            imagen_tk= ImageTk.PhotoImage(imagen)#convertimos la imagen en una imagen de tkinter
            IMAGENES.append(imagen_tk)#guardamos la imagen en la lista
            etiqueta_imagen = tk.Label(marco_centro, image=imagen_tk)
            etiqueta_imagen.pack(pady=10)
            os.remove(ruta_imagen)
        except Exception as e:
            print(e)


def mostrar_salidas_derecha():
    # Limpiar contenido previo del marco derecho
    for widget in marco_derecho.winfo_children():
        widget.destroy()

    # Crear canvas con scroll vertical
    canvas = tk.Canvas(marco_derecho, bg="lightblue", highlightthickness=0)
    scrollbar = tk.Scrollbar(marco_derecho, orient="vertical", command=canvas.yview)
    frame_scroll = tk.Frame(canvas, bg="lightblue")

    # Ajustar scroll al contenido
    frame_scroll.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Colocar el canvas y el scroll
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Leer archivo de salidas
    if not os.path.exists("salidas.txt"):
        etiqueta = tk.Label(frame_scroll, text="No hay registros de salidas.", bg="lightblue")
        etiqueta.pack(pady=10)
        return

    with open("salidas.txt", "r") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        linea = linea.strip()
        if linea:
            datos = linea.split(";")
            if len(datos) == 4:
                matricula, entrada, salida, tarifa = datos
                tarifa_float = float(tarifa)
                color = "black"

                # Coloreamos tarifas altas o desconocidas
                if tarifa_float >= 100:
                    color = "red"
                elif entrada == "DESCONOCIDA":
                    color = "orange"

                texto = (
                    f" Matrícula: {matricula}\n"
                    f" Entrada:  {entrada}\n"
                    f" Salida:   {salida}\n"
                    f" Tarifa:   {tarifa} €\n"
                    f"{'-'*28}"
                )

                etiqueta = tk.Label(
                    frame_scroll,
                    text=texto,
                    bg="lightblue",
                    fg=color,
                    font=("Consolas", 10),
                    anchor="w",
                    justify="left"
                )
                etiqueta.pack(anchor="w", padx=10, pady=5)



'''boton_mostrar_vehiculos=tk.Button(marco_izquidado,text="Mostrar Vehiculos",command=mostrar_imagenes)
boton_mostrar_vehiculos.pack()'''




boton_imagen_entrada=ttk.Button(contenedor_botonoes,text="Entrada Vehiculos",command=seleccionar_imagen)
boton_imagen_entrada.pack(pady=20)

boton_imagen_salida=ttk.Button(contenedor_botonoes,text="Salida Vehiculos",command=seleccionar_imagen_salida)
boton_imagen_salida.pack(pady=20)

boton_ejecutar=ttk.Button(contenedor_botonoes,text="play",command=ejecutar_programa)
boton_ejecutar.pack(pady=20)

ventana.mainloop()