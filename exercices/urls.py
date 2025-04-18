from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ExerciseStatsView

router = DefaultRouter()
router.register(r'', ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', ExerciseStatsView.as_view(), name='exercise-stats'),
]