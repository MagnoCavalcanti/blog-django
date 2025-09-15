from django.shortcuts import render
from .models import Post

def feed(request):
    posts = Post.objects.all().order_by('-created_by')  # Ordena do mais recente para o mais antigo
    return render(request, 'pages/feed.html', {'posts': posts})
