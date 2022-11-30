from django.urls import reverse
from django.utils.translation import activate

from tests.test_settings import Settings


class UrlsShopTestCase(Settings):

    def test_urls_home(self):
        response = self.client.get(reverse('home'))
        print(response.request['PATH_INFO'])

        self.assertEqual(response.status_code, 200)

        with self.subTest("Language UA"):
            activate('uk')
            response = self.client.get(reverse('home'))
            print(response.request['PATH_INFO'])

            self.assertEqual(response.status_code, 200)

    def test_urls_shop(self):
        response = self.client.get(reverse('shop'))
        print(response.request['PATH_INFO'])
        self.assertEqual(response.status_code, 200)

    def test_urls_detail(self):
        response = self.client.get(reverse('detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)

    def test_urls_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_urls_category(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    def test_urls_tag(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag.slug}))
        self.assertEqual(response.status_code, 200)

    def test_urls_brand(self):
        response = self.client.get(reverse('brand', kwargs={'slug': self.manufacturer.slug}))
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
        from shop.models import Reviews
        self.client.force_login(self.user)
        context = {"text": "All right",
                   "rating": Reviews.RATINGS[1],
                   "product_id": self.product.id,
                   "current": reverse('home')}
        response = self.client.post(reverse('add_review'), data=context, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_send_user_mail(self):
        response = self.client.get(reverse('send_user_mail'))
        self.assertEqual(response.status_code, 200)


class UrlsBasketTestCase(Settings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.context = {"size": cls.product.get_default_color_id(),
                       "color": cls.product.get_default_size_id(),
                       "count": 5,
                       "current": reverse('basket')}


    def test_urls_basket(self):
        response = self.client.get(reverse('basket'))
        print(self.context)
        self.assertEqual(response.status_code, 200)

    def test_urls_add_basket(self):
        self.client.force_login(self.user)
        print(self.context)
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
        from basket.models import ProductInBasket
        ProductInBasket.objects.create(product=self.product,
                                       is_active=True,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        response = self.client.post(reverse('edit_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)


class UrlsFavoriteTestCase(Settings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.context = {"size": cls.product.get_default_color_id(),
                       "color": cls.product.get_default_size_id(),
                       "count": 5,
                       "current": reverse('favorite')}

    def test_urls_favorite(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 200)

    def test_urls_add_favorite(self):
        response = self.client.post(reverse('add_favorite', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_remove_favorite(self):
        from favorite.models import Favorite
        Favorite.objects.create(user_authenticated=self.user.email,
                                product=self.product,
                                is_active=True,
                                size_id=self.product.get_default_size_id(),
                                color_id=self.product.get_default_color_id())
        response = self.client.post(reverse('remove_favorite', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)

        self.assertEqual(response.status_code, 200)


class UserTestCase(Settings):
    def test_urls_login(self):
        response = self.client.post(reverse('login'),
                                    data={'username': 'roock@gmail.com', "password": 'aaaa12154'},
                                    )
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_urls_register(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'roock2@gmail.com', "password": 'aaaa12154'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_account(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_urls_account_data(self):
        response = self.client.get(reverse('account_data'))
        self.assertEqual(response.status_code, 200)

    def test_urls_logout(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_urls_subscriber_email(self):
        response = self.client.get(reverse('subscriber_email'))
        self.assertEqual(response.status_code, 200)

    def test_urls_my_product_review(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('my_product_review'), follow=True)
        print(response.request)
        print(response.request)
        print(self.client)
        self.assertEqual(response.status_code, 200)

    def test_urls_communication(self):
        response = self.client.get(reverse('communication'))
        self.assertEqual(response.status_code, 200)
