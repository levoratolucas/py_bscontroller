class UserView:
    def mostrar(self, usuarios):
        for u in usuarios:
            print(f"Bom dia {u.nome}! Idade: {u.idade} Sexo: {u.sexo}")
