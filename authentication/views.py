from django.shortcuts import render
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTOPS, RegisterSerializer, UserSerializer, TeacherSerializer, StudentSerializer
from .models import User, Student, Teacher, Profile

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTOPS

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #Creer un utilisateur
        user_data = serializer.validated_data
        try:
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                is_student=user_data['role'] == 'Student',
                is_teacher=user_data['role'] == 'Teacher'
            )
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        # Retourner une réponse de succès avec les données de l'utilisateur
        return Response({
            'status': 'User created successfully',
            'user': {
                'email': user.email,
                'role': user_data['role']
            }
        }, status=201)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs authentifiés peuvent accéder

    def get(self, request, *args, **kwargs):
        """
        Retourne les informations du profil de l'utilisateur connecté.
        """
        user = request.user
        try:
            profile = user.profile  # On accède au profil lié à l'utilisateur
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found for this user.'}, status=404)

        user_data = {
            'email': user.email,
            'full_name': profile.full_name,
            'photo': profile.photo.url if profile.photo else None,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'location': profile.location,
            'birth_date': profile.birth_date,
            'gender' : profile.gender
        }

        return Response(user_data, status=200)

