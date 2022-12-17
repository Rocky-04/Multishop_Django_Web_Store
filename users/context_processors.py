from .forms import SubscriberEmailForm


def get_newsletter_subscription_form_context(request):
    """
    Get a form for subscribing to news.

    This function returns a dictionary containing the `SubscriberEmailForm` form class. This form
    can be used to collect email addresses for subscribing to news updates.

    :param request: The incoming request object.
    :return: A dictionary containing the `SubscriberEmailForm` form class.
    """
    return {
        'SUBSCRIBER_EMAIL_FORM': SubscriberEmailForm,
    }
