from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from .models import Subscription


def subscription(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Subscription.objects.filter(email=email).exists():
            messages.warning(request, _('E-mail already registered.'))
        else:
            new_email = Subscription.objects.create(
                email=email,
                status=True,
                status_date=now()
            )
            new_email.save()
            messages.success(request, _('Email registered successfully.'))

        redirect_url = reverse('home')
        return HttpResponseRedirect(redirect_url)
