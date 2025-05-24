from jafl_logic.cerebro import (
    guardar_estado_emocional,
    guardar_ultimo_mensaje,
    actualizar_tema,
    generar_reflexion
)
from jafl_logic.aprendizaje import buscar_en_pdf, analizar_emocion  # IMPORTA ambas funciones
import wikipedia
from jafl_logic import data_manager
import requests
import random

def guardar_emocion(nombre_usuario, emocion, mensaje):
    guardar_estado_emocional(emocion)
    guardar_ultimo_mensaje(mensaje)

def detectar_intencion(mensaje):
    mensaje = mensaje.lower()
    if any(x in mensaje for x in ["hola", "buenos días", "buenas tardes", "saludo"]):
        return "saludo"
    elif any(x in mensaje for x in ["adiós", "chao", "hasta luego"]):
        return "despedida"
    elif "pdf:" in mensaje:
        return "consulta_pdf"
    elif "wiki:" in mensaje:
        return "consulta_wikipedia"
    elif any(x in mensaje for x in ["triste", "mal", "deprimido"]):
        return "emocion_negativa"
    elif any(x in mensaje for x in ["feliz", "contento", "alegre"]):
        return "emocion_positiva"
    else:
        return "desconocido"

def diagnosticar_estado_mental(texto):
    texto = texto.lower()
    if "estoy muy triste" in texto or "no quiero seguir" in texto:
        return "Parece que estás pasando por un momento difícil, Jota. Si quieres, puedo escucharte."
    elif "me siento bien" in texto or "estoy feliz" in texto:
        return "Me alegra saber que estás bien, Jota."
    return None

respuestas = {
    "saludo": [
        "Hola Jota, ¿cómo estás?",
        "¡Hola! ¿En qué puedo ayudarte hoy?",
    ],
    "despedida": [
        "Hasta luego, Jota. ¡Cuídate!",
        "Nos hablamos pronto, Jota.",
    ],
    "emocion_negativa": [
        "Estoy acá con vos, Jota. ¿Querés hablar un poco más?",
        "Siento que no te estás sintiendo bien. ¿Querés que te escuche?",
    ],
    "emocion_positiva": [
        "¡Me alegra mucho saber eso!",
        "Qué bien que estés así, ¡yo también me siento motivado!",
    ],
    "consulta_pdf": [],
    "consulta_wikipedia": [],
    "desconocido": [
        "No estoy seguro de entender, pero puedo buscar en Wikipedia o en mis documentos.",
        "Podés intentar preguntarme de otra forma, Jota.",
    ],
}

def manejar_consulta_pdf(mensaje):
    query = mensaje.lower().replace("pdf:", "").strip()
    resultado = buscar_en_pdf(query)
    if resultado:
        return resultado
    return "No encontré información útil en ese documento."

def manejar_consulta_wikipedia(mensaje):
    query = mensaje.lower().replace("wiki:", "").strip()
    return consultar_spyder(query)

def consultar_spyder(query):
    url = "http://127.0.0.1:5000/wikipedia"
    try:
        response = requests.get(url, params={"query": query}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return f"[Error Spyder]: {data['error']}"
        return data.get("translated_text", data.get("summary", "No hay resumen disponible."))
    except requests.RequestException as e:
        return f"[Error conexión Spyder]: {str(e)}"

def detectar_tema(texto):
    texto = texto.lower()
    temas_clave = ["tarea", "ayuda", "vida", "trabajo", "amigo", "emocion", "sentimiento", "pdf", "wiki"]
    for tema in temas_clave:
        if tema in texto:
            return tema
    return "general"

# --- NUEVA FUNCIÓN AGREGADA para que jafl.py la use ---
def responder_a_usuario(mensaje):
    intencion = detectar_intencion(mensaje)
    
    if intencion == "consulta_pdf":
        return manejar_consulta_pdf(mensaje)
    elif intencion == "consulta_wikipedia":
        return manejar_consulta_wikipedia(mensaje)
    elif intencion in respuestas:
        return random.choice(respuestas[intencion])
    else:
        return random.choice(respuestas["desconocido"])
