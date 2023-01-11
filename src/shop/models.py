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
import logging
from users.models import User

logger = logging.getLogger(__name__)


class Category(MPTTModel, models.Model):
    """
     A model representing a category of products.
     A category can have nested subcategories, and it can have products associated with it.
     """

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

    def get_product_count(self) -> int:
        """
        Gets the number of products in this category and its nested subcategories.

        :return: The number of products in this category and its nested subcategories.
        """
        try:
            list_categories = self.get_descendants(include_self=True)
            return Product.objects.filter(category__in=list_categories).count()
        except Product.DoesNotExist as error:
            logger.error(f"No products found in category : {error}")
            return 0

    @staticmethod
    def get_category_by_slug(slug: str) -> 'Category':
        """
        Gets a category by slug.

        :param slug: The slug of the category to retrieve.
        :return: The category with the specified slug, or None if no such category exists.
        """
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist as error:
            logger.error(f"{slug}: {error}")
            return None

    @staticmethod
    def get_categories_by_parent_id(parent_id: int = None) -> QuerySet:
        """
        Gets the categories with the specified parent.

        :param parent_id: The ID of the parent category to filter by.
        :return: The set of categories with the specified parent ID, or an empty QuerySet if no such
            categories exist.
        """
        try:
            return Category.objects.filter(parent__id=parent_id)
        except Category.DoesNotExist as error:
            logger.error(f"{parent_id}: {error}")
            return Category.objects.none()

    @staticmethod
    def get_all_categories() -> QuerySet:
        """
        Gets all categories in the database.

        :return: A QuerySet containing all categories in the database.
        """
        try:
            return Category.objects.all()
        except Category.DoesNotExist as error:
            logger.error(f"No found categories: {error}")
            return Category.objects.none()


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

    @staticmethod
    def get_tag_by_slug(slug: str) -> 'Tag':
        """
        Gets a tag by slug

        :param slug: The slug of the tag to retrieve.
        :return: The tag with the specified slug, or None if no such tag exists.
        """
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist as error:
            logger.error(f"No found tags {slug}: {error}")
            return None


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
    slug = models.SlugField(max_length=50, unique=True, blank=True, db_index=True)
    picture = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('brand', kwargs={'slug': self.slug})

    @staticmethod
    def get_active_brand_with_photo() -> QuerySet:
        """
        Gets manufacturers with photo

        :return: A QuerySet of manufacturers with photo
        """
        try:
            return Manufacturer.objects.annotate(cnt=Count('picture')).filter(cnt__gt=0)
        except Category.DoesNotExist as error:
            logger.error(f"No found manufacturers with photo: {error}")
            return Manufacturer.objects.none()

    @staticmethod
    def get_brand_by_slug(slug: str) -> 'Manufacturer':
        """
        Gets a brand by slug

        :param slug: The slug of the manufacturer to retrieve.
        :return: The brand with the specified slug, or None if no such brand exists.
        """
        try:
            return Manufacturer.objects.get(slug=slug)
        except Manufacturer.DoesNotExist:
            return None


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

    def get_title_photo(self) -> str:
        """
        Chooses a photo of the main color of the product or uses the default photo

        :return: The URL of the chosen photo
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

        :return: The default color id of the selected product
        :raises AttributeError: If no default color is found for the selected product
        """
        try:
            return AttributeColor.objects.filter(product=self)[0].id
        except AttributeError as error:
            logger.error(f"Error getting default color id for product {self.id}: {error}")
            raise error

    def get_default_size_id(self) -> int:
        """
        Returns the default size id of the selected product

        :return: The default size id of the selected product
        :raises AttributeError: If no default size is found for the selected product
        """
        try:
            return AttributeSize.objects.filter(product__product=self)[0].id
        except AttributeError as error:
            logger.error(f"Error getting default size id for product {self.id}: {error}")
            raise error

    def save(self, *args, **kwargs):
        """
        Sets the price of the product, taking into account the discount

        :param args: Additional arguments to be passed to the parent class's `save` method
        :param kwargs: Additional keyword arguments to be passed to the parent class's `save` method
        :raises ValueError: If the discount is negative or greater than 100
        """
        try:
            if self.discount == 0:
                self.price_now = self.price
            else:
                if self.discount < 0 or self.discount > 100:
                    raise ValueError("Discount must be a positive number less than or equal to 100")
                self.price_now = self.price - (self.price / 100 * self.discount)
            super(Product, self).save(*args, **kwargs)
        except ValueError as error:
            logger.error(f"Error setting price for product {self.id}: {error}")
            raise error

    def get_color(self, available: bool = True) -> QuerySet:
        """
        Returns the colors of the selected product

        :param available: Whether to only return colors that are available (defaults to True)
        :return: A QuerySet of colors for the selected product
        :raises AttributeError: If no colors are found for the selected product
        """
        try:
            if available:
                return AttributeColor.objects.filter(product=self, available=True)
            return AttributeColor.objects.filter(product=self)
        except AttributeError as error:
            logger.error(f"Error getting colors for product {self.id}: {error}")
            raise error

    def get_reviews(self) -> QuerySet:
        """
        Collects all product reviews

        :return: A QuerySet of reviews for the selected product
        :raises AttributeError: If no reviews are found for the selected product
        """
        try:
            return Reviews.objects.filter(product=self)
        except AttributeError as error:
            logger.error(f"Error getting reviews for product {self.id}: {error}")
            raise error

    @staticmethod
    def get_product_by_slug(slug: str) -> 'Product':
        """
        Gets a product by slug

        :param slug: The slug of the product to retrieve
        :return: The Product instance with the specified slug
        :raises Product.DoesNotExist: If no product is found with the specified slug
        """
        try:
            return Product.objects.select_related('category', 'country', 'manufacturer').get(
                slug=slug)
        except Product.DoesNotExist as error:
            logger.error(f"Error getting product with slug {slug}: {error}")
            raise error

    @staticmethod
    def get_all_products() -> QuerySet:
        """
        Gets all products

        :return: A QuerySet of all products
        :raises AttributeError: If no products are found
        """
        try:
            return Product.objects.all()
        except AttributeError as error:
            logger.error(f"Error getting all products: {error}")
            raise error


