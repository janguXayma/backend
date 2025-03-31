from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatisticViewSet,StatisticGlobaleViewSet,StatisticStudentViewSet

router = DefaultRouter()
router.register(r'statistics', StatisticViewSet)
router.register(r'statistic-students', StatisticStudentViewSet, basename='statisticstudent') 
router.register(r'statistic-globales', StatisticGlobaleViewSet, basename='statisticglobale')

urlpatterns = [
    path('', include(router.urls)),
]
