document.addEventListener('DOMContentLoaded', () => {
   
    const porcentagem = 0; 

    const progressCircle = document.querySelector('.circular-progress');
    const progressValue = document.querySelector('.progress-value');
    const situacaoText = document.getElementById('situacaoText');


    progressValue.textContent = `${porcentagem}%`;


    progressCircle.style.background = `
        radial-gradient(circle at center, #f5f0f8 60%, transparent 60%),
        conic-gradient(#6b4faa 0% ${porcentagem}%, #d3c1e5 ${porcentagem}% 100%)
    `;

    // Mensagens do situacaoText
    if (porcentagem === 0) {
        situacaoText.textContent = "Ainda não há dados para analisar a situação.";
    } else if (porcentagem <= 33) {
        situacaoText.textContent = "Situação aparentemente estável.";
    } else if (porcentagem <= 66) {
        situacaoText.textContent = "Reaja: possíveis sinais de alerta.";
    } else {
        situacaoText.textContent = "Denuncie: situação de risco elevado.";
    }
});
