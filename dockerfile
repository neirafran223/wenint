# Imagen base
FROM python:3.12-slim

# Definir directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todo el contenido del proyecto al contenedor
COPY TecnoStore /app/

# Copiar requerimientos al contenedor
COPY requerimientos.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r /app/requerimientos.txt

# Exponer el puerto donde correrá Django
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
