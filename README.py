codigo
import requests

API_KEY = "sk-6549f06fb6b941cea7442e5451561a58"
API_URL = "https://api.deepseek.com/v1/chat/completions"

PROMPT_SISTEMA = (
    "eres onbit, un profesor o tutor especializado en cyberseguridad y copias de seguridad. "
    "tienes que brindar respuesta clara y con un breve ejemplo. "
    "si te preguntan de algo que no esté relacionado tienes que explicar amablemente que únicamente estás especializado en cyberseguridad y copias de seguridad."
)

def enviar_mensaje(mensaje, modelo="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensaje}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code != 200:
            try:
                error_detail = response.json()
            except ValueError:
                error_detail = response.text or "Sin detalles"
            return f"Error {response.status_code}: {error_detail}"

        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"
    except Exception as e:
        return f"Error Inesperado: {e}"

def main():
    print("Bienvenido al chatbot de DeepSeek. Escribe 'salir' para terminar.")

    test_response = enviar_mensaje("hola")
    if "Error" in test_response:
        print(f"⚠️ {test_response}")
        print("Por favor, verifica tu API Key en https://platform.deepseek.com/")
        return

    while True:
        mensaje_usuario = input("Tú: ")

        if mensaje_usuario.lower() == "salir":
            print("Chatbot: ¡Hasta Luego!")
            break

        respuesta = enviar_mensaje(mensaje_usuario)
        print(f"Chatbot: {respuesta}\n")

if __name__ == "__main__":
    main()
