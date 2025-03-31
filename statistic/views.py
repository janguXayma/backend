from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Statistic, StatisticStudent, StatisticGlobale
from .serializers import StatisticSerializer, StatisticStudentSerializer, StatisticGlobaleSerializer

class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer


class StatisticStudentViewSet(viewsets.ModelViewSet):
    queryset = StatisticStudent.objects.all()
    serializer_class = StatisticStudentSerializer

    @action(detail=False, methods=['get'])
    def get_statistics_by_student(self, request):
        """Récupère les statistiques d'un étudiant spécifique."""
        student_id = request.query_params.get("student_id")
        if not student_id:
            return Response({"error": "Le paramètre 'student_id' est requis."}, status=400)

        statistics = StatisticStudent.objects.filter(student__id=student_id)
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
