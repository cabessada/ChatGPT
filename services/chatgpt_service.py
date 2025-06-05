import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ask_chatgpt(prompt: str, model="gpt-4"):
    resposta = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content.strip()
