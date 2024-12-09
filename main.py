import streamlit as st
import os
import requests
import json

def decodificar_json(objeto):
    """ Recibe objeto json y retorna campo respuesta"""
    response_str = response.content.decode('utf-8')
    response_dict = json.loads(response_str)
    answer = response_dict['answer']
    return answer


my_secret = os.environ['DIFY_API_KEY']

# Título
st.title("Boletín Oficial Simple")
st.subheader("Inteligencia Artificial Generativa para simplificar las normas")
# Descripción
st.write(
    "Este es un Asistente que utiliza Inteligencia Artificial Generativa para simplificar las normas publicadas a diario en el Boletín Oficial de tu jurisdicción."
)
# Detalles sobre el funcionamiento
st.write("""
### Puedes simplificar:
- Leyes
- Decretos
- Resoluciones
- Disposiciones
- Otros actos administrativos
      
""")

st.write("---")

st.write(
    "Por favor, copia el texto de la norma que deseas simplificar y luego pega el contenido aquí."
)

# Campo de entrada para la norma
norma = st.text_area("Pega la norma aquí:", height=300)

# Crear un botón para enviar el mensaje
if st.button("Generar resumen"):
    # Si el botón es presionado, mostrar el texto ingresado en la sección de resultado
    st.write("### Resultado:")
    base_url = "https://api.dify.ai/v1"
    path = "/completion-messages"
    full_path = base_url + path
    headers = {
        "Authorization": f"Bearer {my_secret}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {
            "topic": f"Bearer {norma}"
        },
        "response_mode": "blocking",
        "user": "m-nuccitelli@hotmail.com"
    }

    response = requests.post(full_path, json=data, headers=headers)

    # Mostrar la respuesta generada por el modelo en un campo de texto
    answer = decodificar_json(response)
    st.write(answer, height=200)
