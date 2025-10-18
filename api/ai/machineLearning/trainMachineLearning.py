import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import joblib
import json
import pandas
import sys
import tensorflow
import traceback

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer


def transformar_fecha_a_timestamp_simple(X):
    if isinstance(X, pandas.DataFrame):
        date_series = X.iloc[:, 0]
    else:
        date_series = pandas.Series(X)
    
    dates = pandas.to_datetime(date_series, format='%Y-%m-%d', errors='coerce')
    
    timestamps = dates.apply(lambda x: int(x.timestamp()) if not pandas.isna(x) else 0)
    
    return timestamps.values.reshape(-1, 1)

if __name__ == "__main__":
    # --- 1. Definición de Constantes ---
    COLUMNAS_NUMERICAS = ['transaction_value']
    COLUMNAS_BOOLEANAS = ['is_recurring', 'is_first_purchase']
    COLUMNAS_CATEGORICAS = ['product_category', 'collector_company', 'iban_anonymized']
    COLUMNA_FECHA = 'transaction_date'

    NOMBRE_ARCHIVO_MODELO = 'machineLearning/machineLearning.weights.h5'

    # --- 2. Verificación de Argumentos ---
    ruta_json = sys.argv[1]
    columna_objetivo = sys.argv[2]

    # --- 3. Cargar y CONVERTIR Datos ---
    try:
        with open(ruta_json, 'r', encoding = 'utf-8') as file:
            data_dict = json.load(file)

        if 'transactions' not in data_dict:
            print("Error: El JSON no tiene la clave 'transactions' en la raíz.")
            sys.exit(1)
        lista_plana_transacciones = data_dict['transactions']

        columnas_minimas = COLUMNAS_NUMERICAS + COLUMNAS_BOOLEANAS + COLUMNAS_CATEGORICAS + [COLUMNA_FECHA, columna_objetivo]
        registros_validos = [transaccion for transaccion in lista_plana_transacciones
                             if all(columna in transaccion for columna in columnas_minimas)]

        num_original = len(lista_plana_transacciones)
        num_validos = len(registros_validos)

        if num_validos == 0:
             print("Error: No se encontraron registros válidos con todas las columnas necesarias en el JSON.")
             sys.exit(1)
    
        datos = pandas.DataFrame.from_records(registros_validos)

        if len(datos) == 0:
            print("Error: El DataFrame resultante está vacío.")
            sys.exit(1)

    except FileNotFoundError:
        print(f"Error: No encontré tu JSON en '{ruta_json}'.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Tu JSON está corrupto.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al leer y convertir el JSON: {e}")
        sys.exit(1)

    # --- 4. Preparación y Preprocesamiento Avanzado ---
    if columna_objetivo not in datos.columns:
        print(f"Error: La columna objetivo '{columna_objetivo}' no se encontró.")
        sys.exit(1)

    try:
        y = datos[columna_objetivo].astype(int)
        X = datos.drop(columns = [columna_objetivo, 'transaction_code'], errors = 'ignore')
    except Exception as e:
        print(f"Error al separar X e y: {e}")
        sys.exit(1)

    preprocessor = ColumnTransformer(
        transformers=[
            ('date', FunctionTransformer(
                transformar_fecha_a_timestamp_simple, 
                validate=False,
                feature_names_out='one-to-one'
            ), [COLUMNA_FECHA]),
            ('num', StandardScaler(), COLUMNAS_NUMERICAS),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), COLUMNAS_CATEGORICAS),
            ('bool', 'passthrough', COLUMNAS_BOOLEANAS)
        ],
        remainder='drop'
    )

    try:
        X_processed = preprocessor.fit_transform(X)

        X_train = X_processed.astype(float)
        y_train = y.values

        feature_names_out = preprocessor.get_feature_names_out()
    except Exception as e:
        print(f"Fallé durante el preprocesamiento: {e}")
        traceback.print_exc()
        sys.exit(1)

    if X_train.size == 0:
         print("Error fatal: No hay características (features) después del preprocesamiento.")
         sys.exit(1)
    if X_train.shape[0] != y_train.shape[0]:
         print(f"Error fatal: Desajuste en número de muestras -> X:{X_train.shape[0]}, y:{y_train.shape[0]}")
         sys.exit(1)

    # --- 5. Definir la Arquitectura del Modelo ---
    tasa_aprendizaje = 0.001
    epocas = 100
    num_features = X_train.shape[1]

    model = tensorflow.keras.models.Sequential([
        tensorflow.keras.layers.Input(shape = (num_features,)),
        tensorflow.keras.layers.Dense(8, activation = 'relu'),
        tensorflow.keras.layers.Dense(1, activation = 'sigmoid')
    ])

    model.compile(
        optimizer = tensorflow.keras.optimizers.Adam(learning_rate = tasa_aprendizaje),
        loss = 'binary_crossentropy',
        metrics = ['accuracy']
    )

    # --- 6. Cargar 'Conocimiento' Previo ---
    modelo_dir = os.path.dirname(NOMBRE_ARCHIVO_MODELO)
    if modelo_dir and not os.path.exists(modelo_dir):
        os.makedirs(modelo_dir, exist_ok=True)

    if os.path.exists(NOMBRE_ARCHIVO_MODELO):
        try:
            model.load_weights(NOMBRE_ARCHIVO_MODELO)
        except Exception as e:
            print(f"Fallé al cargar los pesos de Keras. ¿Quizás la arquitectura cambió drásticamente?")
            print(f"Error: {e}. Empezando de cero.")

    # --- 7. Lógica de Entrenamiento ---
    early_stopping = tensorflow.keras.callbacks.EarlyStopping(
        monitor = 'loss',
        patience = 10,
        restore_best_weights = True
    )

    history = model.fit(
        X_train,
        y_train,
        epochs = epocas,
        callbacks = [early_stopping],
        validation_split = 0.2,
        verbose = 0
    )

    # --- 8. Guardar la 'Inteligencia' Mejorada ---
    try:
        model.save_weights(NOMBRE_ARCHIVO_MODELO)
    except Exception as e:
        print(f"Error al guardar el modelo: {e}")
        if modelo_dir and not os.path.exists(modelo_dir):
             print(f"El directorio '{modelo_dir}' no existe.")
        sys.exit(1)

    # --- 9. Guardar el Preprocesador --- NUEVO PASO
    NOMBRE_ARCHIVO_PREPROCESSOR = 'machineLearning/preprocessor.joblib' # O .pkl si prefieres pickle
    # Asegurarse de que el directorio existe (por si acaso)
    modelo_dir = os.path.dirname(NOMBRE_ARCHIVO_PREPROCESSOR)
    if modelo_dir and not os.path.exists(modelo_dir):
        os.makedirs(modelo_dir, exist_ok=True)

    try:
        joblib.dump(preprocessor, NOMBRE_ARCHIVO_PREPROCESSOR)
    except Exception as e:
        print(f"Error al guardar el preprocesador: {e}")