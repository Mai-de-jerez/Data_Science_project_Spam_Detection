# Usa una imagen base de Python 3.13 (slim-buster es ligera)
FROM python:3.11-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 1. Crea el directorio para los datos de NLTK y asegura permisos.
RUN mkdir -p /usr/share/nltk_data

# 2. Establece la variable de entorno NLTK_DATA para que NLTK sepa dónde buscar.
ENV NLTK_DATA /usr/share/nltk_data

# 3. Descarga los recursos de NLTK directamente a esa ubicación.
#    Usamos 'corpora/stopwords' y 'tokenizers/punkt' para ser muy específicos.
#    El comando 'python -m nltk.downloader' es más robusto que 'nltk.download()'.
RUN python -m nltk.downloader -d /usr/share/nltk_data stopwords
RUN python -m nltk.downloader -d /usr/share/nltk_data punkt

# Copia todos los demás archivos de tu aplicación al contenedor
COPY . .

# Expone el puerto en el que la aplicación Flask va a escuchar
EXPOSE 5000

# Comando para ejecutar la aplicación Flask cuando el contenedor se inicie
CMD ["python", "app.py"]