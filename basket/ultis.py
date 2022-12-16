from django.views import View


class BasketMixin(View):
    """
    Generic mixin is for a user's basket
    """

    def __init__(self):
        """
        Receives data from the post method:
        :self.current: A string representing the full path to the requested page.
        :self.nmb: The number of products.
        :self.size: The ID of the size of the product.
        :self.color: The ID of the color of the product.
        :self.product_id: The ID of the product to from the basket.
        :self.user_authenticated: The unique identifier of the session or user's email.
        """
        super().__init__()
        self.user_authenticated = None
        self.product_id = None
        self.size = None
        self.color = None
        self.nmb = None
        self.current = None

    def post(self, request, *args, **kwargs):
        data = request.POST
        self.current = data.get('current')
        self.nmb = data.get("count")
        self.size = data.get("size")
        self.color = data.get("color")
        self.product_id = kwargs.get('id')
        self.user_authenticated = request.session['user_authenticated']
