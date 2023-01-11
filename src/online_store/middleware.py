import logging

from django.contrib import messages
from django.http import HttpResponseServerError
from django.utils.translation import gettext_lazy as _

from online_store.settings import DEBUG

logger = logging.getLogger(__name__)


class SessionAuthenticationMiddleware:
    """
    Middleware that adds a 'user_authenticated' key to the request session.

    If the user is authenticated, the 'user_authenticated' key is set to the
    user's email address. If the user is not authenticated, the 'user_authenticated'
    key is set to the session key.
    """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.session['user_authenticated'] = request.user.email
        else:
            request.session['user_authenticated'] = request.session.session_key
        response = self._get_response(request)
        return response


class ExceptionLoggingMiddleware:
    """
    Middleware that checks and logs exceptions at the top level.

    If the DEBUG flag is set to True, this middleware simply logs the exception
    and displays an error message to the user. If the DEBUG flag is set to False,
    this middleware logs the exception and returns a 500 Internal Server Error
    response to the user.
    """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        logger.error(str(exception) + ' : ' + str(request.user.is_authenticated))
        messages.error(request, _(
            'An error occurred while executing the request. Try again later'))
        if not DEBUG:
            return HttpResponseServerError
