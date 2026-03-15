"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 4 — Consulta de Produto

Crie a função:
buscar_produto(nome_produto)

Use um dicionário como base de dados:
produtos = {
    "notebook": 4500,
    "mouse": 80,
    "teclado": 150
}

Mensagens possíveis:
Qual o preço do notebook?
Quanto custa um mouse?7

O sistema deve identificar o produto e chamar `buscar_produto`.

"""

from email import message
import json
from urllib import response
from dotenv import load_dotenv
from groq import Groq
from tools import buscar_produto

load_dotenv()

client=Groq()

tools=[
{
        "type":"function",
        "function":{
            "name":"buscar_produto",
            "description":"Busca o valor de um produto",
            "parameters":{
            "type":"object",
            "properties":{
                "nome_produto":{"type":"string"}
            },
            "required":["nome_produto"]
        }
    }
}
]

def perguntar(pergunta):

    response=client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
    {"role":"system","content":"Identifique qual produto procurar"},
    {"role":"user","content":pergunta}
    ],
    tools=tools,
    tool_choice="auto"
    )

    message=response.choices[0].message

    if message.tool_calls:
        call=message.tool_calls[0]
        args=json.loads(call.function.arguments)

        return buscar_produto(**args)

    return message.content

print(perguntar("Qual o preço do notebook?"))
print(perguntar("Quanto custa um mouse?"))