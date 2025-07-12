const contador = document.getElementById('contador');

// Flag para evitar chamadas duplicadas
let lembreteEnviado = false;

if (contador) {
  let tempoRestante = parseInt(contador.dataset.tempo);

  function formatarTempo(segundos) {
    const dias = Math.floor(segundos / (60 * 60 * 24));
    const horas = Math.floor((segundos % (60 * 60 * 24)) / 3600);
    const minutos = Math.floor((segundos % 3600) / 60);
    const segundosRestantes = segundos % 60;
    return `${dias.toString().padStart(2, '0')}:${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${segundosRestantes.toString().padStart(2, '0')}`;
  }

  function atualizarContador() {
    contador.textContent = formatarTempo(tempoRestante);

    if (tempoRestante > 0) {
      tempoRestante--;
      setTimeout(atualizarContador, 1000);
    } else {
      contador.textContent = "00:00:00:00";
      redirecionarParaLembrete();
    }
  }

  function redirecionarParaLembrete() {
    if (lembreteEnviado) return;  // Impede múltiplas chamadas
    lembreteEnviado = true;

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/lembrete';
    document.body.appendChild(form);
    form.submit();
  }

  atualizarContador();
}

// Função para confirmar se o usuário quer voltar à página inicial
function confirmarVoltarInicio() {
  const confirmacao = confirm("Se você voltar agora, os dados preenchidos serão descartados. Deseja continuar?");
  if (confirmacao) {
    window.location.href = "/";
  }
}
