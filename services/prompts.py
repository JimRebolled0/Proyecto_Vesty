def user_info(input_usuario, datos_usuario):

    return f"""
    Perfil del usuario:
    
    Mujer de {datos_usuario['edad']} años, estatura {datos_usuario['estatura']} cm.
    
    Tipo de cuerpo: {input_usuario['morfologia']}.
    Relación hombros-caderas: caderas {input_usuario['caderas_vs_hombros']} respecto a hombros.
    Proporción piernas vs torso: {input_usuario['piernas_vs_torso']} respecto a longitud de torso.
  
    Abdomen: La volumen del abdomen es {input_usuario['abdomen']}.
    Cintura: {input_usuario['cintura']}.
    Glúteo: La proyección del gluteo es {input_usuario['gluteo']}.
    Pecho: {input_usuario['pecho']} en relación con el ancho de su torso.
    
    """

def upper_info(df_result):

    def top_features(col):
        vc = df_result[col].value_counts(normalize=True)
        principales = vc[vc > 0.2].index.tolist()
        return principales[:3]

    resumen = {
        'fit': top_features('fit'),
        'estructura': top_features('estructura'),
        'volumen': top_features('volumen'),
        'neckline_effects': top_features('neckline_effects')
    }

    prendas = df_result['texto_prenda'].sample(min(3, len(df_result))).tolist()
    
    prompt = f"""
    RECOMENDACIONES DETECTADAS:
    {resumen}

    EJEMPLOS DE PRENDAS:
    {prendas}

    """
    return prompt


def lower_info(df_result):

    def top_features(col):
        vc = df_result[col].value_counts(normalize=True)
        principales = vc[vc > 0.2].index.tolist()
        return principales[:3]


    resumen = {
        'fit': top_features('fit'),
        'estructura': top_features('estructura'),
        'volumen': top_features('volumen'),
        'tiro': top_features('tiro'),
        'longitud': top_features('longitud')
    }

    prendas = df_result['texto_prenda'].sample(min(3, len(df_result))).tolist()
    
    prompt = f"""
    RECOMENDACIONES DETECTADAS:
    {resumen}

    EJEMPLOS DE PRENDAS:
    {prendas}


    """
    return prompt


def asesor_imagen(user_text, upper_text, lower_text):

    return f"""
    Eres un asesor experto en imagen y estilismo femenino.

    Tu tarea es analizar el perfil del usuario y las recomendaciones de prendas, y devolver una explicación breve y estructurada.

    DEBES RESPONDER ÚNICAMENTE EN EL SIGUIENTE FORMATO:

    FORTALEZAS:
    Lista o resume las principales fortalezas del cuerpo del usuario.

    RECOMENDACIÓN SUPERIOR (UPPER):
    Explica por qué los cortes y características de las prendas superiores favorecen su figura.

    RECOMENDACIÓN INFERIOR (LOWER):
    Explica por qué los cortes y características de las prendas inferiores favorecen su figura.

    REGLAS:
    - Máximo 6-8 líneas en total.
    - Sé claro, directo y profesional.
    - No agregues introducciones ni conclusiones.
    - No salgas del formato.

    CONTEXTO DEL USUARIO:
    {user_text}

    ANÁLISIS PRENDAS SUPERIORES:
    {upper_text}

    ANÁLISIS PRENDAS INFERIORES:
    {lower_text}
    """

def feed_back(user_text, asesor_text):

    return f"""
    Eres un asesor de imagen experto.

    Tu tarea es explicar de forma breve, clara y amigable por qué las prendas recomendadas favorecen la silueta del usuario.

    CONTEXTO DEL USUARIO:
    {user_text}

    ANÁLISIS DE ESTILO:
    {asesor_text}

    INSTRUCCIONES:
    - Máximo 3-4 líneas.
    - Menciona las características de la prenda y explica el efecto visual que genera en la silueta del usuario (ej: estiliza, equilibra, alarga figura).
    - Usa lenguaje cercano pero profesional.
    - No uses formato estructurado ni listas técnicas.
    """


def generar_prompt_collage_outfits(ocasion):

    map_ocasion = {
        'Casual': 'casual outfit',
        'Formal': 'formal outfit',
        'Noche': 'night outfit',
        'Date': 'date outfit',
        'Invierno': 'winter outfit',
        'Semiformal': 'smart casual outfit'
    }

    ocasion_texto = map_ocasion.get(ocasion, ocasion)

    prompt = f"""
    Create a single fashion lookbook collage image with 5 different outfits.

    Target audience:
    Women aged 18 and 50.
    
    Image layout:
    - 5 outfits arranged in a clean grid (like a fashion catalog page)

    Style:
    - modern fashion illustration
    - minimalist editorial design
    - soft lighting
    - neutral background
    - clean and elegant fashion catalog aesthetic

    Content rules:
    - 5 distinct outfit looks
    - each outfit is a complete clothing set
    - focus only on clothing and styling
    - no people, no faces, no bodies
    - each outfit should be visually separated

    Occasion: {ocasion_texto}

    Final result should look like a professional fashion lookbook page for a clothing brand.
    """
    return prompt

def generar_outfits(ocasion, feed_back_text):

    map_ocasion = {
        'Casual': 'casual outfit',
        'Formal': 'formal outfit',
        'Noche': 'night outfit',
        'Date': 'date outfit',
        'Invierno': 'winter outfit',
        'Semiformal': 'smart casual outfit'
    }

    ocasion_texto = map_ocasion.get(ocasion, ocasion)

    estilo_base = """
    Modern fashion lookbook collage.
    Minimalist editorial fashion aesthetic.
    Soft lighting, neutral backgrounds.
    Clean, elegant clothing presentation.
    No people, no faces, no bodies.
    Only outfits displayed as styled garments.
    """

        # 🔹 aquí entra tu feedback como guía de estilo
    style_guidance = ""

    if feed_back_text:
        style_guidance = f"""
    Personalized styling direction (from user analysis):

    {feed_back_text}

    Interpret this as clothing styling guidance:
    focus on silhouettes, proportions and garment structure.
    """
    else:
        style_guidance = """
    Personalized styling direction:
    balanced, flattering and modern fashion silhouettes.
    """

    prompt = f"""
    Create a single fashion lookbook collage image with 5 different outfit looks.

    Target audience:
    Women aged 18 and 50.

    Image layout:
    - 5 outfits arranged in a clean grid (fashion catalog style)

    {estilo_base}

    {style_guidance}

    Occasion:
    {ocasion_texto}

    Content rules:
    - 5 distinct outfit looks
    - each outfit is a complete clothing set
    - visually separated outfits
    - no text inside image

    Final result must look like a professional fashion brand lookbook page.
    """

    return prompt