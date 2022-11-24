import os

from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
import django

django.setup()


# class Settings(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()


class BasketUrlsTestCase(SimpleTestCase):
    def test_home_url(self):
        assert 1 == 1


class UrlsTestCase(TestCase):
    def test_urls_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_urls_shop(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

    def test_urls_detail(self):
        response = self.client.get(reverse('detail'))
        self.assertEqual(response.status_code, 200)

    def test_urls_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_urls_category(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)

    def test_urls_tag(self):
        response = self.client.get(reverse('tag'))
        self.assertEqual(response.status_code, 200)

    def test_urls_brand(self):
        response = self.client.get(reverse('brand'))
        self.assertEqual(response.status_code, 200)

    def test_urls_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_urls_help(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)

    def test_urls_terms(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)

    def test_urls_search(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_urls_filter(self):
        response = self.client.get(reverse('filter'))
        self.assertEqual(response.status_code, 200)

    def test_urls_skip_filter(self):
        response = self.client.get(reverse('skip_filter'))
        self.assertEqual(response.status_code, 200)

    def test_urls_add_review(self):
        response = self.client.get(reverse('add_review'))
        self.assertEqual(response.status_code, 200)

    def test_urls_send_user_mail(self):
        response = self.client.get(reverse('send_user_mail'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    main()
