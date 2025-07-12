# Importa as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, session  # Flask e utilitários
from datetime import datetime, timedelta  # Para lidar com datas e horários
from mensagens import gerar_mensagem  # Função externa que retorna uma mensagem e tema aleatório



# Cria a aplicação Flask
app = Flask(__name__)

# Define uma chave secreta para manter a sessão segura (obrigatória para usar 'session')
app.secret_key = 'segredo'



# Rota inicial – página onde o usuário informa seu nome
@app.route('/', methods=['GET'])
def inicio():
    return render_template('nome.html')  # Carrega o template com o campo de nome

# Rota do formulário principal (frequência, horário e ocupação)
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Salva o nome na sessão (acessível entre páginas)
        session['nome'] = request.form.get('nome')
    return render_template('formulario.html')  # Exibe o formulário para o usuário

# Rota de espera – mostra um contador até o próximo lembrete
@app.route('/aguardar', methods=['POST', 'GET'])
def aguardar():
    if request.method == 'POST':
        # Salva as respostas do formulário na sessão
        session['frequencia'] = request.form.get('frequencia')
        session['horario'] = request.form.get('horario')
        session['ocupacao'] = request.form.get('ocupacao')

    # Recupera dados salvos da sessão
    horario_str = session.get('horario')
    frequencia = session.get('frequencia')

    # Se alguma informação estiver faltando, volta para o formulário
    if not horario_str or not frequencia:
        return redirect('/formulario')

    agora = datetime.now()
    try:
        # Separa hora e minuto da string "HH:MM"
        hora, minuto = map(int, horario_str.split(':'))
    except Exception:
        return redirect('/formulario')  # Se der erro, volta para o formulário

    # Cria um objeto datetime com a hora desejada
    proximo = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)

    # Se o horário já passou no dia atual, adiciona o intervalo correto (diário, semanal, etc.)
    if proximo <= agora:
        proximo += calcular_intervalo(frequencia)

    # Salva o horário do próximo lembrete na sessão
    session['proximo_lembrete'] = proximo.isoformat()  # Converte para string ISO

    # Calcula quanto tempo falta em segundos e envia para o HTML
    tempo = calcular_tempo_restante(session.get('proximo_lembrete'))
    return render_template('aguardar.html', tempo_restante=tempo)

# Rota que mostra o lembrete aleatório (tema e mensagem)
@app.route('/lembrete', methods=['POST'])
def lembrete():
    nome = session.get('nome', '')  # Recupera o nome da sessão (ou vazio, se não existir)
    mensagem, tema = gerar_mensagem(nome)  # Gera mensagem personalizada com o nome
    return render_template('lembrete.html', mensagem=mensagem, tema=tema)  # Exibe o lembrete



# Retorna um intervalo de tempo (timedelta) com base na frequência escolhida
def calcular_intervalo(freq):
    if freq == 'diario':
        return timedelta(days=1)
    elif freq == 'semanal':
        return timedelta(days=7)
    elif freq == 'mensal':
        return timedelta(days=30)
    return timedelta(minutes=0)  # Valor padrão se não bater nenhum

# Calcula o tempo restante até a hora marcada (em segundos)
def calcular_tempo_restante(futuro):
    agora = datetime.now()

    if not futuro:
        return 0  # Sem tempo futuro definido

    # Se o dado estiver em formato de string, converte para datetime
    if isinstance(futuro, str):
        try:
            futuro = datetime.fromisoformat(futuro)
        except ValueError:
            return 0  # Se falhar a conversão, retorna 0

    # Remove qualquer informação de fuso horário (se existir)
    agora = agora.replace(tzinfo=None)
    futuro = futuro.replace(tzinfo=None)

    if futuro <= agora:
        return 0  # Já passou o horário

    # Calcula a diferença em segundos
    restante = futuro - agora
    return int(restante.total_seconds())


@app.route('/lembrete-aleatorio', methods=['POST'])
def lembrete_aleatorio():
    nome = session.get('nome', '')
    mensagem, tema = gerar_mensagem(nome)
    return render_template('lembrete_aleatorio.html', mensagem=mensagem, tema=tema)

# Inicia o servidor Flask em modo de debug
if __name__ == '__main__':
    app.run(debug=True)
