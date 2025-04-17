from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User, Student, Teacher, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import models
from allauth.socialaccount.models import SocialAccount

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password','is_student', 'is_teacher']
        extra_kwargs = {
            'password': {'write_only': True}
        }

#Serialiseur pour l_etudiant
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['user']

#Serialiseur pour le professeur

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher

#Serialiseur pour le profile utilisateur

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    email = serializers.EmailField(source="user.email", required=False)
    username = serializers.CharField(source="user.username", required=False)
    password = serializers.CharField(source="user.password", write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'email', 'username', 'password', 'full_name', 'photo', 'bio', 'phone_number', 'location', 'birth_date', 'gender']  # Ajout de "password"

    def update(self, instance, validated_data):
        """
        Mise à jour du profil et de l'utilisateur lié.
        """
        user_data = validated_data.pop('user', {})
        
        # Mise à jour des données du profil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mise à jour des informations de l'utilisateur
        user = instance.user
        if 'email' in user_data:
            user.email = user_data['email']
        if 'username' in user_data:
            user.username = user_data['username']
        if 'password' in user_data:
            user.set_password(user_data['password'])  # Hacher le mot de passe
        user.save()

        return instance


#Serialiseur pour le token JWT

class MyTOPS(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'is_student': self.user.is_student,
            'is_teacher': self.user.is_teacher,
        }
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.profile.full_name
        token['email'] = user.email
        token['username'] = user.username
        token['bio'] = user.profile.bio
        token['phone_number'] = user.profile.phone_number
        token['location'] = user.profile.location
        # token['birth_date'] = user.profile.birth_date
        token['role'] = 'student' if user.is_student else 'teacher' if user.is_teacher else 'user'
        token['gender'] = user.profile.gender
        return token
    
# Serialiseur pour l'inscription
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.ChoiceField(choices=['Student', 'Teacher'])

    def validate_password(self, value):
        validate_password(value)
        return value
    
    #Verifier si les deux password sont exactes
    def validate(self, data):
        if data['password']!= data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data
    
    #Creer un utilisateur en fonction de son profile
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        email = validated_data['email']
        username = email.split('@')[0]

        user = User.objects.create_user(
            email=email,
            username=username, 
            password = validated_data['password'],
            is_student = validated_data['role'] == 'Student',
            is_teacher = validated_data['role'] == 'Teacher'
        )
        return user


