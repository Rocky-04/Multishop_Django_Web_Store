class BasketMixin:

    def __init__(self):
        self.session_key = None
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

        if request.user.is_authenticated:
            self.session_key = request.user.email
        else:
            self.session_key = request.session.session_key
