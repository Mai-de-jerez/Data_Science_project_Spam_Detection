# 🚀 DATA SCIENCE PROJECT SPAM DETECTION 🚀
¡Bienvenido a la API de Detección de Spam SMS! Este proyecto es el resultado de un esfuerzo por crear una solución robusta y reproducible para clasificar mensajes de texto como "SPAM" o "HAM" (no spam) utilizando técnicas de Machine Learning y desplegándola como un servicio web con Docker.

## ✨ Esencia del Proyecto
El corazón de este proyecto es un modelo de Machine Learning entrenado para identificar patrones en mensajes SMS que indican si son spam o no. Hemos transformado este modelo en una API accesible a través de HTTP, lo que permite a cualquier aplicación o servicio enviar un mensaje y recibir una predicción instantánea. Todo esto está empaquetado en un contenedor Docker, garantizando que la API funcione de manera consistente en cualquier entorno.

## 📊 DATA COLLECTION
La calidad de los datos es fundamental. Para este proyecto, utilizamos y expandimos nuestro dataset:

**Dataset Inicial (spam.csv):** Comenzamos con un dataset clásico de detección de spam SMS, ampliamente utilizado en la comunidad de Machine Learning, a menudo disponible en repositorios como el UCI Machine Learning Repository. Este dataset nos proporcionó una base sólida de mensajes etiquetados.

**Nuevos Datos (train.parquet, test.parquet):** Tras una fase inicial de desarrollo, identificamos la necesidad de mejorar la robustez del modelo. Esto nos llevó a una fase de expansión y mejora del dataset, donde los datos originales fueron procesados, posiblemente combinados con fuentes adicionales o enriquecidos, y luego divididos en formatos train.parquet y test.parquet para una gestión más eficiente y un mejor rendimiento en el entrenamiento. Estos archivos representan la versión final y optimizada de nuestro conjunto de datos para el entrenamiento y evaluación.

## 🧹 DATA WRANLING (Procesamiento de Datos)
El texto es ruidoso, y para que nuestros modelos lo entiendan, necesitamos limpiarlo a fondo. Realizamos un proceso de preprocesamiento riguroso y consistente:

### **Fase Inicial (con spam.csv):**

- **Conversión a Minúsculas:** Estandarización de todo el texto.

- **Eliminación de Caracteres No Alfabéticos:** Eliminación de números, símbolos y puntuación, reemplazándolos con espacios para no unir palabras.

- **Tokenización:** División de los mensajes en palabras individuales.

- **Eliminación de Stopwords:** Eliminación de palabras comunes (ej., "el", "la", "y") que no aportan significado a la clasificación.

- **Stemming (Porter Stemmer):** Reducción de las palabras a su raíz (ej., "corriendo" -> "corr", "mejoras" -> "mejor") para unificar términos relacionados.

- **Normalización de Espacios:** Eliminación de múltiples espacios y espacios al inicio/final.

## **Fase de Mejora (con train.parquet, test.parquet):**

Se aplicaron exactamente los mismos pasos de preprocesamiento de manera consistente a los nuevos datos para asegurar la uniformidad y evitar sesgos en el modelo. La consistencia en el preprocesamiento es crucial para que el modelo interprete correctamente los datos nuevos.

##  FEATURE ENGINEERING ⚙️

Para transformar el texto limpio en un formato numérico que el modelo pueda procesar, utilizamos:

- **Vectorización TF-IDF (Term Frequency-Inverse Document Frequency):** Esta técnica asigna un peso numérico a cada palabra, reflejando su importancia en un mensaje y en el conjunto total de mensajes. Nos permitió capturar la relevancia de los términos en la detección de spam.

- **Longitud del Mensaje:** Añadimos la longitud del mensaje preprocesado como una característica numérica adicional. Esta característica resultó ser muy potente, ya que los mensajes de spam suelen tener longitudes muy diferentes a los mensajes legítimos.

## 🧠 DESARROLLO Y EVALUACIÓN DE LOS MODELOS

A lo largo del proyecto, exploramos diferentes algoritmos de Machine Learning:

- **Modelos Iniciales:** Comenzamos con modelos como Naive Bayes, que son un buen punto de partida para la clasificación de texto.

- **Iteración y Mejora:** Tras evaluar el rendimiento inicial, identificamos áreas de mejora. Esto nos llevó a la decisión de incorporar más datos y refinar nuestro enfoque.

