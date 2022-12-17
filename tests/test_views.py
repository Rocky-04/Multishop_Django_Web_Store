import tempfile

from django.db.models import QuerySet
from django.urls import reverse
from modeltranslation.manager import MultilingualQuerySet

from basket.models import ProductInBasket
from favorite.models import Favorite
from news.models import Category
from news.models import News
from orders.forms import CreateOrderForm
from orders.models import GoodsInTheOrder
from orders.models import Order
from orders.models import PaymentMethod
from orders.models import PromoCode
from orders.models import Status
from shop.models import Product
from shop.models import Reviews
from tests.test_settings import Settings
from users.forms import CommunicationForm
from users.forms import PasswordResetForm
from users.forms import SubscriberEmailForm
from users.forms import UpdateUserDataForm
from users.forms import UserLoginForm
from users.forms import UserRegisterForm


class BasketViewsTest(Settings):
    def setUp(self) -> None:
        super().setUp()
        self.context = {"size": self.product.get_default_color_id(),
                        "color": self.product.get_default_size_id(),
                        "count": 5,
                        "current": reverse('basket')}

    def test_views_view_cart(self):
        ProductInBasket.objects.create(product=self.product,
                                       is_active=True,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['products_in_basket']), QuerySet)
        self.assertEqual(len(response.context['products_in_basket']), 1)

    def test_views_basket_add(self):
        count = ProductInBasket.objects.count()
        response = self.client.post(reverse('add_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(count, ProductInBasket.objects.count() - 1)
        self.assertEqual(response.status_code, 200)

    def test_views_basket_remove(self):
        ProductInBasket.objects.create(product=self.product,
                                       is_active=True,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        count = ProductInBasket.objects.count()
        response = self.client.post(reverse('remove_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(count, ProductInBasket.objects.count() + 1)
        self.assertEqual(response.status_code, 200)

    def test_views_edit_cart(self):
        ProductInBasket.objects.create(product=self.product,
                                       is_active=True,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        count = ProductInBasket.objects.count()
        self.assertEqual(ProductInBasket.objects.last().nmb, 1)
        response = self.client.post(reverse('edit_basket', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)

        self.assertEqual(count, ProductInBasket.objects.count())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductInBasket.objects.last().nmb, 5)


class FavoriteViewsTest(Settings):
    def setUp(self):
        super().setUp()
        self.context = {"size": self.product.get_default_color_id(),
                        "color": self.product.get_default_size_id(),
                        "count": 5,
                        "current": reverse('favorite')}

    def test_views_favorite(self):
        Favorite.objects.create(product=self.product,
                                is_active=True,
                                size_id=self.product.get_default_size_id(),
                                color_id=self.product.get_default_color_id())
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['favorites']), QuerySet)
        self.assertEqual(len(response.context['favorites']), 1)

    def test_views_add_favorite(self):
        count = Favorite.objects.count()
        response = self.client.post(reverse('add_favorite', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Favorite.objects.count() - 1)

    def test_views_remove_favorite(self):
        Favorite.objects.create(product=self.product,
                                is_active=True,
                                size_id=self.product.get_default_size_id(),
                                color_id=self.product.get_default_color_id())
        count = Favorite.objects.count()
        response = self.client.post(reverse('remove_favorite', kwargs={'id': self.product.id}),
                                    data=self.context,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Favorite.objects.count() + 1)


class NewsViewsTest(Settings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_news = Category.objects.create(title='Big news',
                                                    slug='big_news')
        cls.news = News.objects.create(title='News 1',
                                       content='content news',
                                       photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                       category=cls.category_news,
                                       slug='news_1')

    def test_views_news(self):
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['news']), MultilingualQuerySet)
        self.assertEqual(len(response.context['news']), 1)

    def test_views_news_category(self):
        response = self.client.get(
            reverse('news_category', kwargs={'slug': self.category_news.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['news']), MultilingualQuerySet)
        self.assertEqual(len(response.context['news']), 1)

    def test_views_news_detail(self):
        response = self.client.get(reverse('news_detail', kwargs={'slug': self.news.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['item']), News)


class OrdersViewsTest(Settings):
    def test_views_checkout(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), CreateOrderForm)

    def test_views_create_order(self):
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)


class UserViewsTest(Settings):
    def test_views_login(self):
        context = {'email': 'roock@gmail.com',
                   'password': 'aaaa12154'}
        response = self.client.post(reverse('login'), data=context, follow=True)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context.get('form')), UserLoginForm)

    def test_views_register(self):
        response = self.client.post(reverse('register'))
        self.assertEqual(response.request['PATH_INFO'], reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context.get('form')), UserRegisterForm)

    def test_views_account(self):
        promo_code = PromoCode.objects.create(title='promo 1',
                                              price=250, )
        payment_method = PaymentMethod.objects.create(title='PayPall')
        status = Status.objects.create(title='Developed')
        order = Order.objects.create(user=self.user,
                                     phone_number='3805000000',
                                     status=status,
                                     payment_method=payment_method,
                                     promo_code=promo_code)
        GoodsInTheOrder.objects.create(
            order=order,
            product=self.product,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['orders']), QuerySet)
        self.assertEqual(len(response.context['orders']), 1)
        self.assertEqual(response.context['orders'][0], order)

    def test_views_account_data(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context.get('form')), UpdateUserDataForm)

    def test_views_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.context['user'], self.user)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('home'))
        self.assertTrue(response.context['user'].is_anonymous)

    def test_views_password_reset(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('password_reset'))
        self.assertEqual(type(response.context.get('form')), PasswordResetForm)

    def test_views_subscriber_email(self):
        response = self.client.get(reverse('subscriber_email'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('subscriber_email'))
        self.assertEqual(type(response.context.get('form')), SubscriberEmailForm)

    def test_views_my_product_review(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_product_review'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('reviews')), 1)
        self.assertEqual(response.context.get('reviews')[0], self.review)

    def test_views_communication(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('communication'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context.get('form')), CommunicationForm)
        self.assertEqual(response.request['PATH_INFO'], reverse('communication'))


class ShopViewsTest(Settings):
    def test_views_home(self):
        Favorite.objects.create(product=self.product,
                                is_active=True,
                                size_id=self.product.get_default_size_id(),
                                color_id=self.product.get_default_color_id())

        ProductInBasket.objects.create(product=self.product,
                                       is_active=True,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['category']), 1)
        self.assertEqual(response.context['PRODUCTS_BASKET_NMB'], 1)
        self.assertEqual(response.context['PRODUCTS_BASKET_LIST'][0], 1)
        self.assertEqual(response.context['PRODUCTS_FAVORITE_LIST'][0], 1)
        self.assertEqual(response.context['PRODUCTS_FAVORITE_NMB'], 1)

    def test_views_shop(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), MultilingualQuerySet)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], None)

    def test_views_detail(self):
        response = self.client.get(reverse('detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['context']), Product)
        self.assertEqual(response.context['active_color'].pk, self.color.pk)
        self.assertEqual(response.context['active_size'].pk, self.size.pk)
        self.assertEqual(response.context['context'], self.product)

    def test_views_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_views_category(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), list)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], 1)

    def test_views_tag(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), list)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], False)

    def test_views_brand(self):
        response = self.client.get(reverse('brand', kwargs={'slug': self.manufacturer.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), list)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], False)

    def test_views_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_views_help(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)

    def test_views_terms(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)

    def test_views_search(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_views_filter(self):
        response = self.client.get(reverse('filter'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), MultilingualQuerySet)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], None)
        self.assertEqual(len(response.context['product_list_pk']), 1)
        self.assertEqual(response.context['color_filter'][0], self.color)
        self.assertEqual(response.context['size_filter'][0], self.size)
        self.assertEqual(response.context['manufacturer_filter'][0], self.manufacturer)

    def test_views_skip_filter(self):
        response = self.client.get(reverse('skip_filter'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['product_list']), MultilingualQuerySet)
        self.assertEqual(len(response.context['product_list']), 1)
        self.assertEqual(response.context['parent'], None)
        self.assertEqual(len(response.context['product_list_pk']), 1)

    def test_views_add_review(self):
        Reviews.objects.all().delete()
        count = Reviews.objects.count()
        self.client.force_login(self.user)
        context = {"text": "All right",
                   "rating": Reviews.RATINGS[1][0],
                   "product_id": self.product.id,
                   "current": reverse('home')}
        response = self.client.post(reverse('add_review'), data=context, follow=True)
        count = Reviews.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, 200)

    def test_views_send_user_mail(self):
        context = {'name': 'Valerii',
                   'email': 'Zaluzhnyi',
                   'subject': 'ZSU',
                   'message': 'Slava ZSU'}
        response = self.client.post(reverse('send_user_mail'), data=context)
        self.assertEqual(response.status_code, 200)

    def test_views_custom_page_not_found_view(self):
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 404)
