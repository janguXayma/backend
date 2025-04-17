from django.db import models
from authentication.models import Student,Teacher
import uuid
import random
import string
from simple_history.models import HistoricalRecords


def generate_activation_code():
    """Generate a random activation code of 4 characters."""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if not Classe.objects.filter(code_activation=code).exists():
            return code
        
# Create your models here.
class Classe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,blank=False, null=False)
    code_activation = models.CharField(max_length=4, unique=True, 
                                       default=generate_activation_code,editable=False)
    description = models.TextField(blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='classes', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.name

    
