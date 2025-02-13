import os

from snp_site.settings.django import BASE_DIR

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {request_id} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {request_id} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "rich.logging.RichHandler",
            "filters": ["request_id"],
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "db_queries.log"),
            "filters": ["request_id"],
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {  # Логирование запросов к базе данных
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
