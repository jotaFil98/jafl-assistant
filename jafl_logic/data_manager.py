import pandas as pd
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'jafl_data.csv')

def init_data_file():
    # Crear archivo si no existe con las columnas predefinidas
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["entrada", "respuesta", "emocion", "contexto"])
        df.to_csv(DATA_FILE, index=False)

def guardar_interaccion(entrada, respuesta, emocion=None, contexto=None):
    entrada = entrada.strip().lower()
    respuesta = respuesta.strip()
    if not entrada or not respuesta:
        return  # No guardar si está vacío
    
    init_data_file()
    
    df = pd.read_csv(DATA_FILE)
    
    # Evitar duplicados exactos
    if ((df['entrada'].str.lower() == entrada) & (df['respuesta'] == respuesta)).any():
        return
    
    nueva_fila = {
        "entrada": entrada,
        "respuesta": respuesta,
        "emocion": emocion if emocion else "",
        "contexto": contexto if contexto else ""
    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def buscar_respuesta_por_entrada(entrada):
    entrada = entrada.strip().lower()
    init_data_file()
    try:
        df = pd.read_csv(DATA_FILE)
        resultados = df[df["entrada"].str.contains(entrada, case=False, na=False)]
        if not resultados.empty:
            # Retornamos la primera respuesta encontrada
            return resultados.iloc[0]["respuesta"]
    except pd.errors.EmptyDataError:
        print("El archivo de datos está vacío.")
    except Exception as e:
        print(f"Error al buscar la entrada: {e}")
    
    return None

def obtener_todo():
    init_data_file()
    try:
        return pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
        print("El archivo de datos está vacío.")
    except Exception as e:
        print(f"Error al obtener todo el contenido: {e}")
    
    return pd.DataFrame()
