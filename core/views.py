from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment, User
from django.shortcuts import redirect

def feed(request):
    posts = Post.objects.all().order_by('-created_by')  # Ordena do mais recente para o mais antigo
    return render(request, 'pages/feed.html', {'posts': posts})

def curtir_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        # incrementa o campo `likes` definido no modelo
        post.likes = (post.likes or 0) + 1
        post.save()
        return JsonResponse({"likes": post.likes})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        # criar um comentário simples
        content = request.POST.get('content')
        author = User.objects.first()
        if content and author:
            Comment.objects.create(post=post, author=author, content=content)
            return redirect('post_detail', post_id=post.id)

    comments = post.comments.all().order_by('created_by')
    return render(request, 'pages/post.html', {'post': post, 'comments': comments})
