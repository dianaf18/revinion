from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from google.cloud import speech_v1p1beta1 as speech
import io
import os
from dotenv import load_dotenv

# Charger les credentials de Google Cloud depuis le fichier .env
load_dotenv()

# Vérifier que les variables sont bien définies
required_vars = ['GOOGLE_APPLICATION_CREDENTIALS', 'API_KEY', 'SECRET_KEY', 'FLASK_ENV']
for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"{var} not set in .env file")

# Utiliser les variables d'environnement
google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
flask_env = os.getenv('FLASK_ENV')

# Affichage des variables pour vérification (facultatif)
print("Google Credentials Path:", google_credentials)
print("API Key:", api_key)
print("Secret Key:", secret_key)
print("Flask Environment:", flask_env)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # Utiliser la clé secrète de votre fichier .env
socketio = SocketIO(app)

# Fonction pour transcrire l'audio en temps réel
def transcribe_streaming(stream):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)

    responses = client.streaming_recognize(config=streaming_config, requests=requests)
    return responses

@socketio.on('audio_stream')
def handle_audio_stream(audio_data):
    # Transcrire les données audio
    responses = transcribe_streaming(audio_data)
    for response in responses:
        for result in response.results:
            if result.is_final:
                text = result.alternatives[0].transcript
                # Traiter et organiser le texte
                organized_text = process_text(text)
                # Envoyer le texte organisé au frontend
                emit('transcription', {'data': organized_text})

# Fonction pour traiter le texte et extraire les informations clés
def process_text(text):
    # Placeholder pour le traitement NLP
    return text

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
