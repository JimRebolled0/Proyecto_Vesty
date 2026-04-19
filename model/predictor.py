import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
def out_model(model, col_model, df_prendas_model, df_prendas_raw, input_usuario,prenda):

    def transformar_usuario(input_usuario, model_columns):
        '''
        input_usuario: Se aloja en una diccionario, se obtiene de lo que responde en el cuestionario
        model_columns: Columnas que fueron features en el modelo
        '''
        
        df_usuario = pd.DataFrame([input_usuario])
        
        # Aplicar dummies, como se hizo en la ingeniería de variables
        df_usuario = pd.get_dummies(df_usuario, dtype=int)
        
        # Garantizar que solo corresponda a features del usuario
        user_columns = [
            col for col in model_columns 
            if col.startswith((
                'morfologia_','abdomen_','piernas_vs_torso_',
                'caderas_vs_hombros_','cintura_','gluteo_','pecho_'
            ))
        ]
        
        df_usuario = df_usuario.reindex(user_columns, fill_value=0)
        
        return df_usuario
    df_usuario = transformar_usuario(input_usuario, col_model)

    df_input = df_usuario.merge(df_prendas_model, how='cross')
    df_input_m = df_input.reindex(columns=['article_id'] + list(col_model), fill_value=0)

    df_input_model = df_input_m[list(col_model)]
    df_input['pred'] = model.predict(df_input_model)

    df_fav = df_input[df_input['pred'] == 1].copy()

    df_result = df_fav.merge(df_prendas_raw, on='article_id')

    df_result_u = df_result[prenda].copy()

    return df_result_u