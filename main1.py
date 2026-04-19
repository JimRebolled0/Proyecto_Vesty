import streamlit as st
import joblib
from dotenv import load_dotenv
import os
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
import joblib
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from model.predictor import out_model
from services.prompts import user_info, upper_info, lower_info, asesor_imagen, feed_back, generar_prompt_collage_outfits, generar_outfits

#Cargar cuando se ejecute en local
#load_dotenv()

# Prioridad: Streamlit Secrets → fallback a .env
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=api_key)

st.image("images/Vesty_logo.png", width=150)
st.title("Vesty")
st.caption("Tu silueta, tu regla")
st.markdown(
    """
    Este cuestionario nos ayudará a encontrar las piezas que celebren tu estructura natural.
    """
)

st.markdown("### Descubre que prendas hacen resaltar tu figura")
# -----------INPUTS BÀSICOS------------
if "edad" not in st.session_state:
    st.session_state.edad = None

if "estatura" not in st.session_state:
    st.session_state.estatura = None

if "ocasion" not in st.session_state:
    st.session_state.ocasion = None

edad = st.number_input(
    "Edad",
    min_value=10,
    max_value=90,
    step=1,
    key="edad"
)

estatura = st.number_input(
    "Estatura (cm)",
    min_value=100,
    max_value=220,
    step=1,
    key="estatura"
)
ocasion = st.selectbox(
    "Selecciona la ocasión",
    ["Selecciona una opción"] + ['Casual', 'Formal', 'Noche', 'Date', 'Invierno', 'Semiformal'],
    index=0,
    key="ocasion"
)

#------------CUESTIONARIO-----------

#------------MORFOLGIA-----------

st.markdown("### ¿Con cuál de estas formas de cuerpo te identificas más visualmente?")

opciones = ["ectomorfo", "mesomorfo", "endomorfo"]

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/morfologia_ectomorfo.png", use_container_width=True)
with col2:
    st.image("images/morfologia_mesomorfo.png", use_container_width=True)
with col3:
    st.image("images/morfologia_endomorfo.png", use_container_width=True)

seleccion_morfologia = st.radio(
    "",
    opciones,
    horizontal=True,
    key="morfologia"
)

#------------PIERNAS-----------

st.markdown("### ¿Cómo percibes la proporción de tus piernas en ralación a longitud de tu torso?")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/piernas_vs_torso.png", use_container_width=True)

seleccion_piernas = st.radio(
    "",
    ["largas", "proporcionales", "cortas"],
    horizontal=True,
    key="piernas_vs_torso"
)

#------------CADERAS-----------

st.markdown("### ¿Cómo percibes la proporción de tus caderas en relación a tus hombros?")


col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("images/caderas_vs_hombros.png", use_container_width=True)
seleccion_caderas = st.radio(
    "",
    ["estrechas", "proporcionales", "grandes"],
    horizontal=True,
    key="caderas_vs_hombros"
)

#------------ABDOMEN-----------

st.markdown("### De perfil, ¿cómo percibes la curvatura de tu abdomen?")

opciones_abdomen = ["plano", "medio", "abultado"]

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/abdomen_plano.png", use_container_width=True)
with col2:
    st.image("images/abdomen_medio.png", use_container_width=True)
with col3:
    st.image("images/abdomen_abultado.png", use_container_width=True)

seleccion_abdomen = st.radio(
    "",
    opciones_abdomen,
    horizontal=True,
    key="abdomen"
)

#------------CINTURA-----------

st.markdown("### Si trazaras una línea siguiendo el contorno de tu talle, ¿cuál describe mejor tu silueta?")

opciones_cintura = ["marcada","recta", "semi marcada"]

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/cintura_marcada.png", use_container_width=True)
with col2:
    st.image("images/cintura_semi_marcada.png", use_container_width=True)
with col3:
    st.image("images/cintura_recta.png", use_container_width=True)

seleccion_cintura = st.radio(
    "",
    opciones_cintura,
    horizontal=True,
    key="cintura"
)

#------------GLUTEO-----------

st.markdown("### Observando tu figura de perfil, ¿cómo percibes la proyección de tu zona posterior?")

opciones_gluteo = ["lineal", "estandar", "predominante"]

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/gluteo_lineal.png", use_container_width=True)
with col2:
    st.image("images/gluteo_estandar.png", use_container_width=True)
with col3:
    st.image("images/gluteo_predominante.png", use_container_width=True)

seleccion_gluteo = st.radio(
    "",
    opciones_gluteo,
    horizontal=True,
    key="gluteo"
)

#------------PECHO-----------

st.markdown("### En relación con el ancho de tu torso, ¿cómo percibes el volumen de tu busto?")

opciones_pecho = ["pequeño", "proporcional", "grande"]

col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/pecho_pequeño.png", use_container_width=True)
with col2:
    st.image("images/pecho_proporcional.png", use_container_width=True)
