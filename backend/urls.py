from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestion des Exercices",
        default_version='v1',
        description="API pour la gestion des exercices pédagogiques",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@votre-domaine.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentification
    path('api/v1/auth/', include('authentication.urls')),
    
    # Classes
    path('api/v1/classes/', include('classe.urls')),
    
    # Exercices (versionnée comme les autres APIs)
    path('api/v1/exercises/', include('exercices.urls')),
    
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)