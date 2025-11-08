import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    Logs request method, path, status code, and processing time.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Record start time
        start_time = time.time()
        
        # Extract request information
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else ""
        client_ip = request.client.host if request.client else "unknown"
        
        # Log incoming request
        logger.info(
            f"Request: {method} {path}"
            f"{f'?{query_params}' if query_params else ''} | "
            f"Client IP: {client_ip}"
        )
        
        # Process the request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log any exceptions that occur
            process_time = time.time() - start_time
            logger.error(
                f"Request failed: {method} {path} | "
                f"Error: {str(e)} | "
                f"Process time: {process_time:.4f}s"
            )
            raise
        
        # Calculate process time
        process_time = time.time() - start_time
        
        # Log response
        status_code = response.status_code
        logger.info(
            f"Response: {method} {path} | "
            f"Status: {status_code} | "
            f"Process time: {process_time:.4f}s"
        )
        
        # Add process time to response headers (optional)
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

