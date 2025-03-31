## Parking 

Aplicación de escritorio desarrollada en Python con interfaz gráfica (Tkinter) que detecta matrículas en imágenes de vehículos mediante OCR (Azure Computer Vision) y gestiona la entrada y salida de un parking.

---

## ✨ Características

- Carga de imágenes de vehículos para entrada o salida
- Lectura de matrículas con Azure OCR
- Registro automático en `entradas.txt` y `salidas.txt`
- Historial de entradas/salidas con tarifas
- Interfaz dividida en 3 columnas:
  - ◀ Izquierda: botones de acción
  - ◼ Centro: previsualización de vehículos dentro
  - ▶ Derecha: historial con scroll
- Estilo visual claro y minimalista

---

## 🚀 Tecnologías utilizadas

- Python 3
- Tkinter (GUI)
- Pillow (visualización de imágenes)
- Azure Computer Vision OCR de Microsoft (API REST)
- dotenv (variables de entorno)
- Git

---

## 🎓 Requisitos

- Python 3.10 o superior
- Cuenta en Azure con clave de suscripción OCR
- Variables de entorno configuradas en `.env`:

```
URL=https://<tu-endpoint>.cognitiveservices.azure.com/
KEY=tu_clave_de_azure
```

> **Nota:** El archivo `.env` está incluido en `.gitignore` por seguridad.

> ☕ Esta aplicación utiliza el servicio **Azure Computer Vision**. Puedes crearlo desde el [Azure Portal](https://portal.azure.com), seleccionar "Computer Vision", generar tu clave y endpoint y usarlos en este proyecto.

---

## 🔧 Instalación y uso

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/parking-detector.git
cd parking-detector
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Coloca tus imágenes de prueba en las carpetas `entrada/` y `salida/`, o usa las 6 imágenes de ejemplo incluidas en `/imagenes_ejemplo/`.

5. Ejecuta la aplicación:

```bash
python gui.py
```

---


---

## 🔍 Sobre este proyecto

Este ejercicio con fines educativos simula el funcionamiento automatizado del acceso de vehículos a un parking. Mediante el uso de tecnología de visión por computadora (Azure Computer Vision), el sistema:

- Detecta automáticamente la matrícula de un vehículo cuando entra o sale del parking.
- Registra los datos de entrada y salida.
- Calcula de forma automática la tarifa correspondiente según el tiempo de estacionamiento.

Puedes probarlo con cualquiera de las imágenes de ejemplo proporcionadas, o usar imágenes propias que contengan matrículas legibles.

---

## 🔐 Seguridad

- Las claves API se cargan desde `.env`
- El archivo `.env` no se sube al repositorio (incluido en `.gitignore`)

---

## 🚫 Licencia

Este proyecto se comparte con fines educativos y de demostración. Puedes adaptarlo para tu portfolio personal.

---

## ✨ Autor

Este proyecto forma parte de la Especialización de IA y Big data.
Desarrollado por **David Torres**. Si te gusta este proyecto, no dudes en dejar una estrella ⭐ o visitar mi perfil.



