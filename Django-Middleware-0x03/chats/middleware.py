from datetime import datetime
import os

from django.http import HttpResponseForbidden
from datetime import datetime

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
