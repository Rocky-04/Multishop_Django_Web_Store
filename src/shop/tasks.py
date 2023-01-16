from celery import shared_task
from celery_singleton import Singleton


@shared_task(base=Singleton)
def update_product_rating(product_pk: int) -> None:
    from django.db.models import Avg, Count
    from shop.models import Reviews, Product

    product = Product.objects.get(pk=product_pk)

    # Get the average rating and the number of ratings for the product
    reviews = Reviews.objects.filter(product=product).aggregate(Avg('rating'), Count('rating'))
    rating = reviews['rating__avg']
    count_reviews = reviews['rating__count']

    # Update the product's rating and review count, and save the changes
    product.rating = rating
    product.count_reviews = count_reviews
    product.save(force_update=True)
