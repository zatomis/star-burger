import datetime

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .models import OrderState, Product, UserOrder


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

    def create(self, validated_data):
        order_items_fields = validated_data.pop('products')
        order = UserOrder.objects.create(**validated_data)
        order_items = [OrderState(order=order, price=fields['product'].price, **fields)
                       for fields in order_items_fields]
        OrderState.objects.bulk_create(order_items)
        return order

    def create1(self, validated_data):
        products_data = validated_data.pop('products')
        userorder = UserOrder.objects.create(**validated_data)
        for product_data in products_data:
            OrderState.objects.create(order=userorder, **product_data)
        return userorder

        order_state_fields = validated_data.pop('products')
        products = [field["product"] for field in order_state_fields]
        prices = {product.id: product.price for product in products}
        order_contents = [OrderState(
            order=userorder,
            price = prices[fields["product"].id],
            **fields) for fields in order_state_fields]
        OrderState.objects.bulk_create(order_contents)

        order_items = [OrderItem(order=order, price=fields['product'].price, **fields)
                       for fields in order_items_fields]
        OrderItem.objects.bulk_create(order_items)
        return order


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


@api_view(['POST'])
@transaction.atomic
def register_order(request):
    try:
        request.data
    except ValueError as error:
        return Response({"Ошибка : ": error}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    userorder = serializer.save()
    return Response(OrderSerializer(userorder).data)
