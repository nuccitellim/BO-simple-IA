from logging import PlaceHolder
import streamlit as st
import os
import requests
import json

my_secret = os.environ['DIFY_API_KEY']


def decodificar_json(response):
    """ Recibe objeto json y retorna campo respuesta"""
    response_str = response.content.decode('utf-8')
    response_dict = json.loads(response_str)
    answer = response_dict['answer']
    return answer


# Configuración de la página
st.set_page_config(page_title="Boletín Oficial Simple",
                   page_icon="📃",
                   layout="wide")

# CSS para personalizar estilos
st.markdown("""
    <style>
    .centered-title {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .centered-subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5em;
        font-weight: normal;
        margin-bottom: 50px;
    }
    .custom-label {
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .right-column {
        margin-left: 50px; 
    }
    .footer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 50px;
        font-size: 1.2em;
    }
    </style>
    """,
            unsafe_allow_html=True)

# Inicializar variables en el estado de la sesión
if 'assistant_response' not in st.session_state:
    st.session_state.assistant_response = ""

if 'norm_text_area' not in st.session_state:
    st.session_state.norm_text_area = ""

# Título y subtítulo
st.markdown('<div class="centered-title"> 📃 Boletín Oficial Simple 📃</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="centered-subtitle"> Inteligencia Artificial Generativa para simplificar las normas</div>',
    unsafe_allow_html=True)

# Dividir en columnas
col1, col2 = st.columns([5, 5])

with col1:
    st.markdown(
        '<div class="custom-label">Pega el texto de la norma que desees simplificar: </div>',
        unsafe_allow_html=True)

    # Vincular el área de texto con el estado de la sesión
    st.session_state.norm_text_area = st.text_area(
        label="",
        value=st.session_state.norm_text_area,
        placeholder="Pega el texto de la norma aquí.",
        height=300,
    )

    # Configurar los datos de la solicitud
    base_url = "https://api.dify.ai/v1"
    path = "/completion-messages"
    full_path = base_url + path
    headers = {
        "Authorization": f"Bearer {my_secret}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {
            "topic": st.session_state.norm_text_area
        },
        "response_mode": "blocking",
        "user": "m-nuccitelli@hotmail.com"
    }

    # Botón para generar el resumen
    gresumen = st.button("Generar resumen")
    if gresumen:
        if st.session_state.norm_text_area:
            with st.spinner("Procesando la norma..."):
                response = requests.post(full_path, json=data, headers=headers)
                if response.status_code == 200:
                    answer = decodificar_json(response)
                    st.session_state.assistant_response = answer
                else:
                    st.error(
                        "Hubo un error al generar la respuesta. Intenta nuevamente."
                    )

        # Definir la función para limpiar la búsqueda
        def limpiar_busqueda():
            st.session_state.norm_text_area = ""  # Limpiar el área de texto
            st.session_state.assistant_response = ""  # Limpiar la respuesta del asistente

        # Botón para limpiar búsqueda con callback
        st.button("Limpiar búsqueda", on_click=limpiar_busqueda)

with col2:
    # Mostrar instrucciones o respuesta
    if not st.session_state.assistant_response:
        st.markdown('''
        <div class="right-column">
            <h3>Instrucciones</h3>
            <p>🤖 Este es tu nuevo Asistente con Inteligencia Artificial Generativa, pensado para hacerte la vida más fácil.

📜 Se encarga de simplificar las normas publicadas todos los días en el Boletín Oficial de tu jurisdicción. Podés resumir:
- 🏛️ Leyes  
- 📄 Decretos  
- 🖋️ Resoluciones  
- 📑 Disposiciones  
- ⚖️ Cualquier otro acto administrativo  

Solo escribí el texto que querés simplificar, hacé clic en "Generar resumen" ¡y listo!✨</p>
        </div>
        ''',
                    unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="right-column">
            <h4>Respuesta:</h4>
            <p>{}</p>
        </div>
        '''.format(st.session_state.assistant_response),
                    unsafe_allow_html=True)

# Pie de página
st.markdown(
    '<div class="footer"><p>BO Simple puede cometer errores. Considera verificar la información importante.</p></div>',
    unsafe_allow_html=True)
st.markdown(
    '<div class="footer"><a href="https://forms.gle/mYQFmMyQA7fMMYtF9" target="_blank">Hacé click acá para dejar comentarios, sugerencias o reportes sobre el asistente.</a></div>',
    unsafe_allow_html=True)
