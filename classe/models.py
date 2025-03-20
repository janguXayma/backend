from django.db import models
from authentication.models import Student,Teacher
from .utils import Utils
import uuid

# Create your models here.
class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code_activation = models.CharField(max_length=4, unique=True, 
                                       default=Utils.generate_activation_code,editable=False)
    description = models.TextField(blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='classes', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    
