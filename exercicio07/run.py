"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 7 — Consulta de Clima

Crie a função:
buscar_clima(cidade)

Base de dados fictícia:
clima = {
    "sao paulo": "24°C e nublado",
    "bauru": "30°C e ensolarado",
    "curitiba": "18°C e chuvoso"
}

Mensagens possíveis:
Como está o clima em Bauru?
Qual a temperatura em Curitiba?

O programa deve extrair o nome da cidade e chamar a função.

"""

import json
from dotenv import load_dotenv
from groq import Groq
from tools import buscar_clima

load_dotenv()

client = Groq()

tools = [
{
        "type": "function",
        "function": {
        "name": "buscar_clima",
        "description": "Busca o clima de uma cidade",
        "parameters": {
        "type": "object",
        "properties": {
            "cidade": {
                "type": "string",
                "description": "Nome da cidade"
            }
            },
            "required": ["cidade"]
        }
    }
}
]

def perguntar(pergunta: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Você decide qual cidade consultar o clima."},
            {"role": "user", "content": pergunta}
        ],
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        print(f"Tool chamada: buscar_clima")
        print(f"Argumentos: {args}")

        return buscar_clima(**args)

    return message.content


print(perguntar("Como está o clima em Bauru?"))
print(perguntar("Qual a temperatura em Curitiba?"))