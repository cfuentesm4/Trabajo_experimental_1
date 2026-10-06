clientes = [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Luis"}
]

indice = {cliente["id"]: cliente for cliente in clientes}

print(indice[2]["nombre"])