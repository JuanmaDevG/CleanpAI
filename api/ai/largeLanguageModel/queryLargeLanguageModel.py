import requests
import json
import re
import os
from typing import Dict, Any

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")

PLANTILLA_PROMPT_RIESGO = """
Eres un sistema especializado en detección de fraudes y evaluación de riesgos financieros.

**CONTEXTO DEL CLIENTE:**
- Perfil: {edad} años, salario: {salario}€, zona: {zona}
- Historial de transacciones: {total_transacciones} operaciones

**HISTORIAL RECIENTE DEL CLIENTE (últimas transacciones):**
{historial_reciente}

**TRANSACCIÓN ACTUAL A EVALUAR:**
{transaccion_actual}

**PATRONES DE RIESGO A CONSIDERAR:**
1. Compras en categorías de alto riesgo (gambling, criptomonedas...)
2. Primeras compras en comercios desconocidos
4. Patrones inconsistentes con el comportamiento histórico
5. Transacciones recurrentes sospechosas
6. Incrementos altos en pagos recurentes respecto al historial
7. Recobros de antiguas suscripciones o servicios
8. Movimientos repetidos en cortos periodos de tiempo del mismo producto o servicio

**INSTRUCCIÓN:**
Analiza la transacción actual en contexto del historial del cliente y devuelve SOLO un número entre 0.00 y 1.00 (puede tener 2 decimales) donde:
- 0.00 = Riesgo mínimo (transacción normal, consistente con el historial)
- 1.00 = Riesgo máximo (múltiples señales de fraude)
Entonces tienes que decidir según tu conocimiento y el contexto dado, ¿cuál es la probabilidad de que esta transacción sea fraudulenta?

NO DEVUELVAS NADA MÁS. SOLO EL NÚMERO DEL 0.00 AL 1.00. SOLO EL NÚMERO DEL 0.00 AL 1.00. SOLO EL NÚMERO DEL 0.00 AL 1.00.
"""


def preparar_historial_reciente(historial_completo: Dict[str, Any], limite: int = 10) -> str:
    transacciones = historial_completo.get('transactions', [])
    
    transacciones_ordenadas = sorted(
        transacciones, 
        key=lambda x: x.get('transaction_date', ''), 
        reverse=True
    )[:limite]
    
    resumen = []
    for i, trans in enumerate(transacciones_ordenadas, 1):
        resumen.append(
            f"{i}. {trans.get('product_category', 'N/A')} - "
            f"{trans.get('transaction_value', 0):.2f}€ - "
            f"{trans.get('collector_company', 'N/A')} - "
            f"Recurrente: {trans.get('is_recurring', False)} - "
            f"Reembolsado: {trans.get('has_been_refunded', False)}"
        )
    
    return "\n".join(resumen) if resumen else "No hay historial reciente"

def queryLargeLanguageModel(transaccion_actual: Dict[str, Any], historial_completo: Dict[str, Any]) -> float:
    perfil = historial_completo.get('user_profile', {})
    edad = perfil.get('age', 'N/A')
    salario = perfil.get('salary_usd', 'N/A')
    zona = "urbana" if perfil.get('is_urban', False) else "rural"
    total_transacciones = len(historial_completo.get('transactions', []))

    historial_reciente = preparar_historial_reciente(historial_completo)

    transaccion_formateada = json.dumps(transaccion_actual, indent=2, ensure_ascii=False)
    
    prompt_final = PLANTILLA_PROMPT_RIESGO.format(
        edad=edad,
        salario=salario,
        zona=zona,
        total_transacciones=total_transacciones,
        historial_reciente=historial_reciente,
        transaccion_actual=transaccion_formateada
    )

    payload = {
        "model": "cas/salamandra-7b-instruct:latest",
        "prompt": prompt_final,
        "stream": False,
    }

    try:
        while (True):
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()

            response_data = response.json()
            respuesta_texto = response_data['response'].strip()

            match = re.search(r"0?\.\d+", respuesta_texto)
        
            if match:
                numero_encontrado = match.group(0)
                if numero_encontrado.startswith('.'):
                    numero_encontrado = '0' + numero_encontrado
                
                riesgo = float(numero_encontrado)
                print(riesgo)
                return riesgo
            
    except Exception:
        print("e0.5")
        return 0.5