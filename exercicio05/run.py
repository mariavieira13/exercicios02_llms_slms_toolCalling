"""
    ATENÇÃO – CÓDIGO EDUCACIONAL (NÃO UTILIZAR EM PRODUÇÃO)

    Este código foi desenvolvido exclusivamente para fins didáticos,
    no contexto da disciplina Tecnologias e Programação Integrada.

    O objetivo é demonstrar o uso de LLMs/SLMs com tool calling, permitindo
    que um modelo de linguagem decida qual função Python executar a
    partir de uma entrada em linguagem natural.
"""

"""
# Exercício 5 — Verificação de Estoque

Crie funções:

- `buscar_produto`
- `verificar_estoque`

Base de dados:
estoque = {
    "notebook": 5,
    "mouse": 20,
    "teclado": 8
}

Mensagens possíveis:

Tem notebook em estoque?
Quantos mouses temos?

O sistema deve decidir qual função chamar.
"""

import json
from dotenv import load_dotenv
from groq import Groq
from tools import buscar_produto, verificar_estoque

load_dotenv()

client = Groq()

tools = [
{
        "type": "function",
        "function": {
            "name": "buscar_produto",
            "description": "Verifica se um produto existe no estoque",
            "parameters": {
            "type": "object",
            "properties": {
                "nome_produto": {
                    "type": "string",
                    "description": "Nome do produto"
                }
            },
            "required": ["nome_produto"]
        }
    }
},

{
        "type": "function",
        "function": {
            "name": "verificar_estoque",
            "description": "Verifica quantas unidades do produto contém no estoque",
            "parameters": {
            "type": "object",
            "properties": {
                "nome_produto": {
                    "type": "string",
                    "description": "Nome do produto"
                }
            },
            "required": ["nome_produto"]
        }
    }
}
]

def perguntar(pergunta: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "Você decide qual função usar para consultar estoque."},
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

        if tool_name == "buscar_produto":
            return buscar_produto(**args)

        if tool_name == "verificar_estoque":
            return verificar_estoque(**args)

    return message.content


print(perguntar("Tem notebook em estoque?"))
print(perguntar("Quantos mouses temos?"))