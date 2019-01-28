from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
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
    previous_issues_list = Newsletter.objects.all().order_by('-date')
    context = {'previous_issues_list': previous_issues_list}
    return render(request, template_name, context)


def newsletter(request, newsletter_number, template_name="newsletter.html"):
    content = Newsletter.objects.get(number=newsletter_number)
    facebook = FacebookHighlight.objects.filter(newsletter=content.pk)
    latest_newsletters = Newsletter.objects.filter(number__in=range(int(newsletter_number) - 3, int(newsletter_number)))

    context = {
        'content': content,
        'facebook': facebook,
        'latest_newsletters': latest_newsletters
    }

    return render(request, template_name, context)


@login_required
def send_newsletter(request, newsletter_number):
    if request.method == 'POST':
        content = Newsletter.objects.get(number=newsletter_number)
        facebook = FacebookHighlight.objects.filter(newsletter=content.pk)
        latest_newsletters = Newsletter.objects.filter(number__in=range(
            int(newsletter_number) - 3, int(newsletter_number))
        )

        subject = request.POST['subject']
        from_email = settings.EMAIL_HOST_USER
        to_email = [address['email'] for address in Subscription.objects.all().values('email')]
        html_message = loader.render_to_string(
            'newsletter_content.html',
            {
                'content': content,
                'facebook': facebook,
                'latest_newsletters': latest_newsletters,
                'send_newsletter': True
            }
        )

        if subject and html_message:
            try:
                msg = EmailMessage(subject, html_message, from_email, to_email)
                msg.content_subtype = "html"
                msg.send()
                messages.success(request, _('Newsletter sent successfully.'))
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse("newsletter", args=(content.number,)))
