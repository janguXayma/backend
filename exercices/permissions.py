from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher

class IsExerciseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user