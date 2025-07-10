import random
from datetime import datetime

# Lista de mensagens gerais para qualquer dia
mensagens_gerais = [
    "Leve sua ecobag, recuse plásticos. Pequenas ações mudam o mundo.",
    "Apague as luzes ao sair. Economize energia.",
    "Reutilize potes, garrafas e sacolas sempre que puder.",
    "Use transporte público ou bicicleta quando possível.",
    "Evite o desperdício de água. Feche a torneira ao escovar os dentes."
]

# Mensagens específicas para dias da semana
mensagens_condicionais = {
    'segunda-feira': ["Comece a semana plantando uma ideia sustentável!"],
    'sexta-feira': ["Sextou com consciência! Recolha seu lixo e inspire outros."],
    'domingo': ["Domingo é dia de cuidar do planeta também."]
}

# Temas possíveis que acompanham as mensagens
temas = ["Poluição", "Consumo Consciente", "Economia de Energia", "Descarte Correto", "Água"]

# Função que retorna uma mensagem e tema aleatório, personalizada com o nome
def gerar_mensagem(nome):
    # Pega o dia da semana atual em minúsculo (ex: 'segunda-feira')
    hoje = datetime.today().strftime('%A').lower()

    # Começa com as mensagens gerais disponíveis
    mensagens_validas = list(mensagens_gerais)

    # Se o dia atual tiver mensagens específicas, adiciona elas
    for dia, lista in mensagens_condicionais.items():
        if dia.lower() == hoje:
            mensagens_validas.extend(lista)

    # Escolhe uma mensagem aleatória das válidas
    mensagem = random.choice(mensagens_validas)

    # Escolhe um tema aleatório
    tema = random.choice(temas)

    # Se o nome for informado, adiciona uma frase personalizada
    if nome:
        mensagem = f"{mensagem} 🌱 {nome.capitalize()}, você faz a diferença!"

    # Retorna a mensagem e o tema para o app usar
    return mensagem, tema
