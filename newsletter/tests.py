from django.test import TestCase
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse, resolve
from django.utils.timezone import now

from newsletter.views import subscription, unsubscription, previous_issues, newsletter, send_newsletter
from newsletter.models import Subscription, Newsletter


class NewsletterTest(TestCase):
    def setUp(self):
        Subscription.objects.create(email='fulano@exemplo.com', status=True, status_date=now())
        Newsletter.objects.create(number='1')

    def test_subscription_url_resolves_subscription_view(self):
        view = resolve('/newsletter/subscription')
        self.assertEquals(view.func, subscription)

    def test_new_subscription(self):
        url = reverse('subscription')
        self.data = {
            'email': 'beltrano@exemplo.com',
            'status': True,
            'status_date': now(),
        }
        self.client.post(url, self.data)
        new_subscription = Subscription.objects.filter(email='fulano@exemplo.com')
        self.assertEqual(new_subscription.count(), 1)

    def test_subscription_duplicated(self):
        url = reverse('subscription')
        self.data = {
            'email': 'fulano@exemplo.com',
            'status': True,
            'status_date': now(),
        }
        response = self.client.post(url, self.data)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), 'E-mail already registered.')

    def test_previous_issues_url_resolves_previous_issues_view(self):
        view = resolve('/newsletter/previous')
        self.assertEquals(view.func, previous_issues)

    def test_previous_issues_status_code(self):
        url = reverse('previous_issues')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'previous_issues.html')

    def test_newsletter_url_resolves_newsletter_view(self):
        view = resolve('/newsletter/1')
        self.assertEquals(view.func, newsletter)

    def test_newsletter_status_code(self):
        content = Newsletter.objects.first()
        url = reverse('newsletter', args=(content.number,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsletter.html')

    def test_send_newsletter_url_resolves_send_newsletter_view(self):
        view = resolve('/newsletter/1/submit')
        self.assertEquals(view.func, send_newsletter)

    def test_unsubscription_url_resolves_unsubscription_view(self):
        view = resolve('/newsletter/unsubscription')
        self.assertEquals(view.func, unsubscription)

    def test_unsubscription_status_code(self):
        url = reverse('unsubscription')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'unsubscription.html')

    def test_unsubscription(self):
        url = reverse('unsubscription')
        self.data = {
            'email': 'fulano@exemplo.com',
        }
        self.client.post(url, self.data)
        new_unsubscription = Subscription.objects.filter(email='fulano@exemplo.com', status=False)
        self.assertEqual(new_unsubscription.count(), 1)

    def test_unsubscription_email_not_registered(self):
        url = reverse('unsubscription')
        self.data = {
            'email': 'beltrano@exemplo.com',
        }
        response = self.client.post(url, self.data)
        message = list(get_messages(response.wsgi_request))
        self.assertEqual(len(message), 1)
        self.assertEqual(str(message[0]), 'Email not registered. Did you type it correctly?')
