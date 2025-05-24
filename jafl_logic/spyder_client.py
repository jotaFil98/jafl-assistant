import requests

BASE_URL = "http://127.0.0.1:5000"

def buscar_wikipedia(query):
    try:
        response = requests.get(f"{BASE_URL}/wikipedia", params={"query": query})
        response.raise_for_status()
        data = response.json()
        return data.get("result", "No se encontró resultado.")
    except requests.RequestException as e:
        return f"Error al conectar con Spyder: {e}"
    except ValueError:
        return "Error al procesar la respuesta de Spyder."
