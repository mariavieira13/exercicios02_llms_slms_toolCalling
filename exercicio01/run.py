"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 1 — Calculadora Simples

Crie duas funções:

def somar(a, b):
    return a + b

def multiplicar(a, b):
    return a * b

O programa deve receber uma mensagem do usuário, por exemplo:
Quanto é 5 + 3?

ou

Multiplique 4 por 7

O sistema deve:
1. Interpretar a mensagem  
2. Identificar a operação  
3. Chamar a função correta  
4. Mostrar o resultado

"""

import os
import json
from dotenv import load_dotenv
from groq import Groq
from tools import somar, multiplicar

load_dotenv()

client = Groq()

tools = [
    {
        "type": "function",
        "function": {
            "name": "somar",
            "description": "Calcula a soma de dois números",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "Primeiro número"
                    },
                    "b": {
                        "type": "integer",
                        "description": "Segundo número"
                    }
                },
                "required": ["a", "b"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "multiplicar",
            "description": "Calcula a multiplicação de dois números",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "Primeiro número"
                    },
                    "b": {
                        "type": "integer",
                        "description": "Segundo número"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]


def perguntar(pergunta: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente que decide qual função matemática usar."
            },
            {
                "role": "user",
                "content": pergunta
            }
        ],
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f"Tool chamada: {tool_name}")
        print(f"Argumentos: {args}")

        if tool_name == "somar":
            return somar(**args)

        if tool_name == "multiplicar":
            return multiplicar(**args)

    return message.content


print(perguntar("Quanto é 5 + 3?"))
print(perguntar("Multiplique 4 por 7"))