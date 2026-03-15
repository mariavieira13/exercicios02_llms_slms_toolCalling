"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 3 — Conversão de Temperatura

Crie as funções:

- `celsius_para_fahrenheit`
- `fahrenheit_para_celsius`

Mensagens possíveis:

Converter 30 graus Celsius para Fahrenheit
Quanto é 80F em Celsius?

O programa deve interpretar a mensagem e chamar a função correta.

"""

from email.mime import message
import json
from urllib import response
from dotenv import load_dotenv
from groq import Groq
from tools import celsius_para_fahrenheit, fahrenheit_para_celsius

load_dotenv()
client = Groq()

tools=[
{
        "type":"function",
        "function":{
            "name":"celsius_para_fahrenheit",
            "description":"Converte Celsius para Fahrenheit",
            "parameters":{
            "type":"object",
            "properties":{
                "c":{"type":"number"}
            },
            "required":["c"]
        }
    }
},

{
        "type":"function",
        "function":{
            "name":"fahrenheit_para_celsius",
            "description":"Converte Fahrenheit para Celsius",
            "parameters":{
            "type":"object",
            "properties":{
                "f":{"type":"number"}
            },
            "required":["f"]
        }
    }
}
]

def perguntar(pergunta):

    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"system",
                "content":"Escolha qual conversão usar"
            },
            {
                "role":"user",
                "content":pergunta
            }
        ],
        tools=tools,
        tool_choice="auto"
    )

    message=response.choices[0].message

    if message.tool_calls:
        call=message.tool_calls[0]
        name=call.function.name
        args=json.loads(call.function.arguments)

        if name=="celsius_para_fahrenheit":
            return celsius_para_fahrenheit(**args)

        if name=="fahrenheit_para_celsius":
            return fahrenheit_para_celsius(**args)

    return message.content


print(perguntar("Converter 30 graus Celsius para Fahrenheit"))
print(perguntar("Quanto é 80F em Celsius?"))