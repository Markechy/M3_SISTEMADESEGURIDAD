import face_recognition
import cv2
import os
import time
import subprocess
import requests
from numpy import argmin
from datetime import datetime

# Dirección donde se almacenan las caras conocidas
path_to_images = "/home/raspberry/Pictures/conocidos"
captured_images_path = "/home/raspberry/Pictures/temporales"

# URLs para interactuar con la base de datos
url_get_parking = "http://10.48.73.51:8080/proyecto/get_parking.php"
url_insert_actividad = "http://10.48.73.51:8080/proyecto/insertar_actividad.php"

# Extrae las codificaciones faciales de las imágenes conocidas
known_face_encodings = []
known_face_names = []

for filename in os.listdir(path_to_images):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(path_to_images, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)

        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

# Función para capturar una imagen con libcamera-still
def capture_image(image_path):
    subprocess.run(["libcamera-still", "-o", image_path, "--width", "640", "--height", "480", "--nopreview"])

# Función para obtener el estado más reciente del servidor
def obtener_estado_reciente(url_php):
    try:
        respuesta = requests.get(url_php, timeout=10)
        if respuesta.status_code == 200:
            return int(respuesta.text.strip())
        else:
            print("Error al obtener el estado reciente, código:", respuesta.status_code)
            return None
    except requests.RequestException as e:
        print("Error al realizar la solicitud GET:", e)
        return None


def obtener_fecha_hora_actual():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Función para insertar datos en la base de datos
def insertar_datos_en_actividad(url_php, nombre_conductor):
    fecha_hora = obtener_fecha_hora_actual()
    datos = {"nombre_conductor": nombre_conductor, "fecha_hora": fecha_hora}
    try:
        respuesta = requests.post(url_php, data=datos, timeout=10)
        print("Respuesta del servidor:", respuesta.text)
    except requests.RequestException as e:
        print("Error al realizar la solicitud POST:", e)

try:
    while True:
        print("Capturando imágenes...")
        captured_encodings = []
        image_paths = []

        # Captura 3 imágenes
        for i in range(3):
            image_filename = f"captured_image_{i + 1}.jpg"
            image_path = os.path.join(captured_images_path, image_filename)
            capture_image(image_path)
            image_paths.append(image_path)

            # Carga la imagen y extrae codificaciones faciales
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                captured_encodings.append(encodings[0])

        # Compara cada imagen capturada con las caras conocidas
        identified_person = None
        for encoding in captured_encodings:
            face_distances = face_recognition.face_distance(known_face_encodings, encoding)
            best_match_index = argmin(face_distances)

            # Verifica si hay coincidencias con un umbral de confianza
            threshold = 0.5
            if face_distances[best_match_index] < threshold:
                identified_person = known_face_names[best_match_index]
                break

        if identified_person:
            print(f"La persona es: {identified_person}")
            insertar_datos_en_actividad(url_insert_actividad, identified_person)
        else:
            print("No se encontró coincidencia, puede que sea un desconocido")
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            sospechoso_image = f"Desconocido_{timestamp}.jpg"
            carpeta_destino = "/home/raspberry/Pictures/sospechosos"
            ruta_sospechoso = os.path.join(carpeta_destino, sospechoso_image)
            subprocess.run(["cp", image_paths[0], ruta_sospechoso])

            # Verifica el estado reciente antes de activar la alarma
            estado_reciente = obtener_estado_reciente(url_get_parking)
            if estado_reciente == 0:
                subprocess.run(["python", "msg2.py", ruta_sospechoso]) and subprocess.run(["python", "inyeccion.py", ruta_sospechoso])
            else:
                print("El sistema está desactivado según el estado reciente.")

        # Limpia las imágenes capturadas temporalmente
        for image_path in image_paths:
            if os.path.exists(image_path):
                os.remove(image_path)

        # Esperar 30 segundos antes de la próxima captura
        print("Esperando 30 segundos para la siguiente captura...")
        time.sleep(30)

finally:
    print("Finalizando programa.")
