estoque={
    "notebook":5,
    "mouse":20,
    "teclado":8 
}

def buscar_produto(nome_produto:str):
    if nome_produto in estoque:
        return f"{nome_produto} disponível"
    else:
        return "Produto não disponível"

def verificar_estoque(nome_produto:str):
    if nome_produto in estoque:
        return f"Temos {estoque[nome_produto]} unidades de {nome_produto} em estoque"
    else:
        return "Não temos esse produto disponível em estoque"