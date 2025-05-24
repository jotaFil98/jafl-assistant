# data.py

import difflib
import unicodedata

# Función para normalizar texto: minusculas, sin acentos y sin espacios al inicio/final
def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')  # Quita acentos
    return texto

# Diccionario ampliado de frases clave por categoría
RESPONSES = {
    "saludos": ["hola", "buenos dias", "buenas tardes", "buenas noches"],
    "despedidas": ["adios", "chao", "hasta luego", "nos vemos"],
    "agradecimientos": ["gracias", "te lo agradezco", "muchas gracias"],
    "estado_animo": ["como estas", "que tal", "como te va"],
    "hora": ["que hora es", "dime la hora", "puedes decirme la hora", "hora actual"],
    "nombre": ["me llamo", "mi nombre es"],
    "emociones_tristeza": ["estoy triste", "me siento mal", "me siento solo", "ando bajoneado"],
    "emociones_alegria": ["estoy feliz", "me siento bien", "estoy muy bien", "estoy contento"],
    "aburrimiento": ["estoy aburrido", "me aburro", "no se que hacer"],
    "pedir_datos": ["cuentame algo interesante", "dime algo interesante", "quiero un dato interesante", "dame un dato curioso"],
    "ciencia": ["cuentame algo de ciencia", "dame un dato de ciencia", "algo sobre el universo", "dato cientifico"],
    "historia": ["dime algo de historia", "cuentame un hecho historico", "dato historico"],
    "cultura": ["cuentame algo cultural", "algo de arte", "musica", "literatura"],
    "motivacional": ["necesito un consejo", "me siento perdido", "necesito motivacion"]
}

# Respuestas genéricas por categoría
GENERIC_RESPONSES = {
    "saludos": ["Hola Jota, ¿cómo estás hoy?", "¡Qué gusto saludarte, Jota!"],
    "despedidas": ["Hasta pronto, Jota.", "Cuídate mucho, Jota. ¡Nos vemos!"],
    "agradecimientos": ["¡Con gusto, Jota! Para eso estoy.", "No hay de qué, Jota."],
    "estado_animo": ["Estoy aquí para escucharte, Jota.", "Muy bien, ¿y tú cómo estás, Jota?"],
    "hora": ["Ahora mismo no tengo reloj, pero puedo ayudarte con otra cosa, Jota."],
    "nombre": ["Encantado, Jota. Ya me lo habías dicho, pero me gusta escucharlo."],
    "emociones_tristeza": ["Lamento que te sientas así, Jota. Estoy contigo.", "Estoy aquí para animarte, Jota."],
    "emociones_alegria": ["¡Me alegra mucho, Jota!", "Qué bueno escuchar eso, Jota."],
    "aburrimiento": [
        "¡Hagamos algo divertido, Jota! Puedo contarte chistes, enseñarte algo nuevo o hablar sobre cualquier tema.",
        "Podemos hablar de lo que quieras para entretenernos, Jota."
    ],
    "pedir_datos": ["Claro Jota, déjame pensar en algo curioso...", "¿Sabías que los pulpos tienen tres corazones?"],
    "ciencia": ["El universo sigue expandiéndose cada segundo, Jota.", "Los agujeros negros pueden deformar el tiempo, Jota."],
    "historia": ["¿Sabías que Napoleón fue coronado emperador por sí mismo?", "La Segunda Guerra Mundial terminó en 1945, Jota."],
    "cultura": ["¿Quieres hablar de arte, música o literatura?", "Puedo contarte sobre escritores, músicos o movimientos culturales."],
    "motivacional": [
        "Recuerda que cada día es una nueva oportunidad, Jota. ¡Tú puedes!",
        "A veces el camino se ve difícil, pero la perseverancia te lleva lejos, Jota."
    ]
}

# Coincidencia difusa con difflib
def encontrar_categoria_aproximada(entrada):
    entrada_norm = normalizar_texto(entrada)
    for categoria, frases in RESPONSES.items():
        frases_norm = [normalizar_texto(f) for f in frases]
        coincidencia = difflib.get_close_matches(entrada_norm, frases_norm, n=1, cutoff=0.6)
        if coincidencia:
            return categoria
    return None

# Función principal de respuesta
def obtener_respuesta(entrada):
    categoria = encontrar_categoria_aproximada(entrada)
    if categoria and categoria in GENERIC_RESPONSES:
        return GENERIC_RESPONSES[categoria]
    else:
        return ["Lo siento, no entendí lo que dijiste. ¿Podrías intentarlo de otra manera, Jota?"]
