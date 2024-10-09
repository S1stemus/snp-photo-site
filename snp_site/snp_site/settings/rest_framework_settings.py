REST_FRAMEWORK = {       
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', 
    'EXCEPTION_HANDLER': 'utils.exception_handler.drf_exception_response',
}