# 1. Usamos una imagen oficial, ligera y rápida de Python
FROM python:3.11-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiamos los requerimientos PRIMERO (Estrategia de Caché)
COPY ./app/requirements.txt /code/requirements.txt

# 4. Instalamos las dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiamos el resto del código de la aplicación
COPY ./app /code/app

# 6. Exponemos el puerto interno que usará FastAPI (Uvicorn)
EXPOSE 8000

# 7. El comando maestro para encender el servidor al levantar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]