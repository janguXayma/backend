from django.db import models
from authentication.models import Student, Teacher
from classe.models import Classe
import uuid

class Statistic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='statistics')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='statistics')
    total_exercises_submitted = models.PositiveIntegerField(default=0)
    total_exercises_corrected = models.PositiveIntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Recalcule le taux de succès avant chaque sauvegarde."""
        if self.total_exercises_submitted > 0:
            self.success_rate = (self.total_exercises_corrected / self.total_exercises_submitted) * 100
        else:
            self.success_rate = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Statistiques de la classe {self.classe.name} - Enseignant: {self.teacher.user.username}"


class StatisticStudent(models.Model):
    """Statistiques spécifiques à un étudiant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='statistics')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='statistics')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='student_statistics')
    total_exercises_submitted = models.PositiveIntegerField(default=0)
    total_exercises_corrected = models.PositiveIntegerField(default=0)
    score = models.FloatField(default=0.0)
    best_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    success_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        """Met à jour automatiquement les stats à chaque sauvegarde."""
        # Incrémente les totaux uniquement si c'est une nouvelle soumission
        if self._state.adding:
            self.total_exercises_submitted += 1
            self.total_exercises_corrected += 1
        
        # Calcule la moyenne et le taux de succès
        # if self.total_exercises_submitted > 0:
        #     self.average_score = (
        #         (self.average_score * (self.total_exercises_submitted - 1)) + self.score
        #     ) / self.total_exercises_submitted
        #     self.success_rate = (self.total_exercises_corrected / self.total_exercises_submitted) * 100
        
        student_statistics = StatisticStudent.objects.filter(student = self.student,classe = self.classe)
        if student_statistics.exists():
            total_score = student_statistics.aggregate(models.Sum('score'))['score__sum'] or 0
            counts_score = student_statistics.count()
            self.average_score = total_score / counts_score if counts_score > 0 else 0.0
        
        # Met à jour le meilleur score
        max_score = student_statistics.aggregate(models.Max('score'))['score__max']
        self.best_score = max(max_score or 0, self.score)
        
        super().save(*args, **kwargs)
        #Mise a jour du statistiqueGlobale
        statistic_global,created = StatisticGlobale.objects.get_or_create(classe=self.classe,teacher=self.classe.teacher)
        statistic_global.update_statistic()
    def update_statistic(self, new_score):
        """Met à jour les statistiques d'un étudiant."""
        self.total_exercises_submitted += 1
        self.total_exercises_corrected += 1  
        self.average_score = ((self.average_score * (self.total_exercises_submitted - 1)) + new_score) / self.total_exercises_submitted
        self.success_rate = (self.total_exercises_corrected / self.total_exercises_submitted) * 100 
        self.score = new_score
        max_score = StatisticStudent.objects.filter(student=self.student, classe=self.classe).aggregate(models.Max('score'))['score__max']
        self.best_score = max(max_score or 0, new_score)
        self.save()

    def __str__(self):
        return f"Statistiques de l'étudiant {self.student.user.username} - Classe: {self.classe.name}"


class StatisticGlobale(models.Model):
    """Statistiques globales pour une classe."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='global_statistics')
    classe = models.OneToOneField(Classe, on_delete=models.CASCADE, related_name='global_statistics')
    average_score = models.FloatField(default=0.0)
    best_score = models.FloatField(default=0.0)
    top_students = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Calcule la moyenne et le meilleur score avant chaque sauvegarde."""
        # Récupère toutes les statistiques des étudiants de la classe
        student_statistics = StatisticStudent.objects.filter(classe=self.classe)
        
        if student_statistics.exists():
            total_score = sum(stat.score for stat in student_statistics)
            self.average_score = total_score / student_statistics.count()
            self.best_score = max(stat.score for stat in student_statistics)
            top_students = student_statistics.order_by('-score')[:10]
            self.top_students = [
                {"student_name": stat.student.user.username, "score": stat.score}
                for stat in top_students                 
                ]
        else:
            self.average_score = 0.0
            self.best_score = 0.0
            self.top_students = []
        
        super().save(*args, **kwargs)

    def update_statistic(self):
        """Met à jour les statistiques globales de la classe."""
        student_statistics = StatisticStudent.objects.filter(classe=self.classe)
        
        if student_statistics.exists():
            total_score = sum(stat.score for stat in student_statistics)
            self.average_score = total_score / student_statistics.count()
            self.best_score = max(stat.score for stat in student_statistics)
        else:
            self.average_score = 0.0
            self.best_score = 0.0
        
        self.save()

    def __str__(self):
        return f"Statistiques globales de la classe {self.classe.name} - Enseignant: {self.teacher.user.username}"
