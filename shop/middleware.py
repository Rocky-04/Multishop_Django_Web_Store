import logging

from django.contrib import messages
from django.http import HttpResponseServerError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class CheckAuthenticationMiddleware:
    """
    Adds 'user_authenticated' key to request.session.
    If user is authorized by key = email else key = session_key
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


class CheckExceptionMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        logger.error(exception + ' : ' + request.user.is_authenticated)
        messages.error(request, _(
            'An error occurred while executing the request. Try again later'))
        return HttpResponseServerError
