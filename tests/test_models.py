import datetime
import tempfile
from decimal import Decimal

from django.db.models import QuerySet

from basket.models import ProductInBasket
from favorite.models import Favorite
from news.models import Category
from news.models import News
from orders.models import GoodsInTheOrder
from orders.models import Order
from orders.models import PaymentMethod
from orders.models import PromoCode
from orders.models import Status
from shop.models import AttributeColor
from shop.models import AttributeSize
from shop.models import Banner
from shop.models import Category as Category_Product
from shop.models import Color
from shop.models import Country
from shop.models import Currency
from shop.models import Delivery
from shop.models import Manufacturer
from shop.models import Product
from shop.models import Reviews
from shop.models import Size
from shop.models import Tag
from tests.test_settings import Settings
from users.models import EmailForNews
from users.models import User


class BasketModelTest(Settings):

    def setUp(self) -> None:
        super().setUp()
        self.product_in_basket = ProductInBasket.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())

    def test_check_creating_instance(self):
        count = ProductInBasket.objects.count()

        ProductInBasket.objects.create(product=self.product,
                                       user_authenticated=self.user,
                                       size_id=self.product.get_default_size_id(),
                                       color_id=self.product.get_default_color_id())
        self.assertEqual(count, ProductInBasket.objects.all().count() - 1)

    def test_model_product_in_basket(self):
        product = ProductInBasket.objects.last()
        self.assertEqual(product.user_authenticated, self.user.email)
        self.assertEqual(product.product, self.product)
        self.assertEqual(product.nmb, 1)
        self.assertEqual(float(product.price_per_item), float(self.product.price_now))
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.color.pk, self.color.pk)
        self.assertEqual(product.size.pk, self.size.pk)

    def test_save_basket(self):
        product = ProductInBasket.objects.last()
        product.nmb = 3
        product.save()
        self.assertEqual(product.total_price, float(self.product.price_now) * 3)

    def test_get_products_in_user_basket(self):
        product = ProductInBasket.objects.last()
        answer = product.get_products_in_user_basket(self.user)
        self.assertEqual(type(answer), QuerySet)
        self.assertEqual(answer.count(), 1)

    def test_get_amount_in_user_basket(self):
        product = ProductInBasket.objects.last()
        answer = product.get_amount_in_user_basket(self.user)
        self.assertEqual(type(answer), Decimal)
        self.assertEqual(answer, Decimal(self.product.price_now))


class FavoriteModelTest(Settings):

    def test_model_favorite(self):
        count = Favorite.objects.count()
        Favorite.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())
        self.assertEqual(count, Favorite.objects.all().count() - 1)

        product = Favorite.objects.last()
        self.assertEqual(product.user_authenticated, self.user.email)
        self.assertEqual(product.product, self.product)
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.color.pk, self.color.pk)
        self.assertEqual(product.size.pk, self.size.pk)
        self.assertEqual(product.__str__(), self.product.title)

    def test_get_products_in_user_favorite(self):
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
        cls.category_news = Category.objects.create(title='Big news',
                                                    slug='big_news')
        cls.news = News.objects.create(title='News 1',
                                       content='content news',
                                       photo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                       category=cls.category_news,
                                       slug='news_1')

    def test_model_news(self):
        count = News.objects.all().count()
        self.assertEqual(count, 1)
        news = News.objects.last()
        self.assertEqual(news.title, 'News 1')
        self.assertEqual(news.content, 'content news')
        self.assertEqual(news.category, self.category_news)
        self.assertEqual(news.slug, 'news_1')
        self.assertIsNotNone(news.photo)
        self.assertTrue(news.is_published)
        self.assertIn(news.slug, news.get_absolute_url())

    def test_model_category(self):
        category = Category.objects.last()
        count = Category.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(category.title, 'Big news')
        self.assertEqual(category.slug, 'big_news')
        self.assertIn(self.category_news.slug, self.category_news.get_absolute_url())


