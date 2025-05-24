import requests
from bs4 import BeautifulSoup

def buscar_en_internet(pregunta):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = f"https://www.google.com/search?q={pregunta.replace(' ', '+')}"
        respuesta = requests.get(url, headers=headers)

        # Parsear la respuesta con BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')

        # Intentar obtener el primer resultado relevante de búsqueda
        resultado = soup.find('h3')
        if resultado:
            return resultado.text  # Retorna el texto del primer título encontrado
        return "No pude encontrar un resultado relevante."

    except Exception as e:
        return f"Hubo un problema: {e}"

# Ejemplo de uso
# Puedes usar este código para llamar la función desde donde la necesites.
# resultado = buscar_en_internet("¿Cuál es la capital de Francia?")
# print(resultado)
