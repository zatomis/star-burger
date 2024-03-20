from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count, F, Sum
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

class OrderQuerySet(models.QuerySet):

    def total_count(self):
        return self.annotate(total_count_position=Count(F("order_states")))

    def total_price(self):
        return self.annotate(
            total_price=Sum(F("order_states__quantity") * F("order_states__product__price"))
        )

class UserOrder(models.Model):
    firstname = models.CharField('Имя пользователя заказа', max_length=50, null=False)
    lastname = models.CharField('Фамилия пользователя заказа', max_length=50, null=False)
    address = models.CharField('Адрес для заказа', max_length=250, null=False)
    phonenumber = PhoneNumberField('Номер телефона', region='RU', blank=True, null=True)
    order_date = models.DateTimeField(help_text="Дата заказа", default=now, editable=False, verbose_name='Дата заказа')
    comments = models.TextField(verbose_name="Комментарий", blank=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} т.{self.phonenumber} от ({self.order_date})'


class OrderState(models.Model):
    order = models.ForeignKey(UserOrder, verbose_name="заказ", on_delete=models.CASCADE, related_name="order_states")
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE, related_name="orders")
    quantity = models.SmallIntegerField(default=0, verbose_name='Кол-во заказа')
    price = models.DecimalField(
        verbose_name="стоимость позиции",
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=7,
        blank=True,
    )
    class Meta:
        verbose_name = 'Состояние заказа'
        verbose_name_plural = 'Заказы из корзины'

    def __str__(self):
        return f'{self.product} [{self.quantity}]'
