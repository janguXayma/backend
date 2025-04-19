from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions 
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ReponseSerializer
from .models import Reponse
import os

class UploadPDFAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Auth obligatoire

    def post(self, request, format=None):
        serializer = ReponseSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            instance = serializer.save()  # On récupère l'instance créée
            response_data = ReponseSerializer(instance).data  # On la re-sérialise pour inclure l'ID
            response_data["message"] = "Fichier soumis avec succès !"
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(
            {"message": "Une erreur s'est produite.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class GetUploadedPDFsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uploads = Reponse.objects.all().order_by('-uploaded_at') 
        serializer = ReponseSerializer(uploads, many=True)
        return Response(serializer.data)


class DownloadDecryptedPDFAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, reponse_id, format=None):
       
        reponse = get_object_or_404(Reponse, id=reponse_id)
        """Télécharge le PDF avec un chiffré"""
        pdf_content = reponse.get_encrypted_pdf() 
        if pdf_content is None:
            return JsonResponse({"error": "Fichier introuvable ou erreur de déchiffrement."}, status=404)

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{reponse.get_decrypted_pdf_name()}"' 
        return response
    
class DeletePDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, reponse_id, format=None):
        """
        API permettant de supprimer un fichier PDF associé à une réponse donnée.
        """
        reponse = get_object_or_404(Reponse, id=reponse_id)

        if reponse.delete_pdf():
            return JsonResponse({"message": "PDF supprimé avec succès."}, status=200)
        else:
            return JsonResponse({"error": "Aucun fichier à supprimer."}, status=404)
        

class PDFToTextAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reponse_id, format=None):
        """Extrait le texte d'un PDF et retourne son contenu en .txt"""
        reponse = get_object_or_404(Reponse, id=reponse_id)
        
        text_file_path = reponse.pdf_to_text()
        if not text_file_path or not os.path.exists(text_file_path):
            return JsonResponse({"error": "Impossible d'extraire le texte du PDF."}, status=400)

        # Lire le contenu du fichier texte
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        response = HttpResponse(text_content, content_type="text/plain")
        response['Content-Disposition'] = f'attachment; filename="{reponse.get_decrypted_pdf_name()}_extracted.txt"'
        return response
