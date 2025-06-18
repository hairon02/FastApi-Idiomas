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
