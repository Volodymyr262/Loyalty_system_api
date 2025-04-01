import os
from pathlib import Path
import dj_database_url

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Function to get secrets from environment variables
def get_secret(secret_id, backup=None):
    return os.getenv(secret_id, backup)

# Security Settings
SECRET_KEY = get_secret('SECRET_KEY')
DEBUG = False  # Set to False in production

# Allowed Hosts (Use explicit domains instead of '*')
ALLOWED_HOSTS = [
    "loyaltysystemapi-production.up.railway.app"
]
USE_X_FORWARDED_HOST = True

# ✅ Fix CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://loyaltysystemapi-production.up.railway.app"
]
CORS_ALLOW_CREDENTIALS = True  # 🔥 Required if using authentication
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type", "X-CSRFToken"]

# ✅ CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://loyaltysystemapi-production.up.railway.app"
]

# Installed Apps
INSTALLED_APPS = [
    "corsheaders",
    "drf_yasg",
    "loyalty",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # 🔥 Railway best practice

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ✅ Fix Swagger UI Settings
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "DEFAULT_MODEL_RENDERING": "example",
    "DEFAULT_API_URL": "https://loyaltysystemapi-production.up.railway.app/api/",  # 🔥 Ensure this is correct
}

# Database Configuration
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
