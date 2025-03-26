from django.db import models

# Create your models here.

# mon_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def upload_pdf_path(instance, filename):
    # Permet de stocker les fichiers dans un dossier spécifique par utilisateur.
    return f'pdf_uploads/{instance.user.username}/{filename}'

class Reponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=upload_pdf_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pdf_file.name}"

