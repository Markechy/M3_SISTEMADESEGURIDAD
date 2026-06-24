import requests
import base64
import os
from datetime import datetime

def convertir_imagen_a_base64(ruta_imagen):
    """Convierte una imagen en base64."""
    try:
        with open(ruta_imagen, "rb") as file:
            # Lee el archivo y codifica en base64
            imagen_base64 = base64.b64encode(file.read()).decode('utf-8')
            return imagen_base64
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_imagen}")
        return None

def insertar_sospechoso(url_php, ruta_imagen):
    """Envía los datos a la base de datos mediante una solicitud POST."""
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Convertir la imagen a base64
    imagen_base64 = convertir_imagen_a_base64(ruta_imagen)
    
    if imagen_base64 is None:
        print("No se pudo convertir la imagen a base64. Verifica la ruta del archivo.")
        return
    
    # Crear los datos a enviar
    datos = {
        "fecha": fecha_actual,
        "foto": imagen_base64
    }
    
    # Realizar la solicitud POST
    try:
        respuesta = requests.post(url_php, data=datos, timeout=10)
        print("Respuesta del servidor:", respuesta.text)
    except requests.RequestException as e:
        print("Error al realizar la solicitud POST:", e)

def obtener_ultima_imagen(directorio):
    """Obtiene la ruta de la última imagen añadida a una carpeta."""
    try:
        # Lista de archivos en el directorio con sus rutas completas
        archivos = [os.path.join(directorio, archivo) for archivo in os.listdir(directorio) 
                    if archivo.lower().endswith(('.jpg', '.png')) and os.path.isfile(os.path.join(directorio, archivo))]
        
        if not archivos:
            print("No se encontraron imágenes en el directorio.")
            return None
        
        # Ordenar archivos por fecha de modificación
        ultima_imagen = max(archivos, key=os.path.getmtime)
        return ultima_imagen
    except Exception as e:
        print(f"Error al buscar la última imagen: {e}")
        return None

# Configuración
url_php = "http://10.48.73.51:8080/proyecto/insertar_sospechoso.php"
directorio = "/home/raspberry/Pictures/sospechosos"  # Ruta del directorio con imágenes

# Obtener la última imagen del directorio
ruta_ultima_imagen = obtener_ultima_imagen(directorio)

if ruta_ultima_imagen:
    print(f"Última imagen encontrada: {ruta_ultima_imagen}")
    insertar_sospechoso(url_php, ruta_ultima_imagen)
else:
    print("No se pudo encontrar una imagen para enviar.")
