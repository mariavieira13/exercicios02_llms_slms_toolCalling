"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 2 — Calculadora Completa

Implemente as funções:

- `somar`
- `subtrair`
- `multiplicar`
- `dividir`

Exemplos de mensagens:
Quanto é 10 dividido por 2?
Calcule 15 menos 8

O sistema deve identificar automaticamente qual função chamar.

"""

import json
from dotenv import load_dotenv
from groq import Groq
from tools import somar, subtrair, multiplicar, dividir

load_dotenv()

client = Groq()

tools = [
    {
        "type":"function",
        "function":{
            "name":"somar",
            "description":"Calcula a soma de dois números",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"integer"},
                    "b":{"type":"integer"}
                },
                "required":["a","b"]
        }
    }
},

{
    "type":"function",
    "function":{
        "name":"subtrair",
        "description":"Calcula a diferença de dois números",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"integer"},
                "b":{"type":"integer"}
            },
            "required":["a","b"]
        }
    }
},

{
        "type":"function",
        "function":{
            "name":"multiplicar",
            "description":"Calcula a multiplicação de dois números",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"integer"},
                    "b":{"type":"integer"}
            },
            "required":["a","b"]
        }
    }
},

{
        "type":"function",
        "function":{
            "name":"dividir",
            "description":"Calcula a divisão de dois números",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{"type":"integer"},
                    "b":{"type":"integer"}
            },  
            "required":["a","b"]
        }
    }
}
]

def perguntar(pergunta:str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"system",
                "content":"Você decide qual operação matemática usar."
            },
            {
                "role":"user",
                "content":pergunta
            }
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        call=message.tool_calls[0]
        name=call.function.name
        args=json.loads(call.function.arguments)

        if name=="somar":
            return somar(**args)
        if name=="subtrair":
            return subtrair(**args)
        if name=="multiplicar":
            return multiplicar(**args)
        if name=="dividir":
            return dividir(**args)

    return message.content

print(perguntar("Quanto é 10 dividido por 2?"))
print(perguntar("Calcule 15 menos 8"))