class OrderModelTest(Settings):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.promo_code = PromoCode.objects.create(title='promo 1',
                                                  price=250, )
        cls.payment_method = PaymentMethod.objects.create(title='PayPall')
        cls.status = Status.objects.create(title='Developed')
        cls.order = Order.objects.create(user=cls.user,
                                         phone_number='3805000000',
                                         status=cls.status,
                                         payment_method=cls.payment_method,
                                         promo_code=cls.promo_code)
        cls.goods_in_the_order = GoodsInTheOrder.objects.create(
            order=cls.order,
            product=cls.product,
            size_id=cls.product.get_default_size_id(),
            color_id=cls.product.get_default_color_id())

    def test_model_promo_code(self):
        promo = PromoCode.objects.last()
        self.assertEqual(promo.title, 'promo 1')
        self.assertEqual(promo.price, 250)

    def test_model_payment_method(self):
        method = PaymentMethod.objects.last()
        self.assertEqual(method.title, 'PayPall')

    def test_model_status(self):
        status = Status.objects.last()
        self.assertEqual(status.title, 'Developed')

    def test_model_goods_in_the_order(self):
        product = GoodsInTheOrder.objects.last()
        self.assertEqual(product.product, self.product)
        self.assertEqual(product.color.pk, self.color.pk)
        self.assertEqual(product.size.pk, self.size.pk)
        self.assertEqual(product.order, self.order)
        self.assertEqual(product.total_price, Decimal(1000))
        self.assertEqual(product.nmb, 1)
        self.assertEqual(product.price_per_item, Decimal(self.product.price_now))

    def test_model_goods_in_the_order_save(self):
        product = GoodsInTheOrder.objects.last()
        product.nmb = 3
        product.save()
        self.assertEqual(product.total_price, 3000)

    def test_model_order(self):
        order = Order.objects.last()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.phone_number, '3805000000')
        self.assertEqual(order.status, self.status)
        self.assertEqual(order.payment_method, self.payment_method)
        self.assertEqual(order.promo_code, self.promo_code)
        self.assertEqual(order.total_price, 850)
        self.assertEqual(order.delivery, self.delivery)

    def test_model_product_in_order_post_save(self):
        product = GoodsInTheOrder.objects.last()
        product.nmb = 5
        product.save()
        order = Order.objects.last()
        self.assertEqual(order.total_price, 4850)


