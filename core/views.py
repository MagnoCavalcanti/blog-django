# core/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post, Comment, User, PostView # Importe PostView
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import F 
from django.utils import timezone 


class FeedView(LoginRequiredMixin, View):
    """Lista de posts (GET) e criação rápida de post (POST)."""

    def get(self, request):
        order_by = request.GET.get('order', 'views') 
        if order_by == 'views':
            posts = Post.objects.all().order_by('-views_count', '-created_by')
        else:
            posts = Post.objects.all().order_by('-created_by')
        paginator = Paginator(posts, 5)
        page = int(request.GET.get('page', 1))
        posts = paginator.page(page)

        response = {'posts': posts, 'page': page, 'current_order': order_by} 

        if 'HX-Request' in request.headers:
            return render(request, "partials/posts.html", response)

        return render(request, 'pages/feed.html', response)

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user
        if title and content and author:
            Post.objects.create(title=title, content=content, author=author)
            return redirect('feed')

        return self.get(request)


class CurtirPostView(View):
    """Endpoint que incrementa `likes` no Post e retorna JSON com o novo total."""

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        # Sua lógica de likes
        post.likes = (post.likes or 0) + 1
        post.save()
        return JsonResponse({"likes": post.likes})
    
# ... (LoginView e RegisterView)

class LoginView(View):
    def get(self, request):
        return render(request, 'pages/login.html')

    def post(self, request):
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(self.request, username=username, password=senha)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            return redirect('feed')
        else:
            messages.error(self.request, "Usuário ou senha incorretos.")
            return redirect('login')

class RegisterView(View):
    def get(self, request):
        return render(request, 'pages/register.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')

        if not username or not password or not email or not first_name or not last_name:
            messages.error(request, "Preencha todos os campos.")
            return redirect('register')

        if password2 and password != password2:
            messages.error(request, "As senhas não coincidem.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return redirect('register')

        user = User(username=username, email=email, last_name=last_name, first_name=first_name)
        user.set_password(password)
        user.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('feed')

        messages.success(request, "Cadastro realizado. Faça login.")
        return redirect('login')


@method_decorator(csrf_exempt, name='dispatch')
class PostDetailView(LoginRequiredMixin, View):
    """Mostra o detalhe do post (GET), cria comentário (POST) e permite DELETE."""

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        
        if request.user.is_authenticated:
            user = request.user
            
            # 1. RASTREIA E REGISTRA CADA VISUALIZAÇÃO NO MODELO INTERMEDIÁRIO (N:N)
            PostView.objects.create(
                user=user,
                post=post,
                viewed_at=timezone.now()
            )
            
            # 2. INCREMENTA O CONTADOR TOTAL SIMPLES (views_count)
            Post.objects.filter(id=post_id).update(views_count=F('views_count') + 1)
            
            # 3. Recarrega o objeto 'post' para que ele reflita o novo valor na template.
            post.refresh_from_db() 
        
        comments = post.comments.all().order_by('created_by')
        return render(request, 'pages/post.html', {'post': post, 'comments': comments})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        content = request.POST.get('content')
        author = request.user
        if content and author:
            Comment.objects.create(post=post, author=author, content=content)
            return redirect('post_detail', post_id=post.id)
        return self.get(request, post_id)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        post.delete(hard=False) 
        return JsonResponse({"success": True})