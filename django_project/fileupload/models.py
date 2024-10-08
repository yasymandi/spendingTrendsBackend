from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the file to the user who uploaded it
    file = models.FileField(upload_to='uploads/')  # Store the file in the 'uploads/' folder
    upload_date = models.DateTimeField(auto_now_add=True)  # Store the date the file was uploaded

    def __str__(self):
        return f'{self.user.username} - {self.file.name}'
