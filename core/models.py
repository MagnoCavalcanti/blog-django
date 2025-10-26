from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import SoftDeletableManager

class SoftDeletableMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = SoftDeletableManager()
    all_objects = models.Manager()

    def delete(self, hard=False):
        if hard:
            return super().delete()
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True



class Post(SoftDeletableMixin, models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_by = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(SoftDeletableMixin, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=300, null=False)
    created_by = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author} comentou no post {self.post}"