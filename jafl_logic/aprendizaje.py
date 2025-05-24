import fitz  # PyMuPDF
import os
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI

CHROMA_PATH = "jafl_logic/chroma_data"

def leer_texto_de_pdf(ruta_pdf):
    texto = ""
    with fitz.open(ruta_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def crear_documentos(texto):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_text(texto)
    return [Document(page_content=c) for c in chunks]

def crear_vectorstore(documentos):
    persist_directory = CHROMA_PATH
    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(
        documents=documentos,
        embedding=embedding,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def cargar_vectorstore():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=OpenAIEmbeddings()
    )

def buscar_en_pdf(pregunta):
    if not os.path.exists(CHROMA_PATH):
        return "No se ha indexado ningún documento aún. Decime qué archivo leer."

    vectordb = cargar_vectorstore()
    documentos_relacionados = vectordb.similarity_search(pregunta)

    if not documentos_relacionados:
        return "No encontré nada relevante en el documento."

    modelo = ChatOpenAI(temperature=0)
    cadena = load_qa_chain(modelo, chain_type="stuff")

    resultado = cadena.run(input_documents=documentos_relacionados, question=pregunta)
    return resultado

import os
# ... (el resto de tus imports y código)

# Nueva función para indexar todos los PDFs en la carpeta 'pdf' dentro de JAFL_ASSISTANT
def indexar_pdfs_en_carpeta(carpeta_pdf="pdf"):
    textos_completos = ""
    for archivo in os.listdir(carpeta_pdf):
        if archivo.lower().endswith(".pdf"):
            ruta_pdf = os.path.join(carpeta_pdf, archivo)
            print(f"Indexando {ruta_pdf}...")
            texto = leer_texto_de_pdf(ruta_pdf)
            textos_completos += texto + "\n"

    documentos = crear_documentos(textos_completos)
    crear_vectorstore(documentos)
    print("Indexación completada.")

# Puedes llamar a esta función manualmente para indexar:
# indexar_pdfs_en_carpeta()

def analizar_emocion(texto):
    texto_lower = texto.lower()

    # Diccionario de emociones con palabras clave y pesos
    emociones = {
        "feliz": {"feliz": 3, "contento": 2, "alegre": 3, "genial": 3, "emocionado": 2, "entusiasmado": 2},
        "triste": {"triste": 3, "deprimido": 4, "mal": 2, "llorando": 3, "melancólico": 3, "desanimado": 2},
        "enojado": {"enojado": 3, "molesto": 2, "furioso": 4, "irritado": 2, "frustrado": 2},
        "ansioso": {"ansioso": 3, "nervioso": 2, "preocupado": 3, "estresado": 3, "inquieto": 2},
        "miedo": {"asustado": 3, "temeroso": 3, "aterrorizado": 4, "inseguro": 2, "ansioso": 2},
        "sorprendido": {"sorprendido": 3, "asombrado": 3, "impresionado": 2},
        "calmado": {"calmado": 3, "relajado": 3, "tranquilo": 3, "sereno": 3}
    }

    # Frases emocionales comunes para aumentar score
    frases_emocionales = {
        "feliz": ["me siento genial", "estoy muy contento", "qué alegría", "me encanta", "me hace feliz"],
        "triste": ["me siento mal", "estoy deprimido", "no puedo más", "me duele", "me siento solo"],
        "enojado": ["estoy harto", "no soporto", "me enoja", "me molesta mucho"],
        "ansioso": ["me siento nervioso", "estoy preocupado", "no sé qué hacer", "me inquieta"],
        "miedo": ["tengo miedo", "me asusta", "estoy inseguro", "no me siento seguro"],
        "sorprendido": ["no lo esperaba", "qué sorpresa", "me sorprendió mucho"],
        "calmado": ["todo está bien", "me siento tranquilo", "estoy en paz"]
    }

    # Palabras negativas que anulan o bajan intensidad
    negaciones = ["no ", "nunca ", "jamás ", "sin "]

    # Puntajes por emoción
    puntajes = {emocion: 0 for emocion in emociones.keys()}

    # Función para chequear si una palabra está negada
    def esta_negada(texto, palabra):
        idx = texto.find(palabra)
        if idx == -1:
            return False
        for neg in negaciones:
            neg_idx = texto.rfind(neg, 0, idx)
            if neg_idx != -1 and (idx - neg_idx) <= 3:
                return True
        return False

    # Sumar puntajes por palabras clave con peso
    for emocion, palabras in emociones.items():
        for palabra, peso in palabras.items():
            if palabra in texto_lower and not esta_negada(texto_lower, palabra):
                puntajes[emocion] += peso

    # Sumar puntajes por frases comunes
    for emocion, frases in frases_emocionales.items():
        for frase in frases:
            if frase in texto_lower:
                puntajes[emocion] += 4


    # Buscar la emoción con mayor puntaje
    emocion_max = max(puntajes, key=puntajes.get)
    if puntajes[emocion_max] == 0:
        return "neutral"
    return emocion_max
