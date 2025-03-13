from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Champs pour differencier les roles
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='api_user_groups',  # Nom personnalisé
        related_query_name='api_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='api_user_permissions',  # Nom personnalisé
        related_query_name='api_user',
    )

    def __str__(self):
        return self.email
    
#Modele Etudiant
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='student')
    grade = models.CharField(max_length=50, blank=True, null=True)
    class_level = models.CharField(max_length=100,blank=True, null=True)
    enrollment_year = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.email} - Etudiant"
    
#Modele Enseignant
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='teacher')
    department = models.CharField(max_length=255, blank=True, null=True)
    expertise = models.TextField(blank=True, null=True)
    office_number = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.email} - Enseignant"
    

# Modele Profil Utilisateur
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.user.email}"
    
# Signal pour creer un profil utilisateur apres la creation d'un utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.is_student:
            student = Student.objects.create(user=instance)
            student.grade = "Grade a definir"
            student.class_level = "Niveau a definir"
            student.enrollment_year = None
            student.save()
        elif instance.is_teacher:
            teacher = Teacher.objects.create(user=instance)
            teacher.department = "Département à définir"
            teacher.expertise = "Expertise à définir"
            teacher.office_number = "Bureau à définir"
            instance.profile.save()


