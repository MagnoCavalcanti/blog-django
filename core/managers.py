from django.db import models
from django.utils import timezone

class SoftDeletableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)