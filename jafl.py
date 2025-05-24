from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import wikipedia
import random
import requests
import json
from collections import Counter
from datetime import datetime, timedelta

# 🔌 Lógica personalizada
from jafl_logic.assistant_logic import (
    analizar_emocion,
    detectar_tema,
    responder_a_usuario,
    guardar_estado_emocional,
    guardar_ultimo_mensaje,
    actualizar_tema
)

# 🗂️ Base de datos y respuestas
from jafl_logic.data import normalizar_texto, obtener_respuesta
from jafl_logic.database import (
    get_respuesta_de_base,
    agregar_respuesta_a_base,
    obtener_todas_respuestas
)

# 🌐 Configuración inicial
wikipedia.set_lang("es")
app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📁 Archivos web
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🧠 Contexto de conversación
contexto_conversacional = []

# 📬 Modelo
class ChatInput(BaseModel):
    mensaje: str

# 🔎 Wikipedia
def buscar_en_wikipedia(query):
    try:
        wikipedia.set_lang("en")
        resumen = wikipedia.summary(query, sentences=2)
        wikipedia.set_lang("es")
        return resumen
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Consulta ambigua. Algunas opciones son: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Tiempo de espera agotado con Wikipedia."
    except wikipedia.exceptions.RedirectError:
        return "No se encontró información exacta."
    except Exception as e:
        return f"Error inesperado: {e}"

# 🔎 Spyder client integration
BASE_URL = "http://127.0.0.1:5000"

def buscar_en_spyder(query):
    try:
        response = requests.get(f"{BASE_URL}/wikipedia", params={"query": query})
        response.raise_for_status()
        data = response.json()
        return data.get("result", "No se encontró resultado en Spyder.")
    except requests.RequestException as e:
        return f"Error al conectar con Spyder: {e}"
    except ValueError:
        return "Error al procesar la respuesta de Spyder."

# 🤔 Reflexión emocional
def reflexionar_emociones(ruta="emociones.json"):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        ultimos = [e for e in datos if datetime.fromisoformat(e["fecha"]) > datetime.now() - timedelta(days=3)]
        if not ultimos:
            return None

        emociones = [e["emocion"] for e in ultimos]
        conteo = Counter(emociones)
        total = sum(conteo.values())

        if conteo.get("triste", 0) >= 3:
            return "He notado que últimamente has estado expresando emociones negativas. Estoy contigo, Jota."
        elif conteo.get("feliz", 0) >= 3:
            return "¡Qué bien! Últimamente te he notado feliz. ¡Me alegra mucho eso, Jota!"
        elif conteo.get("neutro", 0) == total:
            return "Has estado muy neutro. ¿Querés charlar un poco más?"
    except Exception as e:
        print(f"Error reflexionando emociones: {e}")
    return None

# 🎯 Intención (si se usa Rasa)
def obtener_intencion_rasa(texto_usuario):
    try:
        response = requests.post(
            "http://localhost:5005/model/parse",
            json={"text": texto_usuario}
        )
        if response.status_code == 200:
            data = response.json()
            return data["intent"]["name"]
    except Exception as e:
        print("Error con Rasa:", e)
    return None

# 🌐 Cargar interfaz web
@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 💬 Chat principal
@app.post("/chat")
async def chat(chat_input: ChatInput):
    user_input = chat_input.mensaje.strip()
    if not user_input:
        raise HTTPException(status_code=400, detail="Mensaje vacío.")

    contexto_conversacional.append(f"Tú: {user_input}")
    guardar_ultimo_mensaje(user_input)
    emocion = analizar_emocion(user_input)
    guardar_estado_emocional(emocion)

    reflexion = reflexionar_emociones()
    if reflexion:
        contexto_conversacional.append(f"JAFL: {reflexion}")
        return {"respuesta": reflexion}

    intencion = obtener_intencion_rasa(user_input)
    if not intencion:
        tema = detectar_tema(user_input)
        actualizar_tema(tema)
        intencion = tema

    # 📄 Consulta PDF
    if user_input.lower().startswith("pdf:"):
        from jafl_logic.aprendizaje import buscar_en_pdf
        query = user_input[4:].strip()
        respuesta_pdf = buscar_en_pdf(query)
        respuesta = respuesta_pdf or "No encontré información útil en ese documento."
        contexto_conversacional.append(f"JAFL: (📄 fuente: PDF)\n{respuesta}")
        return {"respuesta": f"(📄 fuente: PDF)\n{respuesta}"}

    # 🔍 Consulta Spyder
    if user_input.lower().startswith("spyder:"):
        query = user_input[7:].strip()
        respuesta_spyder = buscar_en_spyder(query)
        contexto_conversacional.append(f"JAFL: (🔍 fuente: Spyder)\n{respuesta_spyder}")
        return {"respuesta": f"(🔍 fuente: Spyder)\n{respuesta_spyder}"}

    # 🌍 Consulta Wikipedia
    if user_input.lower().startswith("wiki:"):
        query = user_input[5:].strip()
        respuesta_wiki = buscar_en_wikipedia(query)
        contexto_conversacional.append(f"JAFL: (🌐 fuente: Wikipedia)\n{respuesta_wiki}")
        return {"respuesta": f"(🌐 fuente: Wikipedia)\n{respuesta_wiki}"}

    # 🧠 Buscar en base de datos local
    respuesta = get_respuesta_de_base(user_input)

    if respuesta:
        contexto_conversacional.append(f"JAFL: {respuesta}")
        return {"respuesta": respuesta}
    else:
        # 🧠 Generar nueva respuesta con lógica mejorada desde data.py
        respuestas_generadas = obtener_respuesta(user_input)
        # obtener_respuesta devuelve lista; elegimos una respuesta aleatoria
        respuesta_local = random.choice(respuestas_generadas)
        contexto_conversacional.append(f"JAFL: {respuesta_local}")
        agregar_respuesta_a_base(user_input, respuesta_local)
        return {"respuesta": respuesta_local}

# 🔁 Ejecutar
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
