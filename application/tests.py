from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.utils.timezone import now

from application.views import postdoc
from application.models import Postdoc


class PostdocTest(TestCase):

    def test_postdoc_url_resolves_postdoc_view(self):
        view = resolve('/postdoc/new')
        self.assertEquals(view.func, postdoc)

    def test_postdoc_status_code(self):
        url = reverse('postdoc')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'postdoc.html')

    def fill_researcher_form(self):
        self.data['research_set-TOTAL_FORMS'] = '1'
        self.data['research_set-INITIAL_FORMS'] = '0'
        self.data['research_set-MAX_NUM_FORMS'] = ''

    def test_new_postdoc(self):
        url = reverse('postdoc')
        self.data = {
            'name': 'Beltrano',
            'email': 'beltrano@exemplo.com',
            'date': now(),
            'action': 'save'
        }
        self.fill_researcher_form()
        self.client.post(url, self.data)
        self.assertEqual(Postdoc.objects.filter(email='beltrano@exemplo.com').count(), 1)

    def test_new_postdoc_wrong_action(self):
        url = reverse('postdoc')
        self.data = {
            'name': 'Fulano',
            'email': 'fulano@exemplo.com',
            'date': now(),
            'action': 'bla'
        }
        self.fill_researcher_form()
        response = self.client.post(url, self.data)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "warning")
        self.assertTrue("Action not available." in message.message)

    def test_postdoc_invalid_form(self):
        url = reverse('postdoc')
        self.data = {
            'name': '',
            'email': 'none@exemplo.com',
            'action': 'save'
        }
        self.fill_researcher_form()
        response = self.client.post(url, self.data)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "warning")
        self.assertTrue("Information not saved." in message.message)
