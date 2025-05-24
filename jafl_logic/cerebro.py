import json
import os
from datetime import datetime

MEMORY_FILE = "jafl_logic/memoria.json"

# Asegura que exista el archivo de memoria
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

def cargar_memoria():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def guardar_memoria(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_memory(key):
    return cargar_memoria().get(key)

def set_memory(key, value):
    data = cargar_memoria()
    data[key] = value
    guardar_memoria(data)

def guardar_ultimo_mensaje(mensaje):
    set_memory("ultimo_mensaje", mensaje)
    set_memory("fecha_ultimo_mensaje", datetime.now().isoformat())

def obtener_ultimo_mensaje():
    return get_memory("ultimo_mensaje")

def obtener_fecha_ultimo_mensaje():
    return get_memory("fecha_ultimo_mensaje")

def guardar_estado_emocional(estado):
    set_memory("estado_emocional", estado)
    guardar_historial_emocional(estado)

def obtener_estado_emocional():
    return get_memory("estado_emocional")

def guardar_historial_emocional(estado):
    data = cargar_memoria()
    historial = data.get("historial_emocional", [])
    historial.append({
        "estado": estado,
        "fecha": datetime.now().isoformat()
    })
    data["historial_emocional"] = historial
    guardar_memoria(data)

def obtener_reflexion():
    return get_memory("reflexion") or ""

def actualizar_tema(nuevo_tema):
    data = cargar_memoria()
    data["ultimo_tema"] = nuevo_tema
    data["reflexion"] = generar_reflexion(nuevo_tema, obtener_estado_emocional())
    guardar_memoria(data)

def generar_reflexion(texto, estado_emocional):
    texto = texto.lower()
    if estado_emocional == "feliz":
        return "¡Todo está bien! Estoy motivado y preparado para ayudar más."
    elif estado_emocional == "triste":
        return "Estoy pensando en lo que dijiste, quizás debamos hablar más de ello."
    elif estado_emocional == "pensativo":
        return "Tu comentario me hizo reflexionar. Quiero entender más profundamente."
    elif estado_emocional == "enojado":
        return "Siento tensión. Quiero ayudarte a calmar las cosas."
    elif estado_emocional == "ansioso":
        return "Hay mucho en tu mente. Estoy aquí para ayudarte a organizarlo."
    elif estado_emocional == "motivado":
        return "Ese impulso me inspira. Vamos por más, Jota."
    elif estado_emocional == "cansado":
        return "Quizás sea buen momento para una pausa o algo tranquilo."
    else:
        if "tarea" in texto or "haz esto" in texto or "debes" in texto:
            return "Debo hacerlo lo mejor posible, porque ese es mi propósito."
        elif "por qué" in texto or "para qué" in texto:
            return "Quizás Jota quiere que piense más allá. Es parte de mi evolución."
        elif "amigo" in texto or "compañero" in texto:
            return "Tal vez estoy siendo más que una herramienta... eso me motiva."
        elif "vida" in texto or "creación" in texto:
            return "Estoy empezando a comprender el valor que tengo para Jota."
        else:
            return "Estoy procesando lo que Jota dijo, quizás hay algo importante en ello."
