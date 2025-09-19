let btn = document.getElementById("delete-post")
let url = window.location.pathname
let parts = url.split("/")
const postId = parts[2]

btn.addEventListener("click", () => {
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