# mon_app/serializers.py
from rest_framework import serializers
from .models import Reponse

class ReponseSerializer(serializers.ModelSerializer):
    pdf_file = serializers.FileField()
    student_name = serializers.SerializerMethodField() 

    class Meta:
        model = Reponse
        # fields = ['pdf_file']
        fields = ['id', 'pdf_file', 'uploaded_at', 'student_name']
    
    def get_student_name(self, obj):
        return obj.user.username 

    def validate_pdf_file(self, value):
        """ Vérifie que le fichier est bien un PDF """
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Le fichier doit être au format PDF.")
        max_size = 5 * 1024 * 1024  # 5 Mo
        if value.size > max_size:
            raise serializers.ValidationError("Le fichier ne doit pas dépasser 5 Mo.")

        return value
    
    def create(self, validated_data):
        # Récupérer l'utilisateur et ajouter dans validated_data
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data) 
