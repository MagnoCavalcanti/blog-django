from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse
from .models import Post, Comment, User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


class FeedView(LoginRequiredMixin, View):
    """Lista de posts (GET) e criação rápida de post (POST).

    Mantive o comportamento anterior: se o cabeçalho 'HX-Request' estiver
    presente, renderiza o partial `partials/posts.html`.
    """

    def get(self, request):
        posts = Post.objects.all().order_by('-created_by')
        paginator = Paginator(posts, 5)
        page = int(request.GET.get('page', 1))
        posts = paginator.page(page)

        response = {'posts': posts, 'page': page}

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

        # se faltar campos, apenas re-renderiza a lista (poderia mostrar erro)
        return self.get(request)


class CurtirPostView(View):
    """Endpoint que incrementa `likes` no Post e retorna JSON com o novo total."""

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.likes = (post.likes or 0) + 1
        post.save()
        return JsonResponse({"likes": post.likes})
    
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
        comments = post.comments.all().order_by('created_by')
        return render(request, 'pages/post.html', {'post': post, 'comments': comments})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        content = request.POST.get('content')
        author = request.user
        if content and author:
            Comment.objects.create(post=post, author=author, content=content)
            return redirect('post_detail', post_id=post.id)
        # reexibe mesmo que sem criar
        return self.get(request, post_id)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        post.delete(hard=False)  # usando soft delete
        return JsonResponse({"success": True})


# Página de edição do post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'pages/post.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'post_id': self.object.id})

    # Garante que apenas o autor pode editar
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
