from django.db import models
import uuid

class CustomModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class CommonFields(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    master_objects = models.Manager()
    objects = CustomModelManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']