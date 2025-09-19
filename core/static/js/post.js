let btn = document.getElementById("delete-post")
console.log(btn);
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
        .then(response => response.json)
        .then(data => {
            if (data.success) {
                window.location.href("/"); // recarrega o feed
            } else {
                alert("Erro ao excluir post");
            }
        })
        
})