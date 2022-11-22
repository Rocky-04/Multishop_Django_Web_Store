from .forms import SubscriberEmailForm


def getting_subscribe_email_form(request):
    """
    Form for subscription to news
    """
    subscriber_email_form = SubscriberEmailForm
    return locals()
