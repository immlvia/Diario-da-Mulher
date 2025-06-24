
// Funcionalidade para checkboxes do diário
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os checkboxes do formulário
    const checkboxes = document.querySelectorAll('#registroDiarioForm input[type="checkbox"]');
    
    // Adiciona evento de clique para cada checkbox
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.closest('label');
            
            if (this.checked) {
                // Adiciona classe quando marcado
                label.classList.add('selecionado');
            } else {
                // Remove classe quando desmarcado
                label.classList.remove('selecionado');
            }
        });
    });
    
    // Adiciona funcionalidade de clique no label para marcar/desmarcar
    const labels = document.querySelectorAll('#registroDiarioForm label');
    labels.forEach(label => {
        label.addEventListener('click', function(e) {
            // Se clicou diretamente no label (não em um elemento filho)
            if (e.target === this) {
                const checkbox = this.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    checkbox.dispatchEvent(new Event('change'));
                }
            }
        });
    });
    
    // Adiciona funcionalidade de teclado para acessibilidade
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.checked = !this.checked;
                this.dispatchEvent(new Event('change'));
            }
        });
    });
});