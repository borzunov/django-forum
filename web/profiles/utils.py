from hashlib import sha256

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.urls import reverse


def send_activation_email(request, username, email):
    template = loader.get_template('profiles/activation_email.html')
    activation_url = reverse('profiles:activate', kwargs={'username': username}) + \
                     '?hash=' + get_activation_hash(username)
    context = {
        'url': request.build_absolute_uri(activation_url),
        'username': username,
    }
    send_mail('University forum: activating account', template.render(context),
              settings.SERVICE_EMAIL, [email])


def get_activation_hash(username):
    return sha256(('activation:' + username + ':' + settings.SECRET_KEY).encode()).hexdigest()
