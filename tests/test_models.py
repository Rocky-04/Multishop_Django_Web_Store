from shop.models import Delivery
from tests.test_settings import Settings


class BasketModelTest(Settings):

    def setUp(self) -> None:
        super().setUp()
        from basket.models import ProductInBasket
        self.product_in_basket = ProductInBasket.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())

    def test_check_creating_instance(self):
        from basket.models import ProductInBasket
        count = ProductInBasket.objects.all().count()

        ProductInBasket.objects.create(product=self.product,
                                       user_authenticated=self.user,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        self.assertEqual(count, ProductInBasket.objects.all().count() - 1)

    def test_model_product_in_basket(self):
        from basket.models import ProductInBasket
        product = ProductInBasket.objects.all().last()
        self.assertEqual(product.user_authenticated, self.user.email)
        self.assertEqual(product.product, self.product)
        self.assertEqual(product.nmb, 1)
        self.assertEqual(float(product.price_per_item), float(self.product.price_now))
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.color.pk, self.color.pk)
        self.assertEqual(product.size.pk, self.size.pk)

    def test_save_basket(self):
        from basket.models import ProductInBasket
        product = ProductInBasket.objects.all().last()
        product.nmb = 3
        product.save()
        self.assertEqual(product.total_price, float(self.product.price_now) * 3)

    def test_get_products_in_user_basket(self):
        from django.db.models import QuerySet
        product = self.product_in_basket
        answer = product.get_products_in_user_basket(self.user)
        self.assertEqual(type(answer), QuerySet)
        self.assertEqual(answer.count(), 1)

    def test_get_amount_in_user_basket(self):
        from decimal import Decimal
        product = self.product_in_basket
        answer = product.get_amount_in_user_basket(self.user)
        self.assertEqual(type(answer), Decimal)
        self.assertEqual(answer, Decimal(self.product.price_now))


class FavoriteModelTest(Settings):

    def test_model_favorite(self):
        from favorite.models import Favorite
        count = Favorite.objects.all().count()
        Favorite.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())
        self.assertEqual(count, Favorite.objects.all().count() - 1)

        product = Favorite.objects.all().last()
        self.assertEqual(product.user_authenticated, self.user.email)
        self.assertEqual(product.product, self.product)
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.color.pk, self.color.pk)
        self.assertEqual(product.size.pk, self.size.pk)
        self.assertEqual(product.__str__(), self.product.title)

    def test_get_products_in_user_favorite(self):
        from favorite.models import Favorite
        from django.db.models import QuerySet
        product = Favorite.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())
        answer = product.get_products_in_user_favorite(self.user)
        self.assertEqual(type(answer), QuerySet)
        self.assertEqual(answer.count(), 1)


class NewsModelTest(Settings):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import tempfile
        from news.models import Category
        from news.models import News
        cls.category_news = Category.objects.create(title='Big news',
                                                    slug='big_news')
        cls.news = News.objects.create(title='News 1',
                                       content='content news',
                                       photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                       category=cls.category_news,
                                       slug='news_1')

    def test_model_news(self):
        from news.models import News
        count = News.objects.all().count()
        self.assertEqual(count, 1)
        news = News.objects.all().last()
        self.assertEqual(news.title, 'News 1')
        self.assertEqual(news.content, 'content news')
        self.assertEqual(news.category, self.category_news)
        self.assertEqual(news.slug, 'news_1')
        self.assertIsNotNone(news.photo)
        self.assertTrue(news.is_published)
        self.assertIn(news.slug, news.get_absolute_url())

    def test_model_category(self):
        from news.models import Category
        category = Category.objects.all().last()
        count = Category.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(category.title, 'Big news')
        self.assertEqual(category.slug, 'big_news')
        self.assertIn(self.category_news.slug, self.category_news.get_absolute_url())


class OrderModelTest(Settings):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from orders.models import Order
        from orders.models import GoodsInTheOrder
        from orders.models import Status
        from orders.models import PaymentMethod
        from orders.models import PromoCode
        cls.delivery = Delivery.objects.create(title='Free',
                                               )
        cls.promo_code = PromoCode.objects.create(title='promo 1',
                                                  price=100, )
        cls.payment_method = PaymentMethod.objects.create(title='PayPall')
        cls.status = Status.objects.create(title='Developed')
        cls.goods_in_the_order = GoodsInTheOrder.objects.create(
            product=cls.product,
            size_id=cls.product.get_default_size_id(),
            color_id=cls.product.get_default_color_id())

        cls.order = Order.objects.create(user=cls.user,
                                         phone_number='3805000000',
                                         status=cls.status,
                                         payment_method=cls.payment_method,
                                         promo_code=cls.promo_code)


    def test_model_promo_code(self):
        from orders.models import PromoCode
        promo = PromoCode.objects.all().last()
        self.assertEqual(promo.title, 'promo 1')
        self.assertEqual(promo.price, 100)
