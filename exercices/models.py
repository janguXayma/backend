from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

def encrypted_file_path(instance, filename):
    """Génère un chemin de fichier chiffré avec UUID"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"  # Nom aléatoire
    return os.path.join('encrypted_exercises', filename)

class Exercise(models.Model):
    class ExerciseType(models.TextChoices):
        SQL = 'SQL', 'Exercice SQL'
        THEORY = 'THEORY', 'Question théorique'
        DESIGN = 'DESIGN', 'Modélisation'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    exercise_type = models.CharField(
        max_length=10,
        choices=ExerciseType.choices,
        default=ExerciseType.SQL
    )
    pdf_file = models.FileField(
        upload_to=encrypted_file_path,  # Chemin chiffré
        verbose_name="Fichier PDF chiffré"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    due_date = models.DateTimeField(
        verbose_name="Date limite de soumission",
        default=timezone.now() + timezone.timedelta(days=7)  # 7 jours par défaut
    )

    class Meta:
        ordering = ['-created_at']
        permissions = [
            ("download_encrypted", "Peut télécharger les fichiers chiffrés"),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_exercise_type_display()})"

    def clean(self):
        """Validation de la date limite"""
        if hasattr(self, 'due_date') and self.due_date < timezone.now():
            raise ValidationError("La date limite doit être dans le futur")