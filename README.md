# 🔐 Lock-On - Sistema Antirrobo para Vehículos

Lock-On es un sistema de seguridad vehicular basado en visión computacional, sistemas embebidos y desarrollo multiplataforma, diseñado para la detección y verificación de conductores autorizados en tiempo real. El sistema utiliza reconocimiento facial para identificar usuarios registrados y generar alertas automáticas en caso de detectar posibles intrusos.

Este proyecto integra hardware (Raspberry Pi), backend en PHP, procesamiento en Python y una aplicación móvil, logrando una solución completa de seguridad inteligente.

---

## 📌 Características principales

- Reconocimiento facial en tiempo real
- Detección de conductores autorizados y sospechosos
- Envío automático de alertas por correo electrónico con evidencia fotográfica
- Registro de actividad del vehículo
- Modo "Valet Parking"
- Aplicación móvil para monitoreo y gestión de usuarios
- Base de datos MySQL para almacenamiento de información

---

## 🧠 Tecnologías utilizadas

- Python (visión computacional y reconocimiento facial)
- PHP (conexión con base de datos y backend)
- MySQL (gestión de datos)
- Kotlin / Android Studio (aplicación móvil)
- Raspberry Pi 5 (sistema embebido)
- OpenCV (procesamiento de imágenes)
- SMTP Gmail (envío de alertas)

---

## 📁 Estructura del proyecto

El repositorio está organizado en tres carpetas principales:

- **/python** → Contiene el código de visión computacional, reconocimiento facial y lógica de detección.
- **/php** → Incluye los scripts para conexión con base de datos, gestión de usuarios y comunicación del sistema.
- **/app** → Contiene la aplicación móvil desarrollada en Kotlin para monitoreo, control y visualización del sistema.

---

## ⚙️ Funcionamiento general

1. El sistema captura imágenes del conductor mediante una cámara conectada a Raspberry Pi.
2. Python procesa las imágenes y ejecuta el reconocimiento facial.
3. PHP gestiona la comunicación entre el sistema y la base de datos MySQL.
4. Si se detecta un usuario no registrado, se envía una alerta automática por correo con evidencia fotográfica.
5. La aplicación móvil permite visualizar actividad, usuarios registrados y alertas en tiempo real.

---

## 🚀 Objetivo del proyecto

Desarrollar un sistema de seguridad vehicular inteligente capaz de reducir el riesgo de robo mediante visión computacional, automatización y monitoreo remoto en tiempo real.

---

## 👨‍💻 Autor

Marco A. González Fernández  
Proyecto académico – Sistemas Embebidos Avanzados  
Tecnológico de Monterrey

---

## 📄 Nota

Este proyecto combina hardware y software en un sistema completo de seguridad vehicular, integrando inteligencia artificial ligera, sistemas embebidos y conectividad móvil para ofrecer una solución escalable y funcional.
