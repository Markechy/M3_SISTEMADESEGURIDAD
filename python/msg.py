import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


# Servidor SMTP
smtp_config = {
    'host': 'smtp.gmail.com',     
    'port': 587,
    'email': 'lockoncubica@gmail.com',
    'password': 'ojpb ocwk tsev qxxn'
}

# Obtener los correos y nombres desde el archivo PHP
def get_email_and_names():
    try:
        # Realizar la solicitud al archivo PHP
        response = requests.get('http://10.48.73.51:8080/proyecto/get_mail.php')
        data = response.json()

        email_list = data['emails']
        name_list = data['names']

        return email_list, name_list

    except Exception as e:
        print(f"Error al obtener los datos desde el PHP: {e}")
        return [], []

# Obtener la última imagen de la carpeta "sospechosos"
def get_last_image(folder_path):
    try:
        # Filtrar los archivos por su formato
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        if not files:
            return None
        # Obtener ruta de los archivos
        files = [os.path.join(folder_path, f) for f in files]
        # Ordenar por más reciente
        files.sort(key=os.path.getmtime, reverse=True)
        # Retornar la última imagen
        return files[0]
    except Exception as e:
        print(f"Error al obtener la última imagen: {e}")
        return None

# Función para enviar correos electrónicos con imagen adjunta
def send_emails(email_list, name_list, image_path):
    try:
        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        server.starttls()
        server.login(smtp_config['email'], smtp_config['password'])

        for i, recipient in enumerate(email_list):
            msg = MIMEMultipart()
            msg['From'] = smtp_config['email']
            msg['To'] = recipient
            msg['Subject'] = "Alerta de seguridad"

            # Cuerpo del mensaje
            timestamp = time.strftime("%d-%m-%Y %H:%M:%S")
            body = (
                f"Estimado/a {name_list[i]['nombre']} {name_list[i]['apellido_paterno']} {name_list[i]['apellido_materno']},\n\n"
                f"Se ha detectado una actividad sospechosa el día {timestamp}.\n"
                "¿Reconoces a esta persona?\n"
                "Si no reconoces a esta persona, contacta a Locatel para reportar el robo de tu vehículo.\n"
                "Número de Locatel: 55 5658-1111\n"
                "Número de emergencias: 911"
            )
            msg.attach(MIMEText(body, 'plain'))

            # Adjuntar la imagen
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
                    msg.attach(part)
                print(f"Imagen adjunta: {os.path.basename(image_path)}")
            else:
                print("No se encontró ninguna imagen válida en la carpeta.")

            # Enviar correo
            server.sendmail(smtp_config['email'], recipient, msg.as_string())
            print(f"Correo enviado a: {recipient}")

    except Exception as e:
        print(f"Error enviando correos: {e}")
    finally:
        server.quit()

# Script principal
if __name__ == "__main__":
    folder_path = "/home/raspberry/Pictures/sospechosos" 
    image_path = get_last_image(folder_path)

    email_list, name_list = get_email_and_names()  

    if image_path:
        print(f"Última imagen encontrada: {image_path}")
        if email_list and name_list:
            send_emails(email_list, name_list, image_path)
        else:
            print("No se encontraron correos o nombres en la base de datos.")
    else:
        print("No se encontraron imágenes en la carpeta.")