class ShopModelTest(Settings):

    def test_model_category(self):
        category = Category_Product.objects.last()
        self.assertEqual(category.title, 'Bags')
        self.assertEqual(category.slug, 'bags')
        self.assertIn(category.slug, category.get_absolute_url())

    def test_model_tag(self):
        tag = Tag.objects.last()
        self.assertEqual(tag.title, 'Sale')
        self.assertEqual(tag.slug, 'sale')
        self.assertEqual(tag.description, 'Any text')
        self.assertEqual(tag.is_active, True)
        self.assertIn(tag.slug, tag.get_absolute_url())

    def test_model_country(self):
        country = Country.objects.last()
        self.assertEqual(country.title, 'Ukraine')
        self.assertEqual(country.slug, 'ukraine')

    def test_model_manufacturer(self):
        brand = Manufacturer.objects.last()
        self.assertEqual(brand.title, 'Havana')
        self.assertEqual(brand.slug, 'havana')
        self.assertIn(brand.slug, brand.get_absolute_url())

    def test_model_product(self):
        product = Product.objects.last()
        self.assertEqual(product.title, 'Mini bag')
        self.assertEqual(product.slug, 'mini_bag')
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.description, 'Any text')
        self.assertEqual(product.param, 'Param:1, Param:2')
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.manufacturer, self.manufacturer)
        self.assertEqual(product.currency, self.currency)
        self.assertEqual(product.country, self.country)
        self.assertEqual(product.rating, 4)
        self.assertEqual(product.count_reviews, 1)
        self.assertIn(product.slug, product.get_absolute_url())

    def test_model_product_get_default_color_id(self):
        product = Product.objects.last()
        self.assertEqual(product.get_default_color_id(), 1)

    def test_model_product_get_default_size_id(self):
        product = Product.objects.last()
        self.assertEqual(product.get_default_size_id(), 1)

    def test_model_product_save(self):
        product = Product.objects.last()
        product.discount = 10
        product.save()
        self.assertEqual(product.price_now, 900)
        self.assertEqual(product.discount, 10)

    def test_model_product_get_color(self):
        product = Product.objects.last()
        self.assertIn(self.attribute_color, product.get_color())
        self.assertEqual(type(product.get_color()), QuerySet)
        self.assertEqual(len(product.get_color()), 1)

    def test_model_product_get_reviews(self):
        product = Product.objects.last()
        self.assertEqual(type(product.get_reviews()), QuerySet)
        self.assertEqual(len(product.get_reviews()), 1)

    def test_model_color(self):
        color = Color.objects.last()
        self.assertEqual(color.value, 'black')

    def test_model_attribute_color(self):
        color = AttributeColor.objects.last()
        self.assertEqual(color.product, self.product)
        self.assertEqual(color.color, self.color)
        self.assertTrue(color.available)

    def test_model_attribute_color_get_size(self):
        color = AttributeColor.objects.last()
        self.assertEqual(type(color.get_size()), QuerySet)
        self.assertEqual(color.get_size()[0], self.attribute_size)

    def test_model_size(self):
        size = Size.objects.last()
        self.assertEqual(size.value, 'XL')

    def test_model_attribute_size(self):
        size = AttributeSize.objects.last()
        self.assertEqual(size.product, self.attribute_color)
        self.assertEqual(size.size, self.size)
        self.assertTrue(size.available)

    def test_model_delivery(self):
        delivery = Delivery.objects.last()
        self.assertEqual(delivery.title, 'MAX')
        self.assertEqual(delivery.price, 100)
        self.assertEqual(delivery.order_price, 0)
        self.assertTrue(delivery.is_active)

    def test_model_delivery_get_delivery(self):
        delivery = Delivery.objects.last()
        self.assertEqual(type(delivery.get_delivery(100)), Delivery)
        self.assertEqual(delivery.get_delivery(100), self.delivery)

    def test_model_banner(self):
        Banner.objects.create(title='Ban',
                              tag=self.tag)
        banner = Banner.objects.last()
        self.assertEqual(banner.title, 'Ban')
        self.assertEqual(banner.tag, self.tag)

    def test_model_currency(self):
        currency = Currency.objects.last()
        self.assertEqual(currency.title, 'UAH')
        self.assertEqual(currency.rate, 0)

    def test_model_reviews(self):
        reviews = Reviews.objects.last()
        self.assertEqual(reviews.user, self.user)
        self.assertEqual(reviews.product, self.product)
        self.assertEqual(reviews.text, 'Simple text')
        self.assertEqual(reviews.rating, 4)
        product = Product.objects.last()
        self.assertEqual(product.rating, 4)
        self.assertEqual(product.count_reviews, 1)

    def test_model_rating_in_product_post_save(self):
        reviews = Reviews.objects.last()
        reviews.rating = Reviews.RATINGS[1][0]
        reviews.save()
        product = Product.objects.last()
        self.assertEqual(product.rating, 2)
        self.assertEqual(product.count_reviews, 1)


class UserModelTest(Settings):

    def test_model_user(self):
        user = User.objects.last()
        self.assertEqual(user.email, 'roock@gmail.com')
        self.assertEqual(user.get_review_name(), 'anonymous')
        self.assertEqual(user.__str__(), 'roock@gmail.com')

    def test_model_user_create(self):
        User.objects.create(email='var@gmail.com',
                            password='a123587745a',
                            city='Kyiv',
                            phone_number='+38050505050',
                            address='Shevchenka 22',
                            postcode='16730',
                            additional_information='info',
                            birthday='1985-02-05',
                            first_name='Cristiano',
                            last_name='Ronaldo')
        user = User.objects.last()
        self.assertEqual(user.email, 'var@gmail.com')
        self.assertEqual(user.get_review_name(), 'Cristiano')
        self.assertEqual(user.__str__(), 'Cristiano Ronaldo')
        self.assertEqual(user.city, 'Kyiv')
        self.assertEqual(user.phone_number, '+38050505050')
        self.assertEqual(user.address, 'Shevchenka 22')
        self.assertEqual(user.additional_information, 'info')
        self.assertEqual(user.birthday, datetime.date(1985, 2, 5))
        self.assertEqual(user.first_name, 'Cristiano')
        self.assertEqual(user.last_name, 'Ronaldo')

    def test_model_email_for_news(self):
        EmailForNews.objects.create(email='zsu@gmail.com')
        email = EmailForNews.objects.last()

        self.assertEqual(email.email, 'zsu@gmail.com')
        self.assertTrue(email.is_active)

