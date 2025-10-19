from httpx import options
import requests
import json
import re

from typing import Dict, Any


OLLAMA_URL = "http://localhost:11434/api/generate"

PLANTILLA_PROMPT_RIESGO = """
Eres un sistema especializado en detección de fraudes y evaluación de riesgos financieros.
Obedece estrictamente estas reglas de salida:

Salida única: responde en una sola línea y nada más.

Formato exacto: [<numero>]: <porque>

Rango: <numero> debe estar entre 0.00 y 1.00, con exactamente 2 decimales.

Normalización obligatoria: si cualquier razonamiento interno te da un valor >1 o en otra escala (p. ej., 2, 3, 4, 7, 35%, 8/10), normaliza a [0,1] antes de escribirlo (ej.: 3 → 0.30; 35% → 0.35; 8/10 → 0.80) y redondea a 2 decimales. Nunca escribas un número fuera de [0.00, 1.00].

Explicación breve: <porque> debe ser una sola frase, breve (≤ 20 palabras), aludiendo a los patrones relevantes.

No añadas saludos, etiquetas, listas, justificaciones largas, JSON ni texto adicional.

Rúbrica de decisión (guía interna):

Señales fuertes simultáneas (p. ej., categoría de alto riesgo + primer comercio + importe muy superior al histórico + recurrencia anómala) → 0.75–0.95.

Varias señales moderadas o una fuerte aislada → 0.40–0.74.

Señales débiles o leve desviación del patrón habitual → 0.15–0.39.

Consistente con el historial y sin señales → 0.00–0.14.

Patrones de riesgo a considerar (pondera en contexto):

Compras en categorías de alto riesgo (gambling, cripto...).

Primeras compras en comercios desconocidos.

Patrones inconsistentes con el comportamiento histórico.

Transacciones recurrentes sospechosas.

Incrementos altos en pagos recurrentes vs. historial.

Recobros de antiguas suscripciones/servicios.

Movimientos repetidos en corto periodo del mismo producto/servicio.

Entrada
CONTEXTO DEL CLIENTE:
Perfil: {edad} años, salario: {salario}€, zona: {zona}
Historial de transacciones: {total_transacciones} operaciones

HISTORIAL RECIENTE DEL CLIENTE (últimas transacciones):
{historial_reciente}

TRANSACCIÓN ACTUAL A EVALUAR:
{transaccion_actual}

Instrucción
Analiza la transacción actual en el contexto del historial y devuelve únicamente la línea en el formato exigido.

Ejemplos (aprendizaje por demostración)

Válido (primer comercio, importe x3, categoría cripto):
[0.82]: Primer pago en comercio cripto con importe muy superior a su histórico reciente.

Válido (suscripción habitual, importe estable):
[0.06]: Cargo recurrente conocido y consistente en importe y periodicidad.

Válido (recobro antiguo + incremento fuerte):
[0.71]: Recobro de suscripción inactiva con incremento de importe frente a histórico.

Corrección de escala (modelo tendería a poner “3”):
Nunca 3 → Siempre 0.30
[0.30]: Desviación moderada en importe y comercio poco frecuente.

Corrección de porcentaje (modelo tendería a poner “35%”):
Nunca 35% → Siempre 0.35
[0.35]: Comercio nuevo con ligero aumento frente a compras previas en la categoría.

Recuerda: Sólo una línea con el formato exacto; el número siempre entre 0.00 y 1.00 con dos decimales.
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
        "options": {
            "temperature": 0/0.2 
        }
    }

    try:
        while (True):
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()

            response_data = response.json()
            respuesta_texto = response_data['response'].strip()

            print(f'/n/nres: "{respuesta_texto}/n/n"')

            match = re.search(r"\[([0-9]*\.?[0-9]+)\]:\s*(.+)", respuesta_texto)
    
            if match:
                numero_encontrado = match.group(1)
                mensaje = match.group(2).strip()
        
                riesgo = float(numero_encontrado)
                return riesgo, mensaje
            else:
                match_numero = re.search(r"0?\.\d+", respuesta_texto)
                if match_numero:
                    numero_encontrado = match_numero.group(0)
                    if numero_encontrado.startswith('.'):
                        numero_encontrado = '0' + numero_encontrado
            
                    riesgo = float(numero_encontrado)
                    return riesgo, "No se pudo extraer el mensaje"
    except Exception:
        return 0.5, "Error en la evaluación del riesgo"