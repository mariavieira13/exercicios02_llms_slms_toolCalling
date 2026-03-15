eventos=[]

def criar_evento(titulo: str, data: str):
    evento = {"titulo": titulo, "data": data}
    eventos.append(evento)
    return f"Evento '{titulo}' criado para {data}." 

def listar_eventos():
    if not eventos:
        return "Nenhum evento cadastrado."
    return eventos

