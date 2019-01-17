from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from .models import Newsletter, Subscription, FacebookHighlight


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


def previous_issues(request, template_name="previous_issues.html"):
    previous_issues_list = Newsletter.objects.all()
    context = {'previous_issues_list': previous_issues_list}
    return render(request, template_name, context)


def newsletter(request, newsletter_number, template_name="newsletter.html"):
    content = Newsletter.objects.get(number=newsletter_number)
    facebook = FacebookHighlight.objects.filter(newsletter=content.pk)
    context = {'content': content, 'facebook': facebook}
    return render(request, template_name, context)
