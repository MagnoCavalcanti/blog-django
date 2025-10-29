document.addEventListener('DOMContentLoaded', function () {
    // Helpers
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const url = window.location.pathname;
    const parts = url.split('/');
    const postId = parts[2] || null; // /posts/<id>/ -> index 2

    const deleteBtn = document.getElementById('delete');
    const editBtn = document.getElementById('edit');
    const likeBtn = document.getElementById('like-btn');
    const likeCount = document.getElementById('like-count');

    // DELETE do post via fetch DELETE (AJAX)
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => {
            if (!postId) return alert('ID do post não encontrado.');
            fetch(`/posts/${postId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';
                } else {
                    alert('Erro ao excluir post');
                }
            })
            .catch(err => {
                console.error('Erro na requisição DELETE:', err);
                alert('Erro na requisição');
            });
        });
    }

    // Modal de edição (se existir)
    if (editBtn) {
        const dialog = document.querySelector('#edit-modal');
        editBtn.addEventListener('click', () => {
            if (dialog && typeof dialog.showModal === 'function') dialog.showModal();
        });
        if (dialog) {
            dialog.addEventListener('click', function(event) {
                if (event.target === dialog) dialog.close();
            });
        }
    }

    // Curtir (like) via fetch POST
    if (likeBtn) {
        likeBtn.addEventListener('click', async function () {
            if (!postId) return console.error('postId não encontrado');
            try {
                const response = await fetch(`/curtir/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json'
                    },
                });

                if (!response.ok) {
                    console.error('Resposta não OK ao curtir:', response.status);
                    return;
                }

                const data = await response.json();

                // Atualiza o contador se existir
                if (likeCount) likeCount.innerText = `${data.likes_count}`;

                // Atualiza o botão (icone) visualmente
                likeBtn.innerHTML = data.liked
                    ? `<img width="18" height="18" src="https://img.icons8.com/fluency-systems-filled/48/F91880/like.png" alt="like"/> <span class="active" id="like-count">${data.likes_count}</span>`
                    : `<img width="18" height="18" src="https://img.icons8.com/fluency-systems-regular/48/8899a6/like--v1.png" alt="like--v1"/><span id="like-count">${data.likes_count}</span>`;

            } catch (err) {
                console.error('Erro ao curtir:', err);
            }
        });
    }
})