# app.py

# --- 1. Librerías estándar de Python ---
import re
import numpy as np 

# --- 2. Librerías de terceros ---
import joblib
from flask import Flask, request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy.sparse import hstack # Needed to combine sparse TF-IDF vector with dense message length

# --- Inicialización de Flask ---
app = Flask(__name__)


stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# This function cleans the text of SMS messages.
def preprocess_text(text):
    """
    Preprocesa un mensaje de texto SMS aplicando los siguientes pasos:
    1. Convierte el texto a minúsculas.
    2. Elimina caracteres no alfabéticos (números, puntuación) y los reemplaza con espacios.
    3. Elimina espacios extra.
    4. Divide el texto en palabras y elimina stopwords.
    5. Aplica stemming (reduce palabras a su raíz) utilizando Porter Stemmer.
    
    Args:
        text (str): El mensaje SMS original.
        
    Returns:
        str: El mensaje preprocesado como una cadena de texto.
    """
    if not isinstance(text, str): # Handle potential non-string input
        return ""
    text = text.lower() # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', ' ', text) # Remove non-alphabetic characters (punctuation, numbers), replace with space
    text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single and remove leading/trailing spaces
    words = text.split() # Split text into words
    filtered_words = [word for word in words if word not in stop_words] # Remove stopwords
    stemmed_words = [stemmer.stem(word) for word in filtered_words] # Apply stemming
    return ' '.join(stemmed_words) # Join processed words into a string

try:
    # Rutas actualizadas para el modelo de Regresión Logística afinado y el vectorizador TF-IDF
    model_path = 'model_logistic_regression_tuned.joblib'
    vectorizer_path = 'vectorizer_tfidf.joblib'

    loaded_model = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)
    print("Modelo y vectorizador cargados con éxito para la API.")
except FileNotFoundError:
    print("ERROR: No se encontraron los archivos del modelo o vectorizador.")
    print(f"Asegúrate de que '{model_path}' y '{vectorizer_path}' existan en el mismo directorio que 'app.py'.")
    # Si no se pueden cargar, la API no puede funcionar, así que salimos.
    exit()

# --- Definición de la ruta de la API para clasificar SMS ---
# Esta ruta manejará las solicitudes POST enviadas a '/classify_sms'.
@app.route('/classify_sms', methods=['POST'])
def classify_sms_api():
    """
    Clasifica un mensaje SMS como 'SPAM' o 'HAM' basado en el modelo entrenado.
    Espera un JSON con la clave 'message'.
    """
    # 1. Obtener el cuerpo de la solicitud en formato JSON.
    # 'silent=True' evita un error si el cuerpo no es JSON válido, devolviendo None.
    data = request.json 
    
    if not data or 'message' not in data:
        print("Error: JSON inválido o 'message' no encontrado.")
        return jsonify({"error": "Formato JSON inv\u00e1lido o 'message' no proporcionado en el cuerpo de la solicitud."}), 400

    sms_message = data['message'] # Extraer el mensaje SMS del JSON

    # 2. Preprocesar el mensaje utilizando la misma función de preprocesamiento del notebook.
    clean_sms = preprocess_text(sms_message)

    # 3. Calcular la longitud del mensaje preprocesado (¡nueva característica!)
    message_length = np.array([len(clean_sms)]).reshape(-1, 1)

    # 4. Vectorizar el mensaje utilizando el vectorizador cargado.
    # Es crucial pasar el mensaje como una lista: [clean_sms] porque .transform() espera una secuencia de documentos.
    sms_vectorized = loaded_vectorizer.transform([clean_sms])

    # 5. Combinar el vector TF-IDF con la característica de longitud del mensaje.
    # Esto debe coincidir con cómo se entrenó el modelo (hstack).
    sms_combined_features = hstack([sms_vectorized, message_length])

    # 6. Realizar la predicción con el modelo cargado.
    # [0] se usa para obtener el valor de la predicción (0 para HAM, 1 para SPAM).
    prediction = loaded_model.predict(sms_combined_features)[0]

    # 7. Convertir la predicción numérica a una etiqueta legible.
    result_label = "SPAM" if prediction == 1 else "HAM"

    # 8. Devolver la respuesta en formato JSON.
    return jsonify({
        "original_message": sms_message,
        "preprocessed_message": clean_sms, 
        "prediction": result_label
    })

# --- Ruta de "saludo" o "home" (opcional) ---
# Esta ruta GET es útil para verificar que la API está funcionando simplemente visitando la URL base.
@app.route('/', methods=['GET'])
def home():
    return "¡API de Detección de Spam activa! Envía una solicitud POST a /classify_sms con tu mensaje."

# --- Ejecutar la aplicación Flask ---
if __name__ == '__main__':
    # 'debug=True' es excelente para el desarrollo:
    # - Recarga automáticamente el servidor cuando detecta cambios en el código.
    # - Proporciona mensajes de error detallados en el navegador.
    # Usar debug=False en un entorno de producción por razones de seguridad y rendimiento!
    
    # 'host='0.0.0.0'' hace que el servidor sea accesible desde cualquier IP en tu red local (no solo localhost).
    # 'port=5000' es el puerto predeterminado de Flask.
    app.run(debug=True, host='0.0.0.0', port=5000)