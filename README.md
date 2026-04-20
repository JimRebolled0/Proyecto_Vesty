# Vesty — Asesor de Imagen Inteligente
Vesty es una aplicación que recomienda outfits personalizados para mujeres, combinando **machine learning** y **IA generativa** para adaptar las prendas a la silueta del usuario y a la ocasión, identificando características de las prendas y usuario, para crear una armonización visual. Explica por qué ciertas prendas favorecen al usuario, además, genera imágenes tipo lookbook con IA para visualizar los outfits.


## Estructura del proyecto

```
Vesty/
├── main1.py                # App principal en Streamlit
├── requirements.txt
├── datos/                 # Datos de prendas
├── models/                # Modelos entrenados (.pkl)
├── model/
│   └── predictor.py       # Lógica de predicción
├── services/
│   └── prompts.py         # Construcción de prompts
├── images/                # Recursos visuales
└── .streamlit/
    └── config.toml
```

---

## Variables de entorno

La app requiere una API key:

```
OPENAI_API_KEY=tu_api_key
```

En producción (Streamlit Cloud), se configura desde **Secrets**.

---

## Elaborado por:

Karla Jimena Herández Rebolledo

