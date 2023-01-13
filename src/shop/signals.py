from django.db.models import Avg, Count

from shop.models import Reviews


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
