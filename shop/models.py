from django.db import models
from django.db.models import Avg
from django.db.models import CharField
from django.db.models import Count
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from users.models import User


class Category(MPTTModel, models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True, db_index=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'slug': self.slug})

    def get_count_product_in_category(self):
        """
        Returns count product of nested categories
        """
        list_categories_pk = self.get_list_nested_categories()
        return Product.objects.filter(
            category_id__in=list_categories_pk).count()

    def get_list_nested_categories(self):
        """
        Returns list of pk categories
        """
        list_categories_pk = [self.pk]

        for item in self.get_children():
            list_categories_pk.append(item.pk)
            for item_two in item.get_children():
                list_categories_pk.append(item_two.pk)
                for item_three in item_two.get_children():
                    list_categories_pk.append(item_three.pk)

        return list_categories_pk


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    title_two = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, blank=True, db_index=True)
    description = models.TextField(blank=True, default=None)
    is_active = models.BooleanField(default=True, blank=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/',
                                verbose_name="Photo", null=True, blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('tag', kwargs={'slug': self.slug})


class Country(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            db_index=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['title']

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            db_index=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True,
                                blank=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('brand', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, db_index=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    price_now = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    description = models.TextField(blank=True, default=None)
    param = models.TextField(blank=True, default=None)
    vendor_code: CharField = models.CharField(max_length=50, blank=True)
    global_id = models.CharField(max_length=50, blank=True)
    count_sale = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.ForeignKey('Currency', on_delete=models.SET_NULL, default=1, null=True)
    category = TreeForeignKey(Category, on_delete=models.PROTECT, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, default=1,
                                blank=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True,
                                     default=1, related_name='manufacturer', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    rating = models.DecimalField(max_digits=10, decimal_places=0, default=5)
    count_reviews = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-available', '-count_sale', '-created_at', 'price']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.slug})

    def get_title_photo(self):
        """
        Chooses a photo of the main color of the product or uses the default photo
        """
        images = AttributeColorImage.objects.filter(product__product=self, product__available=True)
        if images:
            return images[0].images.url
        images = AttributeColorImage.objects.filter(product__product=self)
        if images:
            return images[0].images.url
        else:
            return '/media/images/empty/empty.png'

    def get_default_color_id(self) -> int:
        """
        Returns the default color id of the selected product
        """
        return AttributeColor.objects.filter(product=self)[0].id

    def get_default_size_id(self) -> int:
        """
        Returns the default size id of the selected product
        """
        return AttributeSize.objects.filter(product__product=self)[0].id

    def save(self, *args, **kwargs):
        """
        Sets the price of the product, taking into account the discount
        """
        if self.discount == 0:
            self.price_now = self.price
        else:
            self.price_now = self.price - (self.price / 100 * self.discount)
        super(Product, self).save(*args, **kwargs)

    def get_color(self, available: bool = True) -> QuerySet:
        """
        Returns the colors of the selected product
        :param available: bool
        :return: QuerySet
        """
        if available:
            return AttributeColor.objects.filter(product=self, available=True)
        return AttributeColor.objects.filter(product=self)

    def get_reviews(self) -> QuerySet:
        """
        Collects all product reviews
        :return: QuerySet
        """
        return Reviews.objects.filter(product=self)


class Color(models.Model):
    value = models.CharField(max_length=15, blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.value


class AttributeColor(models.Model):
    product = models.ForeignKey('Product', related_name="attribute_color",
                                on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, related_name="color",
                              blank=True, default=None, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Attribute color'
        verbose_name_plural = 'Attribute colors'

    def __str__(self):
        return str(self.product.title) + ' ' + str(self.color)

    def save(self, *args, **kwargs):
        """
        Changes the product availability of the main product when
        the availability of its colors is changed
        """
        if self.available is False and self.product.available is True:
            product = self.product.get_color()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()
        if self.available is True and self.product.available is False:
            self.product.available = True
            self.product.save()

        super().save(*args, **kwargs)

    def get_photo(self):
        """
        Returns all photos of the selected color
        """
        return AttributeColorImage.objects.filter(product=self)

    def get_title_photo(self):
        """
        Returns the main photo of the selected color
        """
        images = AttributeColorImage.objects.filter(product=self)
        if len(images) > 0:
            return images[0].images.url
        else:
            return '/media/images/empty/empty.png'

    def get_size(self, available: bool = True) -> QuerySet:
        """
        Returns the sizes of the selected color
        :param available: bool
        :return: QuerySet
        """
        if available:
            return AttributeSize.objects.filter(product=self, available=True)
        return AttributeSize.objects.filter(product=self)


class Size(models.Model):
    value = models.CharField(max_length=15, blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.value


class AttributeSize(models.Model):
    product = models.ForeignKey('AttributeColor', related_name="attribute_size",
                                on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE,
                             related_name="size", blank=True, default=None, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'AttributeSize'
        verbose_name_plural = 'AttributeSizes'

    def __str__(self):
        return str(self.product) + ' ' + str(self.size)

    def save(self, *args, **kwargs):
        """
        Changes the color availability when
        the availability of its sizes is changed
        """
        if self.available is False and self.product.available is True:
            product = self.product.get_size()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()
        if self.available is True and self.product.available is False:
            self.product.available = True
            self.product.save()

        super().save(*args, **kwargs)


class AttributeColorImage(models.Model):
    product = models.ForeignKey(AttributeColor, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/%Y/%m/%d/')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.product


class Delivery(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    order_price = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = 'shipping cost'
        verbose_name_plural = 'cost of delivery'
        ordering = ['price']

    def __str__(self):
        return str(self.price)

    @staticmethod
    def get_delivery(amount) -> "Delivery":
        """
        Calculates the delivery cost from the order amount
        :param amount:
        :return: Delivery
        """
        delivery = Delivery.objects.filter(is_active=True).order_by("-order_price")
        for item in delivery:
            if amount >= item.order_price:
                return item
        return delivery[-1]


class Banner(models.Model):
    title = models.CharField(max_length=50, unique=True)
    tag = models.ForeignKey(Tag, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['pk']

    def __str__(self):
        return self.title


class Currency(models.Model):
    title = models.CharField(max_length=100, unique=True)
    rate = models.IntegerField(blank=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ['title']

    def __str__(self):
        return self.title


class Reviews(models.Model):
    RATINGS = [(1, _('Very bad')),
               (2, _('Bad')),
               (3, _('Normal')),
               (4, _('OK')),
               (5, _('Very good'))]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(max_length=200)
    rating = models.IntegerField(blank=True, choices=RATINGS)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return str(self.rating)


def rating_in_product_post_save(sender, instance, created=None, **kwargs):
    """
    Reacts to the change or addition of product reviews.
    Changes the average product review
    """
    product = instance.product
    reviews = Reviews.objects.filter(product=product).aggregate(Avg('rating'), Count('rating'))
    rating = reviews['rating__avg']
    count_reviews = reviews['rating__count']
    instance.product.rating = rating
    instance.product.count_reviews = count_reviews
    instance.product.save(force_update=True)


post_save.connect(rating_in_product_post_save, sender=Reviews)
