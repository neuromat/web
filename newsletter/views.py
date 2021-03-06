from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from mezzanine.conf import settings
from mezzanine.utils.views import paginate
from .models import Newsletter, Subscription, FacebookHighlight


def subscription(request,  template_name="subscription.html"):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            contact = Subscription.objects.get(email=email)
        except Subscription.DoesNotExist:
            contact = False

        if contact and contact.status is True:
            messages.warning(request, _('E-mail already registered.'))
        elif contact and contact.status is False:
            contact.status = True
            contact.save()
            messages.success(request, _('Email registered successfully.'))
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

    return render(request, template_name)


def unsubscription(request, template_name="unsubscription.html"):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            contact = Subscription.objects.get(email=email)
        except Subscription.DoesNotExist:
            contact = False

        if contact and contact.status is True:
            contact.status = False
            contact.status_date = now()
            contact.save()
            messages.success(request, _('Email removed successfully.'))
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.warning(request, _('Email not registered. Did you type it correctly?'))
            return HttpResponseRedirect(reverse('unsubscription'))

    return render(request, template_name)


def previous_issues(request, template_name="previous_issues.html"):
    previous_issues_list = Newsletter.objects.all().order_by('-date')
    previous_issues_list = paginate(previous_issues_list, request.GET.get("page", 1),
                                    settings.BLOG_POST_PER_PAGE, settings.MAX_PAGING_LINKS)
    context = {'previous_issues_list': previous_issues_list}
    return render(request, template_name, context)


def newsletter_content(newsletter_number):
    """Function to get the info about a specific newsletter"""
    content = Newsletter.objects.get(number=newsletter_number)
    facebook = FacebookHighlight.objects.filter(newsletter=content.pk).order_by('-date')
    latest_newsletters = Newsletter.objects.filter(
        number__in=range(int(newsletter_number) - 3, int(newsletter_number))
    ).order_by('-number')

    return content, facebook, latest_newsletters


def newsletter(request, newsletter_number, template_name="newsletter.html"):
    content, facebook, latest_newsletters = newsletter_content(newsletter_number)

    context = {
        'content': content,
        'facebook': facebook,
        'latest_newsletters': latest_newsletters
    }

    return render(request, template_name, context)


@login_required
def send_newsletter(request, newsletter_number):
    if request.method == 'POST':
        content, facebook, latest_newsletters = newsletter_content(newsletter_number)
        subject = request.POST['subject']
        from_email = settings.EMAIL_HOST_USER

        if request.POST['test_newsletter'] == '':
            to_email = settings.EMAIL_TO
        else:
            to_email = request.POST['test_newsletter']

        html_message = loader.render_to_string(
            'send_newsletter.html',
            {
                'content': content,
                'facebook': facebook,
                'latest_newsletters': latest_newsletters,
                'domain': request.get_host()
            }
        )

        text_message = strip_tags(html_message)

        if subject and to_email:
            try:
                msg = EmailMultiAlternatives(subject, text_message, from_email, bcc=[to_email])
                msg.attach_alternative(html_message, "text/html")
                msg.send()
                messages.success(request, _('Newsletter sent successfully.'))
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))

            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse("newsletter", args=(content.number,)))
