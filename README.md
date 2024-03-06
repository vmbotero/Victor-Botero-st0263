# ST0263 - Topicos especiales en telemática

## Estudiante
- Victor Manuel Botero Gómez
- Email: mvmboterog@eafit.edu.co

## Profesor
- Alvaro Enrique Ospina Sanjuan
- Email: aeospinas@eafit.edu.co

# Reto N° 1 y 2
## 1. Descripción de la actividad
<Sistema P2P de intercambio de archivos. Desarrollado en python con flask y gRPC para la comunicación entre peers.>

### 1.1. Requerimientos cumplidos
- Desarrollo del servidor primario mediante la utilización de Flask.
- Administración de usuarios, incluyendo el inicio y cierre de sesión, así como la gestión de archivos, abarcando la indexación y búsqueda.
- Creación del servidor y cliente gRPC para facilitar la transferencia de archivos, tanto en la carga como en la descarga.

## 2. Diseño e información general
<El proyecto se adhiere a una arquitectura P2P, permitiendo a los usuarios compartir archivos directamente entre sí. La gestión de la información del usuario y los archivos compartidos se lleva a cabo mediante un servidor central implementado en Flask. La transferencia de archivos se efectúa a través de gRPC.>

<img src="https://postimg.cc/hJdY9w6B">

## 3. Ambiente de desarrollo
- Lenguaje de Programación: Python
- Librerías:  Flask, pymongo, grpc, concurrent.futures
- MongoDB para la gestión de datos

### Cómo compilar y ejecutar
<Para ejecutar el servidor principal (server.py), se debe asegurar que MongoDB esté corriendo y luego en una terminal ejecutar:
py server.py>

<Para el servidor gRPC (p_server.py) deberá ejecutar lo siguiente en otra terminal independiente:
py p_server.py>

<Para el cliente (p_client.py), recuerde utilizar otra terminal y ejecute:
py p_client.py>

<img src="https://docs.google.com/document/d/13UgVoN-MHM2qdVKevYDGSJvoaxu1-W1RNSEjC8auNW0/edit?usp=sharing">


### Detalles de Desarrollo y Técnicos
- La información de los usuarios y los archivos compartidos se almacena en una base de datos SQLite.
- Por defecto, las direcciones IP y los puertos están configurados para operar en el entorno local.

### Resultados o pantallazos
<Incluir imágenes o capturas de pantalla si es necesario.>

<img src="https://www.canva.com/design/DAF-s4b3Dwo/DpQQ7ZIQJMeADuN-9W6WQA/view?utm_content=DAF-s4b3Dwo&utm_campaign=designshare&utm_medium=link&utm_source=recording_view">

## 4. Ambiente de ejecución

### IP o Nombres de Dominio
- IP del servidor Flask: 127.0.0.1:5000
- IP del servidor gRPC: [::]:3000

### Guía de Usuario
- Los usuarios pueden registrarse, iniciar y cerrar sesión mediante el servidor Flask.
- Los archivos se pueden cargar y descargar usando el cliente y servidor gRPC.

## 5. Información Adicional
<Cualquier otra información que consideres relevante para esta actividad.>

## Referencias
- https://grpc.io/docs/languages/python/basics/
- https://devjaime.medium.com/microservicios-de-python-con-grpc-3ff25126b6eb
- https://flask-es.readthedocs.io/