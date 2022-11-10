from .forms import SubscriberEmailForm


def getting_subscribe_email_form(request):
    subscriber_email_form = SubscriberEmailForm
    return locals()
