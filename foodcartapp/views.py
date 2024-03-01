import datetime

from django.http import JsonResponse
from django.templatetags.static import static

import json
from .models import Product, UserOrder, OrderState


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    post_request = json.loads(request.body.decode())
    if (post_request['products']):
        userorder = UserOrder.objects.create(name=post_request['firstname'],
                                             surname=post_request['lastname'],
                                             address=post_request['address'],
                                             phonenumber=post_request['phonenumber'],
                                             order_date=datetime.datetime.now())
        for product in post_request['products']:
            OrderState.objects.create(order=userorder,
                                      product=Product.objects.get(pk=product['product']),
                                      quantity=product['quantity'])
        # TODO это лишь заглушка
        return JsonResponse({})
