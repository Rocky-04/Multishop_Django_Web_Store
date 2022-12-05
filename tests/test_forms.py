from django.urls import reverse

from basket.models import ProductInBasket
from orders.models import Order
from orders.models import PaymentMethod
from orders.models import PromoCode
from orders.models import Status
from shop.models import Reviews
from tests.test_settings import Settings


class CreateOrderFormTest(Settings):

    def setUp(self):
        super().setUp()
        Order.objects.all().delete()
        self.product_in_basket = ProductInBasket.objects.create(
            product=self.product,
            user_authenticated=self.user,
            size_id=self.product.get_default_size_id(),
            color_id=self.product.get_default_color_id())
        self.payment_method = PaymentMethod.objects.create(title='PayPall')
        self.status = Status.objects.create(title='Developed')
        self.promo_code = PromoCode.objects.create(title='promo 1', price=250, )
        self.client.force_login(self.user)

    def test_create_form(self):
        count = Order.objects.count()
        form_data = {'phone_number': '3805000000',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': 'Alex',
                     'promo_code': ''}
        self.client.post(reverse('checkout'),
                         data=form_data,
                         follow=True)
        self.assertEqual(count, Order.objects.count() - 1)

    def test_create_form_no_phone(self):
        count = Order.objects.count()
        form_data = {'phone_number': '',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': 'Alex',
                     'promo_code': ''}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['phone_number'])

    def test_create_form_wrong_method(self):
        count = Order.objects.count()
        form_data = {'phone_number': '+3805055454',
                     "payment_method": 2,
                     "email": 'frank@gmail.com',
                     'first_name': 'Alex',
                     'promo_code': ''}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['payment_method'])

    def test_create_form_wrong_email(self):
        count = Order.objects.count()
        form_data = {'phone_number': '+38050505',
                     "payment_method": 1,
                     "email": 'frankgmail.com',
                     'first_name': 'Alex',
                     'promo_code': ''}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['email'])

    def test_create_form_wrong_first_name(self):
        count = Order.objects.count()
        form_data = {'phone_number': '+3805050505',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': '',
                     'promo_code': ''}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['first_name'])

    def test_create_form_wrong_promo_code(self):
        count = Order.objects.count()
        form_data = {'phone_number': '+38050505',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': 'Michel',
                     'promo_code': 'test'}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['promo_code'])

    def test_create_form_correct_promo_code(self):
        count = Order.objects.count()
        form_data = {'phone_number': '+3805050',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': 'Michel',
                     'promo_code': 'promo 1'}
        self.client.post(reverse('checkout'),
                         data=form_data,
                         follow=True)
        self.assertEqual(Order.objects.last().total_price, 850)
        self.assertEqual(count, Order.objects.count() - 1)

    def test_create_form_no_active_promo_code(self):
        PromoCode.objects.create(title='promo 2',
                                 price=250,
                                 is_active=False)
        count = Order.objects.count()
        form_data = {'phone_number': '+38050505',
                     "payment_method": 1,
                     "email": 'frank@gmail.com',
                     'first_name': 'Michel',
                     'promo_code': 'promo 2'}
        response = self.client.post(reverse('checkout'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(count, Order.objects.count())
        self.assertTrue(response.context['form'].errors.get_json_data()['promo_code'])


class CreateReviewsFormTest(Settings):
    def setUp(self):
        super().setUp()
        Reviews.objects.all().delete()
        self.client.force_login(self.user)

    def test_create_valid_form(self):
        count = Reviews.objects.count()
        form_data = {'rating': Reviews.RATINGS[3][0],
                     'text': 'All right',
                     'product_id': self.product.pk,
                     'current': reverse('detail', kwargs={'slug': self.product.slug})}
        response = self.client.post(reverse('add_review'),
                                    data=form_data,
                                    follow=True)
        self.assertTrue(Reviews.objects.get(product=self.product))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Reviews.objects.count() - 1)

    def test_create_wrong_rating(self):
        count = Reviews.objects.count()
        form_data = {'rating': 7,
                     'text': 'All right',
                     'product_id': self.product.pk,
                     'current': reverse('detail', kwargs={'slug': self.product.slug})}
        response = self.client.post(reverse('add_review'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Reviews.objects.count())

    def test_create_wrong_text(self):
        count = Reviews.objects.count()
        form_data = {'rating': 5,
                     'text': '',
                     'product_id': self.product.pk,
                     'current': reverse('detail', kwargs={'slug': self.product.slug})}
        response = self.client.post(reverse('add_review'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Reviews.objects.count())

    def test_create_too_long_text(self):
        count = Reviews.objects.count()
        form_data = {'rating': 5,
                     'text': """Loose-fit sweatshirt in cotton-blend fabric with a printed  motif
                      at front and soft, brushed inside. Dropped shoulders, long sleeves,and ribbing
                      at neckline, cuffs, and hem. Loose-fit sweatshirt in cotton-blend fabric with
                      a printed motif at front and soft, brushed inside. Dropped shoulders, long 
                      sleeves, and ribbing at neckline, cuffs, and hem.""",
                     'product_id': self.product.pk,
                     'current': reverse('detail', kwargs={'slug': self.product.slug})}
        response = self.client.post(reverse('add_review'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Reviews.objects.count())

    def test_create_second_review(self):
        Reviews.objects.create(user=self.user,
                               product=self.product,
                               text='Simple text',
                               rating=4)

        count = Reviews.objects.count()
        form_data = {'rating': 5,
                     'text': 'Cool product',
                     'product_id': self.product.pk,
                     'current': reverse('detail', kwargs={'slug': self.product.slug})}
        response = self.client.post(reverse('add_review'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count, Reviews.objects.count())
        review = Reviews.objects.last()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, 'Cool product')
