# mon_app/urls.py
from django.urls import path
from .views import UploadPDFAPIView

app_name = 'pdf_upload'

urlpatterns = [
    path('upload_pdf_api/', UploadPDFAPIView.as_view(), name='upload_pdf_api'),
]
