import google.generativeai as genai
from decouple import config
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde un archivo .env

# Configura la API Key desde tus variables de entorno
genai.configure(api_key=config("GOOGLE_API_KEY"))

def explicar_error_con_prompt(error_usuario: str, idioma: str = "español") -> str:
    """
    Llama al modelo Gemini para explicar un error del usuario en el idioma indicado.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Corrige y explica brevemente el siguiente error en {idioma}, usando un máximo de dos renglones. 
    No des saludos, no hagas introducción, no uses saltos de línea, responde directo y de forma concisa.

    Error del usuario: {error_usuario}

    Solo responde la explicación breve y resumida.
    """

    response = model.generate_content(prompt)
    explicacion = response.text.strip().replace('\n', ' ').replace('\\"', '"').replace("\"", "")
    return explicacion

# services/ia_services.py
# ... (imports existentes)
from google.cloud import texttospeech # <-- Asegúrate de que este import esté

# ... (tu función existente explicar_error_con_prompt)

# --- AÑADE ESTA NUEVA FUNCIÓN ---
def generar_audio_desde_texto(texto: str, codigo_idioma: str = "pt-BR") -> bytes:
    """Usa la API de Google Cloud para convertir texto en audio MP3."""
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=texto)
    voice = texttospeech.VoiceSelectionParams(
        language_code=codigo_idioma, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

# services/ia_services.py
# ... (imports existentes)
from google.cloud import speech # <-- Importa la nueva librería


def transcribir_audio_a_texto(audio_bytes: bytes, codigo_idioma: str = "pt-BR") -> str:
    """Usa la API de Google Cloud para transcribir audio a texto."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    
    # --- AQUÍ ESTÁ LA CORRECCIÓN ---
    config = speech.RecognitionConfig(
        # Le decimos a Google que el audio es de tipo WAV (LINEAR16)
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=codigo_idioma,
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return ""
    
from thefuzz import fuzz # <-- Importa la nueva librería
def verificar_similitud_frase(frase_usuario: str, frase_correcta: str, umbral: int = 80) -> bool:
    """
    Compara dos frases y devuelve True si su similitud es mayor o igual al umbral.
    La comparación no distingue entre mayúsculas y minúsculas.
    """
    # fuzz.ratio calcula la similitud de 0 a 100
    similitud = fuzz.ratio(frase_usuario.lower(), frase_correcta.lower())
    print(f"Similitud calculada: {similitud}%") # Log para depuración
    return similitud >= umbral