class Color(models.Model):
    value = models.CharField(max_length=15, blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return str(self.value)


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
        the availability of its colors is changed.

        The product's availability is changed to False if there are no available colors remaining,
        and changed to True if any of the colors are available.
        """
        # Check if the current color is being set to unavailable,
        # and the main product is still available
        if not self.available and self.product.available:
            product = self.product.get_color()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()

        # Check if the current color is being set to available,
        # and the main product is currently unavailable
        if self.available and not self.product.available:
            self.product.available = True
            self.product.save()

        super().save(*args, **kwargs)

    def get_photo(self) -> QuerySet:
        """
        Retrieves all photos associated with the given color.

        :return: A queryset of photos for the given color.
        """
        try:
            return AttributeColorImage.objects.filter(product=self)
        except AttributeColorImage.DoesNotExist as error:
            logger.error(f"Error getting photos for color {self.id}: {error}")
            return QuerySet()

    def get_title_photo(self) -> str:
        """
        Returns the main photo for the selected color.

        :return: The URL of the main photo for the selected color, or the URL of a default
            placeholder image if no photos are available.
        """
        images = AttributeColorImage.objects.filter(product=self)
        if images.exists():
            # Return the URL of the first photo in the queryset
            return images[0].images.url
        else:
            # Return the URL of a default placeholder image
            logger.warning(f"Empty photo for color {self}")
            return '/media/images/empty/empty.png'

    def get_size(self, available: bool = True) -> QuerySet:
        """
        Gets the sizes of the selected color.

        :param available: Whether to return only available sizes. Defaults to True.
        :return: A queryset of sizes for the selected color.
        """
        try:
            sizes = AttributeSize.objects.filter(product=self)

            if available:
                # If available is True, filter the queryset to return only available sizes
                return sizes.filter(available=True)
            else:
                # If available is False, return the entire queryset
                return sizes
        except AttributeError as error:
            logger.error(f"Error getting sizes for color {self.id}: {error}")
            raise error


class Size(models.Model):
    value = models.CharField(max_length=15, blank=True, default=None, null=True)

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return str(self.value)


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

    def save(self, *args, **kwargs) -> None:
        """
        Changes the color availability when
        the availability of its sizes is changed.
        """
        # Check if the current color is set to unavailable and the main
        # product is still available
        if not self.available and self.product.available:
            product = self.product.get_size()
            if len(product) <= 1:
                self.product.available = False
                self.product.save()

        # Check if the current color is set to available and the main
        # product is currently unavailable
        if self.available and not self.product.available:
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
        return str(self.product)


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
    def get_delivery(amount: float) -> "Delivery":
        """
        Calculates the delivery cost for a given order amount.
        
        :param amount: The total amount of the order.
        :return: The delivery cost for the given order amount,
            or None if no matching delivery cost is found.
        """
        try:
            # Get all active delivery costs, sorted by descending order price
            delivery_costs = Delivery.objects.filter(is_active=True).order_by("-order_price")

            # Find the first delivery cost with an order price
            # that is less than or equal to the given amount
            for delivery in delivery_costs:
                if amount >= delivery.order_price:
                    return delivery

            # If no matching delivery cost is found, return the last delivery cost in the queryset
            return delivery_costs[-1]
        except IndexError as error:
            # If no delivery costs are found, return None
            logger.error(f"No found delivery: {error}")
            return None


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


def rating_in_product_post_save(sender, instance, created=None, **kwargs) -> None:
    """
    Reacts to the change or addition of product reviews.
    Updates the average product rating and the number of reviews.
    """
    # Get the product associated with the review that was just added or changed
    product = instance.product

    # Get the average rating and the number of ratings for the product
    reviews = Reviews.objects.filter(product=product).aggregate(Avg('rating'), Count('rating'))
    rating = reviews['rating__avg']
    count_reviews = reviews['rating__count']

    # Update the product's rating and review count, and save the changes
    product.rating = rating
    product.count_reviews = count_reviews
    product.save(force_update=True)


post_save.connect(rating_in_product_post_save, sender=Reviews)
