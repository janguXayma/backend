from django.shortcuts import render

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ClasseSerializer
from authentication.models import Student, Teacher
from .models import Classe
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

# Create your views here.

class ClasseViewSet(viewsets.ModelViewSet):
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'students','teacher']
    search_fields = ['name', 'code_activation']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

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
            return Response({"detail": "Vous n'avez pas la permission de créer une classe."}, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Seuls les enseignants peuvent modifier une classe"""
        classe = self.get_object()
        if classe.teacher.user != request.user:
            return Response({"detail": "Vous n'avez pas la permission de modifier cette classe."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Empêche la suppression d'une classe si ce n'est pas un enseignant"""
        classe = self.get_object()
        if classe.teacher.user != request.user:
            return Response({"detail": "Vous ne pouvez pas supprimer cette classe."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    

    @action(detail=False, methods=['post'], url_path='join-class')
    def join_class(self, request, *args, **kwargs):
        """Permet à un étudiant de rejoindre une classe en utilisant le code d'activation."""
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "Authentification requise."}, status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.filter(user=user).first()
        if not student:
            return Response({"detail": "Vous devez être un étudiant pour rejoindre une classe."}, status=status.HTTP_403_FORBIDDEN)

        code_activation = request.data.get('code_activation')
        if not code_activation:
            return Response({"detail": "Veuillez fournir un code d'activation."}, status=status.HTTP_400_BAD_REQUEST)

        classe = get_object_or_404(Classe, code_activation=code_activation)

        if classe.students.filter(user=student.user).exists():
            return Response({"message": "Vous êtes déjà inscrit à cette classe."}, status=status.HTTP_200_OK)

        with transaction.atomic():
            classe.students.add(student)
        return Response({"message": f"Étudiant {student.user.username} ajouté à la classe {classe.name}."}, status=status.HTTP_200_OK)
    


    @action(detail=False, methods=['post'], url_path='leave-class')
    def leave_class(self, request, *args, **kwargs):
        """Permet à un étudiant de quitter une classe."""
        user = request.user
        if user.is_anonymous:
            return Response({"detail": "Authentification requise."}, status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.filter(user=user).first()
        if not student:
            return Response({"detail": "Vous devez être un étudiant pour quitter une classe."}, status=status.HTTP_403_FORBIDDEN)

        code_activation = request.data.get('code_activation')
        if not code_activation:
            return Response({"detail": "Veuillez fournir un code d'activation."}, status=status.HTTP_400_BAD_REQUEST)

        classe = get_object_or_404(Classe, code_activation=code_activation)

        if not classe.students.filter(user=student.user).exists():
            return Response({"message": "Vous n'êtes pas inscrit à cette classe."}, status=status.HTTP_200_OK)

        with transaction.atomic():
            classe.students.remove(student)
        return Response({"message": f"Étudiant {student.user.username} est retiré de la classe {classe.name}."}, status=status.HTTP_200_OK)