import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

import json
from typing import List, Dict, Any
from largeLanguageModel.queryLargeLanguageModel import queryLargeLanguageModel
from machineLearning.queryMachineLearning import queryMachineLearning
from machineLearning.trainMachineLearning import transformar_fecha_a_timestamp_simple


def procesar_transacciones(archivo_json: str, archivo_historial: str) -> List[Dict[str, Any]]:
    with open(archivo_json, 'r', encoding='utf-8') as file:
        datos_analizar = json.load(file)

    with open(archivo_historial, 'r', encoding='utf-8') as file:
        historial_completo = json.load(file)
    
    resultados = []
    
    for transaccion in datos_analizar['transactions']:
        datos_comunes = {
            'transaction_value': transaccion['transaction_value'],
            'is_recurring': transaccion['is_recurring'],
            'is_first_purchase': transaccion['is_first_purchase'],
            'product_category': transaccion['product_category'],
            'collector_company': transaccion['collector_company'],
            'iban_anonymized': transaccion['iban_anonymized'],
            'transaction_date': transaccion['transaction_date'],
            'has_been_refunded': transaccion['has_been_refunded']
        }
        
        riesgo_llm = queryLargeLanguageModel(datos_comunes, historial_completo)
        riesgo_ml = queryMachineLearning(datos_comunes)
        umbral_probabilistico = (riesgo_llm * 0.5) + (riesgo_ml * 0.5)

        resultado = {
            'iban': datos_analizar['user_profile']['iban_number'],
            'codigo_transaccion': transaccion['transaction_code'],
            'importe': transaccion['transaction_value'],
            'umbral_probabilistico': umbral_probabilistico,
            'iban_empresa_colaboradora': transaccion['iban_anonymized']
        }

        resultados.append(resultado)
    
    return resultados

if __name__ == "__main__":
    archivo_analizar = "json files/testing/ult_2_dias_cliente1.json"
    archivo_historial = "json files/training/cliente1_total.json"
    
    try:
        resultados = procesar_transacciones(archivo_analizar, archivo_historial)
        print(resultados)
        
    except Exception as e:
        print(f"Error: {e}")