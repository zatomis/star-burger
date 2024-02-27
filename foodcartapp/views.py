from django.http import JsonResponse
from django.templatetags.static import static

import json
from .models import Product


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
    post_data_request = json.loads(request.body.decode())
    print(post_data_request)
    print(post_data_request['products'])

    # {'products': [{'product': 4, 'quantity': 3}, {'product': 3, 'quantity': 1}, {'product': 2, 'quantity': 1},
    #               {'product': 1, 'quantity': 3}], 'firstname': 'Иван', 'lastname': 'Ван', 'phonenumber': '+79287778111',
    #  'address': 'Москва, пл. Киевского Вокзала, 2'}

    # {'products':
    #      [{'product': 4, 'quantity': 1}],
    #      'firstname': 'Иван',
    #      'lastname': 'g',
    #      'phonenumber': '+79287778111',
    #      'address': 'Франция, ул.Розовых Цветов 12'}



    # TODO это лишь заглушка
    return JsonResponse({})
