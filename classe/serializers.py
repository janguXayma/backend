from rest_framework import serializers
from .models import Classe
from authentication.models import Student, Teacher
from django.shortcuts import get_object_or_404

class ClasseSerializer(serializers.ModelSerializer):
    teacher = serializers.HiddenField(default = serializers.CurrentUserDefault())
    name = serializers.CharField(required=True)

    class Meta:
        model = Classe
        fields = ['id','name', 'code_activation', 'description', 'students', 'teacher','created_at','updated_at']
        read_only_fields = ('code_activation', 'teacher', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = validated_data.pop('teacher')
        teacher_obj = get_object_or_404(Teacher, user=user)
        return Classe.objects.create(teacher=teacher_obj, **validated_data)
    