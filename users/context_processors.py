from .forms import SubscriberEmailForm


def getting_subscribe_email_form(request):
    """
    Form for subscription to news
    """
    return {
        'SUBSCRIBER_EMAIL_FORM': SubscriberEmailForm,
    }
