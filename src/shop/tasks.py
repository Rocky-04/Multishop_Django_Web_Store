from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction


@shared_task(base=Singleton)
def update_product_rating(product_pk: int) -> None:
    from django.db.models import Avg, Count
    from shop.models import Reviews, Product

    # Get the average rating and the number of ratings for the product
    reviews = Reviews.objects.filter(product__pk=product_pk).aggregate(Avg('rating'),
                                                                       Count('rating'))

    # Update the product's rating and review count, and save the changes
    with transaction.atomic():
        product = Product.objects.get(pk=product_pk)
        product.rating = reviews['rating__avg']
        product.count_reviews = reviews['rating__count']
        product.save(force_update=True)
