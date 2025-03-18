# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User, Student, Teacher, Profile

# # Configuration personnalisée pour le modèle User
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'username', 'is_student', 'is_teacher', 'is_active', 'is_staff', 'date_joined')
#     list_filter = ('is_student', 'is_teacher', 'is_active', 'is_staff')
#     search_fields = ('email', 'username')
#     ordering = ('email',)
    
#     # Formulaire d'édition de l'utilisateur
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'full_name')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_student', 'is_teacher', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2', 'is_student', 'is_teacher')
#         }),
#     )

# # Enregistrement du modèle User avec la configuration personnalisée
# admin.site.register(User, CustomUserAdmin)

# # Enregistrement des autres modèles
# admin.site.register(Student)
# admin.site.register(Teacher)
# admin.site.register(Profile)
