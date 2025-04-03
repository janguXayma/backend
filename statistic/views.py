from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Statistic, StatisticStudent, StatisticGlobale
from .serializers import StatisticSerializer, StatisticStudentSerializer, StatisticGlobaleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter 

class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer


class StatisticStudentViewSet(viewsets.ModelViewSet):
    queryset = StatisticStudent.objects.all()
    serializer_class = StatisticStudentSerializer
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['student', 'classe']
    search_fields = ['student__user__username', 'classe__name']
    ordering_fields = ['created_at', 'updated_at']

    @action(detail=False, methods=['get'])
    def get_statistics_by_student(self, request):
        """Récupère les statistiques d'un étudiant spécifique."""
        student_id = request.query_params.get("student_id")
        if not student_id:
            return Response({"error": "Le paramètre 'student_id' est requis."}, status=400)

        statistics = StatisticStudent.objects.filter(student_id=student_id)
        serializer = self.get_serializer(statistics, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Met à jour le score d'un étudiant."""
        statistic = self.get_object()
        new_score = request.data.get("new_score")

        if new_score is None:
            return Response({"error": "Le champ 'new_score' est requis."}, status=400)

        try:
            new_score = float(new_score)
        except ValueError:
            return Response({"error": "Le score doit être un nombre valide."}, status=400)

        statistic.update_statistic(new_score)
        return Response(StatisticStudentSerializer(statistic).data)


class StatisticGlobaleViewSet(viewsets.ModelViewSet):
    queryset = StatisticGlobale.objects.all()
    serializer_class = StatisticGlobaleSerializer
    filter_backends =[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['teacher', 'classe']
    search_fields = ['teacher__user__username', 'classe__name']
    ordering_fields = ['created_at', 'updated_at']
    
    @action(detail=False, methods=['get'])
    def get_statistic_by_class(self,request):
        """Récupère les statistiques globales d'une classe spécifique."""
        classe_id = request.query_params.get("classe_id")
        if not classe_id:
            return Response({"error": "Le paramètre 'classe_id' est requis."}, status=400)

        statistics = StatisticGlobale.objects.filter(classe__id=classe_id)
        serializer = self.get_serializer(statistics, many=True)
        return Response(serializer.data)

