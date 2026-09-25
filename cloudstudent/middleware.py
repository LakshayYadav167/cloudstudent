import time
import uuid
import logging

logger = logging.getLogger('cloudstudent.request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        
        # We don't log the start of the request to avoid double logging.
        # Just record the start time.
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = round((time.time() - start_time) * 1000, 2)
        
        # Don't log health endpoint to avoid spamming
        if request.path == '/health/':
            return response
            
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'anonymous'
        
        log_data = f"method={request.method} path={request.path} status={response.status_code} duration={duration}ms user={user} request_id={request_id}"
        
        if response.status_code >= 500:
            logger.error(f"Server Error: {log_data}")
        elif response.status_code >= 400:
            logger.warning(f"Client Error: {log_data}")
        else:
            logger.info(f"Request: {log_data}")
            
        response['X-Request-ID'] = request_id
        return response
