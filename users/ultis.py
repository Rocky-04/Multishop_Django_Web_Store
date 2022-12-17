from django.shortcuts import redirect


class AuthorizedUserMixin:
    """
    A mixin for views that checks if the user is authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
