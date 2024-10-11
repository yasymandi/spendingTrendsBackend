from django.db import models
from django.contrib.auth.models import User

class ProcessedFile(models.Model):
    file_path = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    transactions_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.file_name
