import warnings
warnings.filterwarnings('ignore', message='.*Skipping variable loading for optimizer.*')

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas
import tensorflow
import traceback
import joblib

from typing import Dict, Any


def queryMachineLearning(transaction_data: Dict[str, Any]) -> float:
    COLUMNAS_NUMERICAS = ['transaction_value']
    COLUMNAS_BOOLEANAS = ['is_recurring', 'is_first_purchase']
    COLUMNAS_CATEGORICAS = ['product_category', 'collector_company', 'iban_anonymized']
    COLUMNA_FECHA = 'transaction_date'
    
    NOMBRE_ARCHIVO_MODELO = 'api/ai/machineLearning/machineLearning.weights.h5'
    NOMBRE_ARCHIVO_PREPROCESSOR = 'api/ai/machineLearning/preprocessor.joblib'
    
    try:
        if not os.path.exists(NOMBRE_ARCHIVO_MODELO):
            raise FileNotFoundError(f"No se encontró el modelo en {NOMBRE_ARCHIVO_MODELO}")
        
        if not os.path.exists(NOMBRE_ARCHIVO_PREPROCESSOR):
            raise FileNotFoundError(f"No se encontró el preprocesador en {NOMBRE_ARCHIVO_PREPROCESSOR}")
        
        # 1. Cargar el preprocesador
        preprocessor = joblib.load(NOMBRE_ARCHIVO_PREPROCESSOR)
        
        # 2. Convertir el diccionario a DataFrame (una sola fila)
        transaction_df = pandas.DataFrame([transaction_data])
        
        # 3. Verificar que tenemos todas las columnas necesarias
        columnas_requeridas = COLUMNAS_NUMERICAS + COLUMNAS_BOOLEANAS + COLUMNAS_CATEGORICAS + [COLUMNA_FECHA]
        for columna in columnas_requeridas:
            if columna not in transaction_df.columns:
                raise ValueError(f"Falta la columna requerida: {columna}")
        
        # 4. Preprocesar los datos
        X_processed = preprocessor.transform(transaction_df)
        X_processed = X_processed.astype(float)
        
        # 5. Cargar y construir el modelo (misma arquitectura que en entrenamiento)
        num_features = X_processed.shape[1]
        
        model = tensorflow.keras.models.Sequential([
            tensorflow.keras.layers.Input(shape=(num_features,)),
            tensorflow.keras.layers.Dense(8, activation='relu'),
            tensorflow.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=tensorflow.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # 6. Cargar los pesos entrenados
        model.load_weights(NOMBRE_ARCHIVO_MODELO)
        
        # 7. Realizar la predicción
        prediction = model.predict(X_processed, verbose=0)
        
        # 8. Devolver la probabilidad como float
        return float(prediction[0][0])
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Asegúrate de que el modelo ha sido entrenado primero ejecutando trainMachineLearning.py")
        return 0.5
        
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        traceback.print_exc()
        return 0.5