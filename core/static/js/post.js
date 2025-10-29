document.addEventListener('DOMContentLoaded', function () {
    let deleteBtn = document.getElementById("delete")
    let url = window.location.pathname
    let parts = url.split("/")
    const postId = parts[2]

    if(!!deleteBtn){
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


        let editBtn = document.getElementById("edit")
        let dialog = document.querySelector("dialog")

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

    console.log(data.likes_count);
    

    // Atualiza o texto e contador
    likeCount.innerText = `${data.likes_count}`;
    
  })
})