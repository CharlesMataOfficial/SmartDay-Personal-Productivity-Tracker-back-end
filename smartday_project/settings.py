# smartday_project/settings.py
from pathlib import Path
import os
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---------------------------------------------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="fallback-secret-for-local")
DEBUG = config("DEBUG", default=False, cast=bool)

# Allow trimming whitespace when splitting env lists
def _split_env_list(name, default=""):
    return [s.strip() for s in config(name, default=default).split(",") if s.strip()]

ALLOWED_HOSTS = _split_env_list("ALLOWED_HOSTS", default="localhost")

# --- APPLICATIONS & MIDDLEWARE ----------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "smartday_app",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # keep this high (before CommonMiddleware)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smartday_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "smartday_app", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "smartday_project.wsgi.application"

# --- DATABASE (Postgres) ----------------------------------------------------
# Prefer a single DATABASE_URL env var (clean & recommended for hosting providers).
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    # If connecting inside Render's private network, include .internal in the host inside DATABASE_URL.
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=False)
    }
else:
    # Fallback to individual DB_* env vars for local dev or if you prefer separate vars.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="postgres"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default=""),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default=5432, cast=int),
        }
    }

# --- AUTH, TIME, STATIC, ETC -----------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files: collectstatic will write into STATIC_ROOT on Render
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS origins (read from env; split by comma)
CORS_ALLOWED_ORIGINS = _split_env_list(
    "CORS_ALLOWED_ORIGINS", default="https://your-frontend.vercel.app"
)
