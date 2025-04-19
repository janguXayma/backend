# mon_app/urls.py
from django.urls import path
from .views import UploadPDFAPIView , DownloadDecryptedPDFAPIView , DeletePDFAPIView , PDFToTextAPIView, GetUploadedPDFsAPIView

app_name = 'pdf_upload'

urlpatterns = [
    path('upload_pdf_api/', UploadPDFAPIView.as_view(), name='upload_pdf_api'),
    path('download_pdf/<int:reponse_id>/', DownloadDecryptedPDFAPIView.as_view(), name='download_pdf'),
    path('delete_pdf/<int:reponse_id>/', DeletePDFAPIView.as_view(), name='delete_pdf'),
    path('pdf_to_text/<int:reponse_id>/', PDFToTextAPIView.as_view(), name='pdf_to_text'),
    path('list_uploaded_pdfs/', GetUploadedPDFsAPIView.as_view(), name='list_uploaded_pdfs'),
]
