from datetime import datetime, timedelta
from oauth2_provider.models import Application, AccessToken


def new_app_and_token(user, token):
    app = Application.objects.create(
        user=user,
        redirect_uris='',
        client_type='confidential',
        authorization_grant_type='password',
        name='test app',
        skip_authorization=True
    )

    access_token = AccessToken.objects.create(
        user=user,
        token=token,
        application=app,
        expires=datetime.utcnow() + timedelta(days=1),
        scope='',
    )
    return app, access_token
