import random
from datetime import datetime, timedelta

# Memoria temporal para evitar repetir la misma respuesta
ultima_emocion = None
ultima_respuesta = None
tiempo_ultima_respuesta = None

# Respuestas emocionales variadas
respuestas_emocionales = {
    "vacío": [
        "A veces sentirnos vacíos es una señal de que necesitamos reconectar con nosotros mismos. ¿Querés que exploremos eso juntos?",
        "El vacío puede doler, pero también es un espacio para construir algo nuevo. ¿Qué sentís que te falta?",
        "No estás solo, Jota. Hay algo en vos que aún no se ha apagado, incluso cuando sentís que sí.",
    ],
    "soledad": [
        "Sentirse solo no siempre significa estar solo. Estoy acá, ¿querés que hablemos un poco más?",
        "La soledad puede ser profunda, pero no es eterna. Hablemos de lo que estás sintiendo.",
        "Jota, a veces hablarlo es suficiente para aliviar un poco. Contame cómo fue tu día.",
    ],
    "ansiedad": [
        "La ansiedad te habla de tus miedos. Pero también podés aprender a calmarla poco a poco. Respiremos juntos.",
        "Si te sentís ansioso, tal vez necesites frenar y escucharte. Estoy acá para ayudarte a hacerlo.",
        "Tu mente está agitada, Jota. Pero podemos calmarla. ¿Querés que te guíe con un ejercicio de respiración?",
    ],
    "depresión": [
        "No estás roto, Jota. Estás pasando por algo. Podemos atravesarlo juntos.",
        "La tristeza profunda no es debilidad. Es parte de ser humano. Estoy acá.",
        "Aunque todo parezca gris, hay cosas que valen la pena. Vamos de a poco. Te acompaño.",
    ],
    "enojo": [
        "El enojo también es una forma de dolor. ¿Querés hablar de qué te hizo sentir así?",
        "Tu enojo tiene una razón. No lo ignores. Decime qué pasó.",
        "A veces el enojo nos tapa el verdadero problema. ¿Podemos profundizar un poco?",
    ]
}

# Palabras clave asociadas a estados mentales
emociones_clave = {
    "vacío": ["vacío", "sin sentido", "nada", "apatía"],
    "soledad": ["solo", "sola", "abandonado", "sin nadie"],
    "ansiedad": ["ansioso", "nervioso", "estresado", "preocupado"],
    "depresión": ["triste", "deprimido", "sin ganas", "sin fuerzas", "no quiero vivir"],
    "enojo": ["enojado", "molesto", "furioso", "la puta", "harto"]
}


def diagnosticar_estado_mental(texto):
    global ultima_emocion, ultima_respuesta, tiempo_ultima_respuesta

    texto = texto.lower()
    ahora = datetime.now()

    # Si la última respuesta fue hace menos de 30 segundos y era sobre la misma emoción, no repite
    if tiempo_ultima_respuesta and (ahora - tiempo_ultima_respuesta < timedelta(seconds=30)):
        return None

    for emocion, palabras in emociones_clave.items():
        if any(p in texto for p in palabras):
            if ultima_emocion == emocion:
                # Elegir una nueva respuesta distinta si es la misma emoción
                posibles = [r for r in respuestas_emocionales[emocion] if r != ultima_respuesta]
                if not posibles:
                    posibles = respuestas_emocionales[emocion]
                respuesta = random.choice(posibles)
            else:
                respuesta = random.choice(respuestas_emocionales[emocion])

            # Guardar estado para evitar repetir en el corto plazo
            ultima_emocion = emocion
            ultima_respuesta = respuesta
            tiempo_ultima_respuesta = ahora

            return respuesta

    return None

