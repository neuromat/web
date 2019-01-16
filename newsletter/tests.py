from django.test import TestCase
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse, resolve
from django.utils.timezone import now

from newsletter.views import subscription
from newsletter.models import Subscription


class NewsletterTest(TestCase):
    def setUp(self):
        Subscription.objects.create(email='fulano@exemplo.com', status=True, status_date=now())

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
