from openai import OpenAI


def traducir_a_valenciano(texto_espanol):
    hf_token = "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"

    client = OpenAI(
        base_url="https://y9qb4ck1bebf371m.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=hf_token
    )
    
    try:
        chat_completion = client.chat.completions.create(
            model="gplsi/Aitana-TA-2B-S",
            messages=[{
                "role": "user", 
                "content": f"Traduce el siguiente texto del español al valenciano.\nEspañol: {texto_espanol}\nValenciano:"
            }],
            max_tokens=500,
            temperature=0.3
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error en traducción: {str(e)}"