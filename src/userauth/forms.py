import logging

from django.conf import settings
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.forms import PasswordResetForm

from notifications_python_client.notifications import NotificationsAPIClient

logger = logging.getLogger(__name__)


class SigninForm(forms.Form):
    email = forms.CharField(label=_('Email address'), max_length=100)
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.PasswordInput
    )


class UserPasswordReset(PasswordResetForm):

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None):
        """
        Uses govuk notify to deliver email providing a link for the user to
        reset their password.
        """
        if not settings.NOTIFY_APIKEY:
            return

        notifications_client = NotificationsAPIClient(settings.NOTIFY_APIKEY)

        # TODO: We should look up the template IDs from configuration
        # somewhere.
        template_id = '22afa457-ee83-4af2-aab7-db5299f54b6b'

        del context['user']
        del context['email']
        context['uid'] = context['uid'].decode("utf-8")

        try:
            notifications_client.send_email_notification(
                email_address=to_email,
                template_id=template_id,
                personalisation=context,
                reference=None
            )
        except Exception as e:
            logger.exception(e)
            raise e
