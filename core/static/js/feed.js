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



    document.querySelectorAll('#postID').forEach(article => {
        article.addEventListener('click', (e) => {
            // Evita conflitos com botões internos (comentários, curtidas, etc.)
            const isButton = e.target.closest('.action-button');
            if (!isButton) {
                const url = article.getAttribute('data-url');
                window.location.href = url;
            }
            });
    });
});