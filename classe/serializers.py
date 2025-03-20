from rest_framework import serializers
from .models import Classe
from authentication.models import Student, Teacher

class ClasseSerializer(serializers.Serializer):
    teacher = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Classe
        fields = ['id','name', 'code_activation', 'description', 'students', 'teacher','created_at','updated_at']
        read_only_fields = ('code_activation', 'teacher', 'created_at', 'updated_at')