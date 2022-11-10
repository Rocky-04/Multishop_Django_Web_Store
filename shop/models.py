from django.db import models
from django.db.models import Avg
from django.db.models import Count
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from users.models import User


class Category(MPTTModel, models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['title']

    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True,
                            db_index=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True,
                                blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'slug': self.slug})

    def get_count_product_in_category(self):
        """
        Returns count(int) product of nested categories
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
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']

    title = models.CharField(max_length=50, unique=True)
    title_two = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=50, blank=True, db_index=True)
    description = models.TextField(blank=True, default=None)
    is_active = models.BooleanField(default=True, blank=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/',
                                verbose_name="Photo", null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('tag', kwargs={'slug': self.slug})


class Country(models.Model):
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['title']

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            db_index=True)

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['title']

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True,
                            db_index=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True,
                                blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('brand', kwargs={'slug': self.slug})


class Product(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-available', '-count_sale', '-created_at', 'price']

    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, db_index=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    price_now = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    description = models.TextField(blank=True, default=None)
    param = models.TextField(blank=True, default=None)
    vendorCode = models.CharField(max_length=50, blank=True)
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
    counnt_reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.slug})

    def get_title_photo(self):
        images = AttributeColorImage.objects.filter(product__product=self,
                                                    product__available=True)
        if images:
            return images[0].images.url
        images = AttributeColorImage.objects.filter(product__product=self)
        if images:
            return images[0].images.url
        else:
            return '/media/images/empty/empty.png'

    def get_title_color_id(self):
        return AttributeColor.objects.filter(product=self)[0].id

    def get_title_size_id(self):
        return AttributeSize.objects.filter(product__product=self)[0].id

    def save(self, *args, **kwargs):
        if self.discount == 0:
            self.price_now = self.price
        else:
            self.price_now = self.price - (self.price / 100 * self.discount)
        super(Product, self).save(*args, **kwargs)

    def get_pk(self):
        return self.pk

    def get_active_color(self):
        return AttributeColor.objects.filter(product=self, available=True)

    def get_all_color(self):
        return AttributeColor.objects.filter(product=self)

    def get_reviews(self):
        return Reviews.objects.filter(product=self)


class Color(models.Model):
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    value = models.CharField(max_length=15, blank=True, default=None,
                             null=True)

    def __str__(self):
        return self.value


class AttributeColor(models.Model):
    class Meta:
        verbose_name = 'Attribute color'
        verbose_name_plural = 'Attribute colors'

    product = models.ForeignKey('Product', related_name="attribute_color",
                                on_delete=models.CASCADE)
    color = models.ForeignKey('Color', on_delete=models.CASCADE,
                              related_name="color", blank=True, default=None,
                              null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product.title) + ' ' + str(self.color)

    def save(self, *args, **kwargs):
        if self.available is False and self.product.available is True:
            product = self.product.get_active_color()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()
        if self.available is True and self.product.available is False:
            self.product.available = True
            self.product.save()

        super().save(*args, **kwargs)

    def get_photo(self):
        return AttributeColorImage.objects.filter(product=self)

    def get_title_photo(self):
        images = AttributeColorImage.objects.filter(product=self)
        if len(images) > 0:
            return images[0].images.url
        else:
            return '/media/images/empty/empty.png'

    def get_active_size(self):
        return AttributeSize.objects.filter(product=self, available=True)

    def get_all_size(self):
        return AttributeSize.objects.filter(product=self)


class Size(models.Model):
    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    value = models.CharField(max_length=15, blank=True, default=None,
                             null=True)

    def __str__(self):
        return self.value


class AttributeSize(models.Model):
    class Meta:
        verbose_name = 'AttributeSize'
        verbose_name_plural = 'AttributeSizes'

    product = models.ForeignKey('AttributeColor',
                                related_name="attribute_size",
                                on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE,
                             related_name="size", blank=True, default=None,
                             null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product) + ' ' + str(self.size)

    def save(self, *args, **kwargs):
        if self.available is False and self.product.available is True:
            product = self.product.get_active_size()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()
        if self.available is True and self.product.available is False:
            self.product.available = True
            self.product.save()

        super().save(*args, **kwargs)


class AttributeColorImage(models.Model):
    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    product = models.ForeignKey(AttributeColor, default=None,
                                on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/%Y/%m/%d/')


class Delivery(models.Model):
    class Meta:
        verbose_name = 'shipping cost'
        verbose_name_plural = 'cost of delivery'
        ordering = ['price']

    title = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    order_price = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return str(self.price)

    @staticmethod
    def get_delivery(amount):
        delivery = Delivery.objects.filter(is_active=True)

        for item in delivery:
            if amount >= item.order_price:
                return item


class Banner(models.Model):
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['pk']

    title = models.CharField(max_length=50, unique=True)
    tag = models.ForeignKey(Tag, blank=True, on_delete=models.CASCADE)


class Currency(models.Model):
    title = models.CharField(max_length=100, unique=True)
    rate = models.IntegerField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ['title']


class Reviews(models.Model):
    class Meta:
        unique_together = ('user', 'product')

    RATINGS = [(1, _('Дуже погано')),
               (2, _('Погано')),
               (3, _('Нормально')),
               (4, _('Добре')),
               (5, _('Дуже добре'))]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='rewiews')
    text = models.TextField(max_length=200)
    rating = models.IntegerField(blank=True, choices=RATINGS)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


def rating_in_product_post_save(sender, instance, created=None, **kwargs):
    product = instance.product
    reviews = Reviews.objects.filter(product=product).aggregate(Avg('rating'),
                                                                Count(
                                                                    'rating'))
    rating = reviews['rating__avg']
    count_rewiews = reviews['rating__count']
    instance.product.rating = rating
    instance.product.counnt_reviews = count_rewiews
    instance.product.save(force_update=True)


post_save.connect(rating_in_product_post_save, sender=Reviews)
