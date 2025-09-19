from django.db import models

# Create your models here.
class User(models.Model):

    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)

    def str(self):
        return self.username

class Post(models.Model):

    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_by = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def str(self):
        return self.title

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=300, null=False)
    created_by = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def str(self):
        return f"{self.author} comentou no post {self.post}"