from django.db import models
from django.contrib.auth.models import User

class ProcessedFile(models.Model):
    file_path = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    processed_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.file_name