with col3:
    st.image("images/pecho_grande.png", use_container_width=True)

seleccion_pecho = st.radio(
    "",
    opciones_pecho,
    horizontal=True,
    key="pecho"
)

input_usuario = {
    "morfologia": seleccion_morfologia,
    "piernas_vs_torso": seleccion_piernas,
    "caderas_vs_hombros": seleccion_caderas,
    "abdomen": seleccion_abdomen,
    "cintura": seleccion_cintura,
    "gluteo": seleccion_gluteo,
    "pecho": seleccion_pecho
}

datos_usuario = {
    "edad": edad,
    "estatura": estatura,
}
# PAUSA NECESARIA. Para que usuario responda el cuestionario
# Boton final y validación--------------
#estado inicial


if "generado" not in st.session_state:
    st.session_state.generado = False

    # botón
if st.button("Generar recomendaciones"):

    if not edad or not estatura:
        st.warning("Completa edad y estatura")
        st.stop()

    if len(input_usuario) < 7:
        st.warning("Completa todo el cuestionario")
        st.stop()
    if ocasion == "Selecciona una opción":
        st.warning("Selecciona una ocasión válida")
        st.stop()

    st.session_state.generado = True


# SOLO SE EJECUTA SI YA SE PRESIONÓ EL BOTÓN
if st.session_state.generado:


    placeholder = st.empty()


    with st.spinner("Generando recomendaciones..."):

        # 🔹 1. Dato curioso (1 sola vez)
        fact = client.responses.create(
            model="gpt-4.1-mini",
            input="Dame un dato corto (1-2 líneas) interesante sobre moda"
        )

        dato_curioso = fact.output[0].content[0].text

        # 🔹 2. Mostrarlo
        placeholder.info(f"💡 {dato_curioso}")

        time.sleep(3)

        # 🔹 2. Mensaje emocional (impacto del vestir)
        fact2 = client.responses.create(
            model="gpt-4.1-mini",
            input="""
            Dame un mensaje corto (1-2 líneas) sobre por qué la forma en que te vistes impacta:
            - la seguridad personal
            - la percepción de los demás
            - la confianza corporal

            Tono: inspirador, elegante, no cliché.
            """
        )

        mensaje_estilo = fact2.output[0].content[0].text

        placeholder.info(f"✨ {mensaje_estilo}")


    # --------- CARGAR MODELOS----------


    with open("models/model_rf_upper.pkl", "rb") as f:
        model_upper = joblib.load(f)

    with open("models/model_rf_lower.pkl", "rb") as f:
        model_lower = joblib.load(f)

    # -------- CARGAR FEATURES ---------
    with open("models/model_rf_upper_col.pkl", "rb") as f:
        col_upper =joblib.load(f)

    with open("models/model_rf_lower_col.pkl", "rb") as f:
        col_lower = joblib.load(f)


    BASE_DIR = os.path.dirname(__file__)

    df_upper_model = pd.read_csv(os.path.join(BASE_DIR, "datos", "df_upper_model.csv"))
    df_upper_raw   = pd.read_csv(os.path.join(BASE_DIR, "datos", "df_upper_raw.csv"))

    df_lower_model = pd.read_csv(os.path.join(BASE_DIR, "datos", "df_lower_model.csv"))
    df_lower_raw   = pd.read_csv(os.path.join(BASE_DIR, "datos", "df_lower_raw.csv"))


    lower = ['article_id','detail_desc','texto_prenda','fit','estructura','material','volumen','tiro','longitud']
    upper =['article_id','detail_desc','texto_prenda','fit','estructura','volumen','sleeve','neckline','material','neckline_effects']
    df_upper_result = out_model(model_upper, col_upper, df_upper_model, df_upper_raw, input_usuario,upper)
    df_lower_result = out_model(model_lower, col_lower, df_lower_model, df_lower_raw, input_usuario,lower)


    #---------Prompt intermedios--------------
    user_text = user_info(input_usuario, datos_usuario)
    upper_text = upper_info(df_upper_result)
    lower_text = lower_info(df_lower_result)

    prompt_explicacion = asesor_imagen(user_text, upper_text, lower_text)


    feedback = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt_explicacion
    )

    feed_back_text = feedback.output[0].content[0].text

    st.markdown("## ✨ Tu análisis de estilo Vesty")
    st.info(feed_back_text)

  

    def generar_collage_imagen(client, ocasion):

        prompt = generar_outfits(ocasion,feed_back_text)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        image_url = response.data[0].url
        return image_url

    st.markdown(f"## 👗 Inspiración de outfits para ocasión {ocasion}")

    if st.button("Generar collage de outfits"):

        with st.spinner("Creando tu lookbook Vesty..."):

            collage_url = generar_collage_imagen(client, ocasion)

            st.image(collage_url, use_container_width=True)

            st.success("Lookbook generado con éxito ✨")

    
#streamlit run main1.py