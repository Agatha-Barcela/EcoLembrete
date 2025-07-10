// Pegamos o elemento HTML com id "contador"
const contador = document.getElementById('contador');

// Verifica se o elemento contador existe na página
if (contador) {
  // Pegamos o tempo restante (em segundos) do atributo data-tempo
  let tempoRestante = parseInt(contador.dataset.tempo);

  // Função que formata o tempo em dias, horas, minutos e segundos
  function formatarTempo(segundos) {
    const dias = Math.floor(segundos / (60 * 60 * 24)); // Calcula os dias
    const horas = Math.floor((segundos % (60 * 60 * 24)) / 3600); // Calcula as horas restantes
    const minutos = Math.floor((segundos % 3600) / 60); // Calcula os minutos restantes
    const segundosRestantes = segundos % 60; // Calcula os segundos restantes

    // Retorna o tempo formatado no estilo DD:HH:MM:SS
    return `${dias.toString().padStart(2, '0')}:${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${segundosRestantes.toString().padStart(2, '0')}`;
  }

  // Função que atualiza o contador na tela a cada segundo
  function atualizarContador() {
    // Mostra o tempo atual formatado
    contador.textContent = formatarTempo(tempoRestante);

    // Se ainda há tempo, espera 1 segundo e atualiza de novo
    if (tempoRestante > 0) {
      tempoRestante--;
      setTimeout(atualizarContador, 1000); // Chama essa função de novo depois de 1 segundo
    } else {
      // Quando o tempo acabar, mostra tudo zerado e redireciona
      contador.textContent = "00:00:00:00";
      redirecionarParaLembrete();
    }
  }

  // Função que redireciona automaticamente para /lembrete (via POST)
  function redirecionarParaLembrete() {
    const form = document.createElement('form'); // Cria um formulário
    form.method = 'POST'; // Define o método como POST
    form.action = '/lembrete'; // Define a rota de envio
    document.body.appendChild(form); // Adiciona o formulário no corpo do HTML
    form.submit(); // Envia o formulário
  }

  // Começa o contador logo que a página carrega
  atualizarContador();
}

// Função que pergunta se o usuário quer voltar pra página inicial
function confirmarVoltarInicio() {
  const confirmacao = confirm("Se você voltar agora, os dados preenchidos serão descartados. Deseja continuar?");
  if (confirmacao) {
    window.location.href = "/"; // Redireciona para a página inicial
  }
}
