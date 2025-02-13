from split_settings.tools import include

settings = [
    "app_settings.py",
    "db_settings.py",
    "django.py",
    "logs.py",
    "rest_framework_settings.py",
]

include(*settings)
