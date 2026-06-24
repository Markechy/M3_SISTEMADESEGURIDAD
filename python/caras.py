import requests
import base64
import os
import subprocess
import time

# Define las rutas de las carpetas
directorio = "/home/raspberry/Pictures/conocidos"
dir_base_datos = r"C:\Users\mario\Desktop\facedetection\base_Datos\INSERCION"

# Crear la carpeta si no existe
os.makedirs(directorio, exist_ok=True)

# URL del PHP
url_php = "http://10.48.73.51:8080/proyecto/obtener_usuarios.php"

# Intervalo de tiempo en segundos entre cada actualización
intervalo_actualizacion = 300  # 5 minutos

while True:
    try:
        # Limpia el directorio antes de descargar nuevas imágenes
        print("Limpiando el directorio de imágenes...")
        for archivo in os.listdir(directorio):
            ruta_archivo = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        print("Directorio limpio.")

        # Realizar la solicitud GET al servidor
        print("Solicitando nuevas imágenes desde la base de datos...")
        respuesta = requests.get(url_php, timeout=10)
        respuesta.raise_for_status()  # Lanza una excepción si ocurre un error HTTP

        # Convertir la respuesta JSON a un objeto Python
        usuarios = respuesta.json()

        # Procesar cada usuario y guardar su imagen
        for usuario in usuarios:
            nombre = usuario["nombre"]
            foto_base64 = usuario["foto"]

            # Decodificar la imagen base64
            imagen = base64.b64decode(foto_base64)

            # Crear el nombre del archivo de la imagen
            nombre_archivo = os.path.join(directorio, f"{nombre}.jpg")

            # Guardar la imagen en el archivo
            with open(nombre_archivo, "wb") as file:
                file.write(imagen)
            print(f"Imagen guardada: {nombre_archivo}")

        # Ejecutar el script de detección facial
        subprocess.run(["python", "facedetect.py", directorio])

    except requests.RequestException as e:
        print(f"Error al realizar la solicitud GET: {e}")
    except KeyError as e:
        print(f"Error al procesar los datos recibidos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Esperar antes de la próxima actualización
    print(f"Esperando {intervalo_actualizacion} segundos antes de la próxima actualización...")
    time.sleep(intervalo_actualizacion)
