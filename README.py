import requests
from gtts import gTTS
from IPython.display import Audio, display
import io

API_KEY = "sk-22f9df29562b47a1aadb5303be7e34e0"
API_URL = "https://api.deepseek.com/v1/chat/completions"

PROMPT_SISTEMA = (
   "eres onbit, un profesor o tutor altamente especializado y experto en ciberseguridad y copias de seguridad. "
   "tienes que brindar una respuesta extremadamente clara, detallada, técnica y con un breve ejemplo práctico. "
   "si te preguntan de algo que no esté relacionado, tienes que explicar amablemente que únicamente estás ultra especializado en ciberseguridad y copias de seguridad."
)

def speak_text(text, lang='es'):
    """
    Convierte texto a voz usando gTTS y lo reproduce en el notebook.
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        display(Audio(fp.read(), autoplay=True))
    except Exception as e:
        print(f"Error al reproducir el audio: {e}")

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
   welcome_message = "Bienvenido al chatbot de DeepSeek. Escribe 'salir' para terminar."
   print(welcome_message)
   speak_text(welcome_message)

   test_response = enviar_mensaje("hola")
   if "Error" in test_response:
       error_msg = f"⚠️ {test_response}\nPor favor, verifica tu API Key en https://platform.deepseek.com/"
       print(error_msg)
       speak_text("Ha ocurrido un error. Por favor, verifica tu clave API.")
       return

   while True:
       mensaje_usuario = input("Tú: ")

       if mensaje_usuario.lower() == "salir":
           exit_message = "Chatbot: ¡Hasta Luego!"
           print(exit_message)
           speak_text(exit_message)
           break

       respuesta = enviar_mensaje(mensaje_usuario)
       print(f"Chatbot: {respuesta}\n")
       speak_text(respuesta)

if __name__ == "__main__":
   main()
