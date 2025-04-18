from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Exercise
from .serializers import ExerciseSerializer
from .permissions import IsTeacher, IsExerciseOwner
from django.db.models import Count
from django.utils import timezone
from django.core.exceptions import ValidationError
import os


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    # permission_classes = [IsAuthenticated, IsTeacher]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Filtre les exercices par utilisateur et statut de publication"""
    #     queryset = super().get_queryset()

    #     # Filtre supplémentaire pour les requêtes GET
    #     if self.request.method == 'GET':
    #         is_published = self.request.query_params.get('published')
    #         if is_published in ['true', 'false']:
    #             queryset = queryset.filter(is_published=is_published == 'true')

    #     if not self.request.user.is_staff:
    #         queryset = queryset.filter(created_by=self.request.user)

    #     return queryset
    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_staff:
            return queryset.filter(created_by=self.request.user)

        return queryset.filter(is_published=True)


    def perform_create(self, serializer):
        """Validation de la date limite avant sauvegarde"""
        due_date = serializer.validated_data.get('due_date', None)

        if due_date and due_date < timezone.now():
            raise ValidationError(
                {"due_date": "La date limite doit être dans le futur"},
                code=status.HTTP_400_BAD_REQUEST
            )

        # Sauvegarde avec l'utilisateur courant comme créateur
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Endpoint pour télécharger le PDF chiffré"""
        exercise = self.get_object()

        if not exercise.pdf_file:
            return Response(
                {"detail": "Aucun fichier PDF associé"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            response = Response()
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(exercise.pdf_file.name)}"'
            response['X-Accel-Redirect'] = exercise.pdf_file.url  # Pour Nginx
            return response
        except FileNotFoundError:
            return Response(
                {"detail": "Fichier PDF introuvable"},
                status=status.HTTP_410_GONE
            )

    @action(detail=False, methods=['get'])
    def upcoming_deadlines(self, request):
        """Liste des exercices avec date limite approchante"""
        upcoming = self.get_queryset().filter(
            due_date__gte=timezone.now(),
            due_date__lte=timezone.now() + timezone.timedelta(days=3)
        ).order_by('due_date')

        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


class ExerciseStatsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        """Statistiques améliorées avec dates limites"""
        stats = {
            'total': Exercise.objects.count(),
            'published': Exercise.objects.filter(is_published=True).count(),
            'expired': Exercise.objects.filter(due_date__lt=timezone.now()).count(),
            'by_type': Exercise.objects.values('exercise_type')
            .annotate(count=Count('id')),
            'next_deadline': Exercise.objects.filter(due_date__gte=timezone.now())
                             .order_by('due_date')
                             .values('title', 'due_date')[:3]
        }
        return Response(stats)