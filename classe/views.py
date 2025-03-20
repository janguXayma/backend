from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ClasseSerializer
from authentication.models import Student, Teacher
from .models import Classe
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Create your views here.

class ClasseViewSet(viewsets.ModelViewSet):
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retourne les classes du professeur connecté ou celles auxquelles l'étudiant appartient"""
        
        user  = self.request.user

        if Teacher.objects.filter(user=user).exists():
            return Classe.objects.filter(teacher__user=user)
        
        elif Student.objects.filter(user=user).exists():
            return Classe.objects.filter(students__user=user)
        
        return Classe.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Seuls les enseignants peuvent créer une classe"""
        if not Teacher.objects.filter(user=request.user).exists():
            return Response({"detail": "Vous n'avez pas la permission de créer une classe."}, status=403)
        
        return super().create(request, *args, **kwargs)
    

    def join_class(self, request, *args, **kwargs):
        """Permet à un étudiant de rejoindre une classe en utilisant le code d'activation"""
        code_activation = request.data.get('code_activation')
        user = request.user
        student = get_object_or_404(Student, user=user)
        
        try:
            classe = get_object_or_404(Classe, code_activation=code_activation)
        except Classe.DoesNotExist:
            return Response({"detail": "Classe non trouvée."}, status=404)

        if student in classe.students.all():
            return Response({"message": "Vous êtes déjà inscrit à cette classe."}, status=200)

        classe.students.add(student)
        return Response({"message": f"Étudiant {student} ajouté à la classe {classe}."}, status=200)
    


    