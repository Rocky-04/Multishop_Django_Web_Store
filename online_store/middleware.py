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
