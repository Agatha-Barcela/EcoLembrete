from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
from mensagens import gerar_mensagem  # Função que retorna uma mensagem e um tema aleatório

app = Flask(__name__)
app.secret_key = 'segredo'  # Chave secreta para manter os dados da sessão seguros

# Rota inicial – Página para o usuário digitar o nome
@app.route('/', methods=['GET'])
def inicio():
    return render_template('nome.html')

# Rota do formulário principal
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Armazena o nome na sessão
        session['nome'] = request.form.get('nome')
    return render_template('formulario.html')

# Rota de espera, mostra o contador para o próximo lembrete
@app.route('/aguardar', methods=['POST', 'GET'])
def aguardar():
    if request.method == 'POST':
        # Salva as respostas do formulário na sessão
        session['frequencia'] = request.form.get('frequencia')
        session['horario'] = request.form.get('horario')
        session['ocupacao'] = request.form.get('ocupacao')

    horario_str = session.get('horario')
    frequencia = session.get('frequencia')

    # Se algo estiver faltando, redireciona de volta ao formulário
    if not horario_str or not frequencia:
        return redirect('/formulario')

    agora = datetime.now()
    try:
        # Transforma o horário em hora e minuto
        hora, minuto = map(int, horario_str.split(':'))
    except Exception:
        return redirect('/formulario')

    # Define o horário do próximo lembrete
    proximo = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Se o horário já passou hoje, adiciona o intervalo escolhido
    if proximo <= agora:
        proximo += calcular_intervalo(frequencia)

    # Salva o horário futuro na sessão
    session['proximo_lembrete'] = proximo.isoformat()

    # Calcula os segundos restantes e envia para o contador
    tempo = calcular_tempo_restante(session.get('proximo_lembrete'))
    return render_template('aguardar.html', tempo_restante=tempo)

# Rota que exibe o lembrete aleatório (após o tempo acabar)
@app.route('/lembrete', methods=['POST'])
def lembrete():
    nome = session.get('nome', '')
    mensagem, tema = gerar_mensagem(nome)  # Puxa uma mensagem personalizada
    return render_template('lembrete.html', mensagem=mensagem, tema=tema)

# Função para calcular o intervalo de tempo com base na frequência
def calcular_intervalo(freq):
    if freq == 'diario':
        return timedelta(days=1)
    elif freq == 'semanal':
        return timedelta(days=7)
    elif freq == 'mensal':
        return timedelta(days=30)
    return timedelta(minutes=0)

# Função para calcular o tempo restante até o próximo lembrete
def calcular_tempo_restante(futuro):
    agora = datetime.now()

    if not futuro:
        return 0

    # Converte de string para objeto datetime, se necessário
    if isinstance(futuro, str):
        try:
            futuro = datetime.fromisoformat(futuro)
        except ValueError:
            return 0

    # Garante que os objetos datetime estejam sem fuso horário
    agora = agora.replace(tzinfo=None)
    futuro = futuro.replace(tzinfo=None)

    # Se já passou, retorna 0
    if futuro <= agora:
        return 0

    restante = futuro - agora
    return int(restante.total_seconds())  # Retorna o tempo em segundos

# Executa o app
if __name__ == '__main__':
    app.run(debug=True)