- **Modelo Campeón (Regresión Logística Afinada):** Finalmente, optamos por un modelo de Regresión Logística. Este modelo fue afinado (optimizando sus hiperparámetros) para lograr la máxima precisión y robustez en la clasificación de spam. La combinación de la vectorización TF-IDF y la característica de longitud del mensaje con este modelo resultó ser la más efectiva.

## 🌐 Construcción y Dockerización de la API

El objetivo final era hacer que nuestro modelo fuera accesible.

- **Primera Iteración de la API:** Construimos una API inicial con Flask para exponer el modelo. Sin embargo, al probarla, nos dimos cuenta de que el modelo inicial y el dataset no eran lo suficientemente robustos.

- **Mejora Continua:** Esto nos impulsó a una segunda fase de desarrollo, donde obtuvimos y procesamos más datos, y entrenamos el modelo de Regresión Logística afinado.

- **Dockerización (¡El Desafío Final!):** Para garantizar la reproducibilidad y facilitar el despliegue, decidimos contenerizar la API con Docker. Este proceso implicó:

- Definir el entorno Python y las dependencias en Dockerfile y requirements.txt.

- Asegurar que los datos de NLTK (como las stopwords) se descargaran correctamente dentro del contenedor, lo cual fue un desafío debido a la naturaleza aislada de Docker.

- Manejar las versiones de Python y librerías para evitar conflictos.

¡Finalmente, lo logramos! La API ahora se empaqueta y ejecuta perfectamente en un contenedor Docker, lista para ser utilizada en cualquier entorno.

## 🚀 Cómo Usar y Probar la API 

¡Si quieres ver esta API en acción, sigue estos sencillos pasos!

**1. Requisitos Previos**
  
Necesitarás tener Docker Desktop (para Windows/macOS) o Docker Engine (para Linux) instalado en tu sistema. Puedes descargarlo desde docker.com.

_Nota: También puedes optar por ejecutar Docker dentro de una máquina virtual (VM) con un sistema operativo Linux (como Ubuntu), tal como se hizo en el desarrollo de este proyecto. Esto proporciona un entorno aislado y controlado para Docker._  

**2. Clonar el Repositorio**
  
Abre tu terminal (o Git Bash/PowerShell en Windows) y clona este repositorio:

```
git clone https://github.com/Mai-de-jerez/Data_Science_project_Spam_Detection.git
cd Data_Science_project_Spam_Detectio
```

**3. Construir la Imagen Docker**
  
Una vez dentro de la carpeta del proyecto, construye la imagen Docker. Este comando descargará la imagen base de Python, instalará todas las dependencias (incluyendo scikit-learn, nltk, numpy, scipy, flask, joblib) y descargará los datos de NLTK necesarios.

```
docker build -t spam-detector-api .
```

Este proceso puede tardar unos minutos la primera vez, ya que Docker necesita descargar las capas necesarias.

**4. Lanzar el Contenedor Docker**
  
Una vez que la imagen se haya construido con éxito, lanza el contenedor. Esto iniciará tu API de Flask en el puerto 5000 de tu máquina.

```
docker run -p 5000:5000 spam-detector-api
```

Verás los mensajes de inicio de Flask en tu terminal. Deja esta terminal abierta, ya que es donde se está ejecutando la API.

**5. Probar la API**
  
Ahora, abre una segunda terminal (o usa una herramienta como Postman o Insomnia) para enviar solicitudes a tu API.

La API espera solicitudes POST a la ruta /classify_sms con un cuerpo JSON que contenga la clave "message".

**Ejemplo de Mensaje SPAM (usando curl):**

```
curl -X POST -H "Content-Type: application/json" -d '{ "message": "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C'\''s apply." }' http://localhost:5000/classify_sms
```

Respuesta esperada:

```
{
  "original_message": "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply.",
  "prediction": "SPAM",
  "preprocessed_message": "free entri wkli comp win fa cup final tkt st may text fa receiv entri question std txt rate c appli"
}
```

Ejemplo de Mensaje HAM (No Spam) (usando curl):

```
curl -X POST -H "Content-Type: application/json" -d '{ "message": "Hey, how are you doing today? Let'\''s catch up soon." }' http://localhost:5000/classify_sms
```

Respuesta esperada:

```
{
  "original_message": "Hey, how are you doing today? Let's catch up soon.",
  "prediction": "HAM",
  "preprocessed_message": "hey do today let catch soon"
}
```

¡Y eso es todo! ¡Ya tienes tu API de detección de spam funcionando localmente!
