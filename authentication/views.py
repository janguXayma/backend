from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTOPS, RegisterSerializer, UserSerializer, TeacherSerializer, StudentSerializer
from .models import User, Student, Teacher, Profile
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialToken, SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import status
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTOPS

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # Utilisation de save() directement

        return Response({
            'status': 'User created successfully',
            'user': {
                'email': user.email,
                'username': user.username, 
                'role': 'Student' if user.is_student else 'Teacher' if user.is_teacher else 'User'
            }
        }, status=201)
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
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
    

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        try:
            # Récupérez le token Google depuis le corps de la requête
            token = request.data.get('token')
            if not token or not isinstance(token, str):
                return Response(
                    {"detail": "A valid token string is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Transformez le token en format attendu par allauth
            request.data.update({
                'code': token,  # Utilisez le token comme code
                'id_token': token,  # Ajoutez également le token comme id_token
            })

            # Vérifiez si l'utilisateur existe déjà
            email = request.data.get("email")
            if email:
                accounts = SocialAccount.objects.filter(user__email=email)
                if accounts.count() == 0:
                    # Créez un nouvel utilisateur si aucun n'est trouvé
                    user = User.objects.create_user(email=email, username=email)
                    # Vous pouvez également créer un SocialAccount ici si nécessaire
                elif accounts.count() > 1:
                    return Response(
                        {"detail": "Multiple accounts found for this email. Please use a unique account."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Appelez la méthode parente pour gérer la connexion sociale
            return super().post(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


