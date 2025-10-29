document.addEventListener('DOMContentLoaded', function () {
    let deleteBtn = document.getElementById("delete")
    let url = window.location.pathname
    let parts = url.split("/")
    const postId = parts[2]
    let editBtn = document.getElementById("edit")

    if(!!deleteBtn && !!editBtn){
        deleteBtn.addEventListener("click", () => {
            fetch(`/posts/${postId}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}" // necessário se sua view exigir CSRF
                }
            })
                .then(response => {
                    console.log(response);
                    
                    if (response.ok) {
                        window.location.href = "/"; // recarrega o feed
                    } else {
                        alert("Erro ao excluir post");
                    }
                })
            
        })


        
        let dialog = document.querySelector("#edit-modal")

        editBtn.addEventListener("click", () => {
            dialog.showModal(); // Adicione os parênteses
        })

        dialog.addEventListener('click', function(event) {
            if (event.target === dialog) {
                dialog.close();
            }
        });
    }


  const likeBtn = document.getElementById('like-btn');
  const likeCount = document.getElementById('like-count');


  likeBtn.addEventListener('click', async function () {
    const response = await fetch(`/curtir/${postId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'X-Requested-With': 'XMLHttpRequest',
      },
    });

    const data = await response.json();

    

    // Atualiza o texto e contador
    likeCount.innerText = `${data.likes_count}`;

    likeBtn.innerHTML = data.liked? `<img width="18" height="18" src="https://img.icons8.com/fluency-systems-filled/48/F91880/like.png" alt="like"/> <span class="active" id="like-count">${data.likes_count}</span> ` : `<img width="18" height="18" src="https://img.icons8.com/fluency-systems-regular/48/8899a6/like--v1.png" alt="like--v1"/><span id="like-count">${data.likes_count}</span>`
    
  })
})