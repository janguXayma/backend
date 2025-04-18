from rest_framework import serializers
from .models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Exercise
        fields = [
            'id', 'title', 'description', 'exercise_type',
            'pdf_file', 'pdf_url', 'created_at', 'created_by',
            'is_published'
        ]
        read_only_fields = ['created_by', 'created_at']
        extra_kwargs = {
            'pdf_file': {'write_only': True}
        }

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None