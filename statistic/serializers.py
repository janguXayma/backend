from rest_framework import serializers
from .models import Statistic, StatisticStudent, StatisticGlobale
from django.shortcuts import get_object_or_404
from authentication.models import Teacher
from rest_framework.permissions import IsAuthenticated 


class StatisticStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    classe_name = serializers.CharField(source='classe.name', read_only=True)

    class Meta:
        model = StatisticStudent
        fields = '__all__'
        read_only_fields = ('teacher', 'average_score', 'success_rate', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        teacher_obj = get_object_or_404(Teacher, user=user)

        classe = validated_data.get('classe')
        student = validated_data.get('student')

        if classe.teacher != teacher_obj:
            raise serializers.ValidationError("Cette classe ne vous appartient pas.")

        if not classe.students.filter(user=student.user).exists():
            raise serializers.ValidationError("Cet étudiant n'est pas inscrit dans cette classe.")

        return StatisticStudent.objects.create(**validated_data)  # Supprime 'teacher'



class StatisticGlobaleSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    classe_name = serializers.CharField(source='classe.name', read_only=True)

    class Meta:
        model = StatisticGlobale
        fields = '__all__'
        read_only_fields = ('teacher', 'average_score', 'created_at', 'updated_at')


class StatisticSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    classe_name = serializers.CharField(source='classe.name', read_only=True)

    class Meta:
        model = Statistic
        fields = '__all__'
        read_only_fields = ('teacher', 'success_rate', 'created_at', 'updated_at')
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        teacher_obj = get_object_or_404(Teacher, user=user)
        validated_data['teacher'] = teacher_obj
        return Statistic.objects.create(**validated_data)