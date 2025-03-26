# mon_app/serializers.py
from rest_framework import serializers
from .models import Reponse

class ReponseSerializer(serializers.ModelSerializer):
    pdf_file = serializers.FileField()

    class Meta:
        model = Reponse
        fields = ['pdf_file']

    def validate_pdf_file(self, value):
        """ Vérifie que le fichier est bien un PDF """
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Le fichier doit être au format PDF.")
        return value

    def create(self, validated_data):
        # Récupérer l'utilisateur et ajouter dans validated_data
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
