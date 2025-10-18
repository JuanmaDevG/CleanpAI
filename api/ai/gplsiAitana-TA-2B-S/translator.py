from openai import OpenAI


def traducir_a_valenciano(texto_espanol):
    hf_token = "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" # token de Maryan Iavorskyy

    client = OpenAI(
        base_url = "https://y9qb4ck1bebf371m.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key = hf_token
    )

    chat_completion = client.chat.completions.create(
        model = "gplsi/Aitana-TA-2B-S",
        messages = [{
            "role": "user",
            "content": f"Traduce el siguiente texto del español al valenciano.\nEspañol: {texto_espanol}\nValenciano:"
        }],
        stream = True
    )

    traduccion = ""
    for message in chat_completion:
        if message.choices[0].delta.content:
            contenido = message.choices[0].delta.content
            traduccion += contenido
    
    return traduccion