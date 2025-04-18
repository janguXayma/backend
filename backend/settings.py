import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

from corsheaders.defaults import default_headers


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
   # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'authentication',
    'classe',
    'statistic',
    #jwt token
    'pdf_upload',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    #doc
    'drf_yasg',
    #history
    'simple_history',
    # Pour Google
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'exercices',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
]
SIMPLE_HISTORY_USER_MODEL = 'authentication.User'
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Ton front en React
    'http://127.0.0.1:3000',  # Autre variation
    'http://localhost:3000',  # Ton front en React
    'http://127.0.0.1:3000',  # Autre variation
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8000',
]
CORS_ALLOW_CREDENTIALS = True  # Autorise les cookies et l'authentification avec CORS
CORS_ORIGIN_ALLOW_ALL = False  # Ne pas autoriser toutes les origines
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Embedder-Policy',
]

# Entête COOP à ajouter pour permettre une interaction entre différentes fenêtres
CORS_EXPOSE_HEADERS = [
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Embedder-Policy',
]
# settings.py
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = 'require-corp'
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Embedder-Policy',
]

# Entête COOP à ajouter pour permettre une interaction entre différentes fenêtres
CORS_EXPOSE_HEADERS = [
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Embedder-Policy',
]
# settings.py
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = 'require-corp'

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

USE_POSTGRES  = os.getenv('USE_POSTGRES','False').lower() == 'true'
if USE_POSTGRES:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style':'{'
        },
        'style':{
            'format':'{levelname} {message}',
            'style':'{'
        },
    },
    'handlers': {
        'file':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'logs','debug.log'),
            'formatter':'verbose',
        },
        'console': {
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter':'style',
        },
    },
    'loggers':{
        'django':{
            'handlers':['file','console'],
            'level':'DEBUG',
            'propagate':True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

AUTH_USER_MODEL = 'authentication.User'

SITE_ID = 1

SITE_ID = 1

#Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # Authentification par token
        'rest_framework.authentication.SessionAuthentication',  # Aut
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# Configuration AllAuth pour éviter les emails de confirmation
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]


# Permettre l'authentification sociale
REST_USE_JWT = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'FETCH_USERINFO':True,
    }
}


# Configuration AllAuth pour éviter les emails de confirmation
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]


# Permettre l'authentification sociale
REST_USE_JWT = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'FETCH_USERINFO':True,
    }
}



#Token
SIMPLE_JWT = {
    # Durée de vie de l'access token (50 minutes)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    # Durée de vie du refresh token (3 jours)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    
    # Sécurisation de la rotation des refresh tokens
    "ROTATE_REFRESH_TOKENS": True,  # Activez la rotation des tokens de rafraîchissement
    "BLACKLIST_AFTER_ROTATION": True,  # Les tokens de rafraîchissement sont mis en liste noire après utilisation

    # Empêcher la mise à jour du login à chaque utilisation du token
    "UPDATE_LAST_LOGIN": False,

    # Sécuriser l'algorithme
    "ALGORITHM": "HS256",  # Utilisation de HS256 pour une bonne balance entre performance et sécurité

    #sécurité pour vérifier les tokens
    "VERIFYING_KEY": "", 
    "AUDIENCE": None,
    "ISSUER": None,
    "LEEWAY": 0,

    # Authentification via le header Bearer
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    # Configuration des claims
    "USER_ID_FIELD": "id",  # Utilisation de l'ID de l'utilisateur pour identifier
    "USER_ID_CLAIM": "user_id",

    # Configuration pour les tokens de type Access
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",

    # Configuration des serializers
    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.MyTOPS",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
}



# Créer le dossier chiffré au démarrage
import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(os.path.join(MEDIA_ROOT, 'encrypted_exercises'), exist_ok=True)

# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']  # Format des messages acceptés
CELERY_TASK_SERIALIZER = 'json'  # Sérialisation des tâches
CELERY_RESULT_SERIALIZER = 'json'  # Sérialisation des résultats
CELERY_TIMEZONE = 'UTC'  # Fuseau horaire (ajustez selon vos besoins)
CELERY_ENABLE_UTC = True  # Utiliser UTC pour la gestion du temps
# Nombre maximum de tâches simultanées par worker
CELERYD_CONCURRENCY = 4 

# Tâches périodiques (si vous en avez besoin)
CELERY_BEAT_SCHEDULE = {
    'task_name': {
        'task': 'path.to.task',
        'schedule': 10.0,  # Intervalle en secondes
    },
}

# Mode de journalisation des tâches
CELERYD_LOG_COLOR = True  # Coloriser les logs dans la console
CELERYD_LOG_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'  # Format des logs

