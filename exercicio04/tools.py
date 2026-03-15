def buscar_produto(nome_produto: str):
    produtos={
        "notebook":4500,
        "mouse":80,
        "teclado":150
    }
    
    nome_produto = nome_produto.lower()
    if nome_produto in produtos:
        return f"Preço do {nome_produto}: R${produtos[nome_produto]}"
    else:
        return "Produto não encontrado"