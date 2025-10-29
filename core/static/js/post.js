let deleteBtn = document.getElementById("delete")
let url = window.location.pathname
let parts = url.split("/")
const postId = parts[2]

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