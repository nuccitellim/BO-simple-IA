import streamlit as st
from litellm import completion
import os

my_secret = os.environ['GROQ_API_KEY']

# asignamos la API KEY a la variable my_secret

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

# probar este si no funciona el siguiente
# st.text_area(label="Texto de la norma:",
# placeholder="Pegue el texto de la norma aquí.")

# Campo de entrada para la norma
norma = st.text_area("Pega la norma aquí:", height=300)

# print(norma)

# Crear un botón para enviar el mensaje
if st.button("Generar resumen"):
    # Si el botón es presionado, mostrar el texto ingresado en la sección de resultado
    st.write("### Resultado:")
    # Llamar a la función completion de litellm
    response = completion(
        model="groq/llama3-8b-8192",
        messages=[{
            "role": "user",
            "content": norma
        }],
    )

#st.write(response) print(response)

# Mostrar la respuesta generada por el modelo en un campo de texto
st.write(response.choices[0].message.content, height=200)
