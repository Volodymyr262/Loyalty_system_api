import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# Define get_secret directly
def get_secret(secret_id, backup=None):
    return os.getenv(secret_id, backup)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True

CORS_ALLOWED_ORIGINS = [
    "https://loyaltysystemapi-production.up.railway.app"]

CORS_ALLOW_CREDENTIALS = True  # 🔥 Required if using authentication
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type", "X-CSRFToken"]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # 🚀 Required for Railway HTTPS
SECURE_SSL_REDIRECT = not os.getenv("DISABLE_SSL_REDIRECT_FOR_TESTS", False)

SESSION_COOKIE_SECURE = True  # Secure cookies
CSRF_COOKIE_SECURE = True  # Secure CSRF cookie
APPEND_SLASH = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication using "Token <your-token>"',
        }
    },
    'USE_SESSION_AUTH': False,  # Hide the login/logout buttons
}

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'drf_yasg',
    'loyalty',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
ROOT_URLCONF = 'Loyalty_system.urls'

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

WSGI_APPLICATION = 'Loyalty_system.wsgi.application'

# Database
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# Password validation
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

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Ensure this matches the expected URL path

# This should be the absolute path where `collectstatic` places static files
STATIC_ROOT = os.path.join(Path(__file__).resolve().parent.parent.parent, 'static')

# Extra directories where static files might be collected from
STATICFILES_DIRS = []

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = ['https://loyaltysystemapi-production.up.railway.app']