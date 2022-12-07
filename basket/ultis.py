from django.views import View


class BasketMixin(View):

    def __init__(self):
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
