clima = {
    "sao paulo": "24°C e nublado",
    "bauru": "30°C e ensolarado",
    "curitiba": "18°C e chuvoso"
}

def buscar_clima(cidade: str):
    cidade=cidade.lower()

    if cidade in clima:
        return f"Clima em {cidade}: {clima[cidade]}"
    else:
        return "Cidade não encontrada"
    
