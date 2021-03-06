import uuid

from django.core.urlresolvers import reverse

from lib.sellers.models import Seller, SellerPaypal, SellerProduct
from solitude.base import APITest


def make_seller_paypal(uuid):
    seller = Seller.objects.create(uuid=uuid)
    product = SellerProduct.objects.create(seller=seller, external_id='xyz')
    paypal = SellerPaypal.objects.create(seller=seller)
    return seller, paypal, product


class SellerTest(APITest):

    def create_seller(self, **kwargs):
        defaults = {'uuid': 'seller:' + str(uuid.uuid4())}
        defaults.update(kwargs)
        return Seller.objects.create(**defaults)

    def get_seller_uri(self, seller):
        return reverse(
            'api_dispatch_detail',
            kwargs={
                'api_name': 'generic',
                'resource_name': 'seller',
                'pk': seller.pk,
            }
        )

    def create_seller_product(self, seller=None, **kwargs):
        defaults = {
            'seller': seller or self.create_seller(),
            'public_id': 'public:' + str(uuid.uuid4()),
            'external_id': 'external:' + str(uuid.uuid4()),
        }
        defaults.update(kwargs)

        return SellerProduct.objects.create(**defaults)

    def get_seller_product_uri(self, seller_product):
        return reverse(
            'api_dispatch_detail',
            kwargs={
                'api_name': 'generic',
                'resource_name': 'product',
                'pk': seller_product.pk,
            }
        )
