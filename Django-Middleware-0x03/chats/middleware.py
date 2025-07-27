import os
from django.http import HttpResponseForbidden
from datetime import datetime
from collections import defaultdict, deque

# Global tracker: {ip: deque of request timestamps}
_request_tracker = defaultdict(lambda: deque(maxlen=5))


class OffensiveLanguageMiddleware:
    """
    Middleware that limits POST requests per IP to 5 per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply rate-limiting only on POST requests (sending messages)
        if request.method == "POST":
            ip = self._get_client_ip(request)
            now = datetime.now()

            # Remove timestamps older than 60 seconds
            while _request_tracker[ip] and now - _request_tracker[ip][0] > timedelta(seconds=60):
                _request_tracker[ip].popleft()

            if len(_request_tracker[ip]) >= 5:
                return HttpResponseForbidden(
                    "Rate limit exceeded: Maximum 5 messages per minute per IP."
                )

            _request_tracker[ip].append(now)

        return self.get_response(request)

    def _get_client_ip(self, request):
        """Extract client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RequestLoggingMiddleware:
    """
    Middleware that logs each request's timestamp, user, and path to requests.log
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # log file will be stored at the project root (same level as manage.py)
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requests.log')

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Append the log entry to requests.log
        with open(self.log_file, "a") as f:
            f.write(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that blocks requests outside 06:00 to 21:00 (6 AM to 9 PM)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # If current time is before 6 AM or 9 PM and later (>=21), block request
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Chat access is allowed only between 6 AM and 9 PM."
            )

        # Otherwise, continue
        return self.get_response(request)

class RolepermissionMiddleware:
    """
    Middleware that checks if the user has the correct role.
    Only admin (is_superuser) or moderator (is_staff) can access.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ["/admin-only/"]  # You can update paths to protect

        # Check if request.path is restricted
        if any(request.path.startswith(path) for path in restricted_paths):
            user = getattr(request, "user", None)
            if not (user and (user.is_staff or user.is_superuser)):
                return HttpResponseForbidden(
                    "You do not have permission to access this resource."
                )

        return self.get_response(request)

