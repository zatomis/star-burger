import datetime

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

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

class OrderStateSerializer(ModelSerializer):
    class Meta:
        model = OrderState
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = OrderStateSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = UserOrder
        fields = ["id", "firstname", "lastname", "address", "phonenumber", "products"]

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


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    try:
        request.data
    except ValueError as error:
        return Response({"Ошибка : ": error}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    userorder = UserOrder.objects.create(
                firstname=serializer.validated_data["firstname"],
                lastname=serializer.validated_data["lastname"],
                phonenumber=serializer.validated_data["phonenumber"],
                address=serializer.validated_data["address"],
                order_date=datetime.datetime.now())

    order_state_fields = serializer.validated_data["products"]
    order_contents = [OrderState(order=userorder, **fields) for fields in order_state_fields]
    OrderState.objects.bulk_create(order_contents)
    return Response(OrderSerializer(userorder).data)
