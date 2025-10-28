// static/js/feed.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Lógica do Dialogo (Modal) ---
    const dialog = document.querySelector('dialog');
    const openBtn = document.getElementById('open-dialog-btn'); 

    if (openBtn && dialog) {
        openBtn.addEventListener('click', function() {
            dialog.showModal();
        });
        
        // Fechar o modal ao clicar fora
        dialog.addEventListener('click', function(event) {
            if (event.target === dialog) {
                dialog.close();
            }
        });
    }
});