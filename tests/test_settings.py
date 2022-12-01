import os
import shutil
import tempfile
import tracemalloc

from django.conf import settings
from django.test import TestCase
from django.utils.translation import activate

from shop.models import AttributeColor
from shop.models import AttributeColorImage
from shop.models import AttributeSize
from shop.models import Category
from shop.models import Color
from shop.models import Country
from shop.models import Currency
from shop.models import Delivery
from shop.models import Manufacturer
from shop.models import Product
from shop.models import Size
from shop.models import Tag
from users.models import User


class Settings(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
        # Create a temporary folder
        tracemalloc.start()
        activate('en')
        settings.MEDIA_ROOT = tempfile.mktemp(dir=settings.BASE_DIR)
        settings.DJANGO_TEST_PROCESSES = 4
        settings.PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ]

        cls.manufacturer = Manufacturer.objects.create(title='Havana',
                                                       slug='havana',
                                                       picture=tempfile.NamedTemporaryFile(
                                                           suffix=".jpg").name)
        cls.category = Category.objects.create(title='Bags',
                                               slug='bags',
                                               picture=tempfile.NamedTemporaryFile(
                                                   suffix=".jpg").name)
        cls.tag = Tag.objects.create(title='Sale',
                                     slug='sale',
                                     description='Any text',
                                     picture=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        cls.currency = Currency.objects.create(title='UAH', rate=0)
        cls.country = Country.objects.create(title='Ukraine', slug='ukraine')
        cls.product = Product.objects.create(title='Mini bag',
                                             slug='mini_bag',
                                             price='1000.00',
                                             description='Any text',
                                             param='Param:1, Param:2',
                                             category=cls.category,
                                             manufacturer=cls.manufacturer,
                                             currency=cls.currency,
                                             country=cls.country
                                             )
        cls.product.tags.add(cls.tag)
        cls.color = Color.objects.create(value='black')
        cls.size = Size.objects.create(value='XL')
        cls.attribute_color = AttributeColor.objects.create(product=cls.product,
                                                            color=cls.color, )
        cls.attribute_size = AttributeSize.objects.create(product=cls.attribute_color,
                                                          size=cls.size, )
        cls.attribute_color_image = AttributeColorImage.objects.create(
            product=cls.attribute_color, images=tempfile.NamedTemporaryFile(suffix=".jpg").name, )

        cls.delivery = Delivery.objects.create(title='MAX',
                                               price=100, )
        cls.user = User.objects.create(email='roock@gmail.com',
                                       password='aaaa12154')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Delete temporary files
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
