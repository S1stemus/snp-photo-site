REST_FRAMEWORK = {       
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', 
    'EXCEPTION_HANDLER': 'utils.exception_handler.drf_exception_response',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),  
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.custom_pagination.CustomPagination',  
    'PAGE_SIZE': 2
    
}