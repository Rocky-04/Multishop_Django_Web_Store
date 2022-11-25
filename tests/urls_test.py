from django.urls import reverse

from tests.settings_test import Settings


class UrlsShopTestCase(Settings):
    def test_urls_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_urls_shop(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

    def test_urls_detail(self):
        response = self.client.get(reverse('detail', kwargs={'slug': 'mini_bag'}))
        self.assertEqual(response.status_code, 200)

    def test_urls_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_urls_category(self):
        response = self.client.get(reverse('category', kwargs={'slug': 'bags'}))
        self.assertEqual(response.status_code, 200)

    def test_urls_tag(self):
        response = self.client.get(reverse('tag', kwargs={'slug': 'sale'}))
        self.assertEqual(response.status_code, 200)

    def test_urls_brand(self):
        response = self.client.get(reverse('brand', kwargs={'slug': 'zara'}))
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
        self.assertEqual(response.status_code, 405)

    def test_urls_send_user_mail(self):
        response = self.client.get(reverse('send_user_mail'))
        self.assertEqual(response.status_code, 200)


class UrlsBasketTestCase(Settings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.context = {"size": cls.product.get_title_color_id,
                       "color": cls.product.get_title_size_id,
                       "count": 5,
                       "current": reverse('basket')}

    def test_urls_basket(self):
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)

    def test_urls_add_basket(self):
        response = self.client.post(reverse('add_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_remove_basket(self):
        response = self.client.post(reverse('remove_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)

        self.assertEqual(response.status_code, 200)

    def test_urls_edit_basket(self):
        response = self.client.post(reverse('edit_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
