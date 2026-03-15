"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 6 — Sistema de Agenda

Crie funções:
criar_evento(titulo, data)
listar_eventos()

Armazene eventos em uma lista.

Mensagens possíveis:
Criar evento reunião amanhã
Mostrar meus eventos

O sistema deve interpretar a mensagem e chamar a função correta.

"""

import json
from dotenv import load_dotenv
from groq import Groq
from tools import criar_evento, listar_eventos

load_dotenv()

client = Groq()

tools = [
{
        "type": "function",
        "function": {
        "name": "criar_evento",
        "description": "Cria um novo evento na agenda",
        "parameters": {
        "type": "object",
        "properties": {
            "titulo": {"type": "string"},
            "data": {"type": "string"}
            },
            "required": ["titulo", "data"]
        }
    }
},

{
        "type": "function",
        "function": {
        "name": "listar_eventos",
        "description": "Lista todos os eventos cadastrados na agenda",
        "parameters": {
        "type": "object",
        "properties": {}
        }
    }
}
]

def perguntar(pergunta: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Você decide qual função da agenda utilizar."},
            {"role": "user", "content": pergunta}
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

        if tool_name == "criar_evento":
            return criar_evento(**args)

        if tool_name == "listar_eventos":
            return listar_eventos()

    return message.content


print(perguntar("Criar evento reunião amanhã"))
print(perguntar("Mostrar meus eventos"))