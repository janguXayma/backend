from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ReponseSerializer
from .models import Reponse

class UploadPDFAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Auth obligatoire

    def post(self, request, format=None):
        serializer = ReponseSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Fichier soumis avec succès !"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"message": "Une erreur s'est produite.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

