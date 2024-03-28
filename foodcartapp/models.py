from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count, F, Sum
from django.utils import timezone
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
    # longitude = models.FloatField(
    #     'Долгота',
    #     null=True,
    #     blank=True,
    # )
    # latitude = models.FloatField(
    #     'Широта',
    #     null=True,
    #     blank=True,
    # )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects.filter(availability=True)
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


class OrderStateQuerySet(models.QuerySet):

    def get_unique_user_id(self):
        user_id = set()
        for product in self:
            user_id.add(product.order.id)
        return list(user_id)


class OrderQuerySet(models.QuerySet):

    def total_count(self):
        return self.annotate(total_count_position=Count(F("order_states")))

    def total_price(self):
        return self.annotate(
            total_price=Sum(F("order_states__price"))
        )


class UserOrder(models.Model):
    ORDER_CHOICES = (
        (-1, 'Заказ выполнен'),
        (0, 'Необработанный'),
        (1, 'Принят в работу'),
        (2, 'Заказ на сборке'),
        (3, 'Передан курьеру'),
    )
    PAYMENT_METHOD = ((False, '💰'), (True, '💳'))

    firstname = models.CharField('Имя', max_length=50, null=False)
    lastname = models.CharField('Фамилия', max_length=50, null=False)
    address = models.CharField('Адрес заказа', max_length=250, null=False)
    phonenumber = PhoneNumberField('Номер ☎️', region='RU', blank=True, null=True, default='-')
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    status = models.SmallIntegerField(default=0, verbose_name='Статус заказа', choices=ORDER_CHOICES, db_index=True)
    registr_date = models.DateTimeField(help_text="Дата регистрации заказа", blank=True, default=timezone.now,
                                        editable=False, verbose_name='Заказ')
    call_date = models.DateTimeField(help_text="Дата звонка", blank=True, verbose_name='Созвон')
    delivered_date = models.DateTimeField(help_text="Дата доставки", blank=True, verbose_name='Доставка')
    payment = models.BooleanField(default=True, verbose_name='Оплата', choices=PAYMENT_METHOD, db_index=True)
    available_restaurants = models.ManyToManyField(
        Restaurant,
        verbose_name="доступные рестораны",
        blank=True
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def save(self, *args, **kwargs):
        if not self.available_restaurants.all():
            if self.status == 0:
                self.status = self.status + 1
        super(UserOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.firstname} {self.correct_phone_number(self.phonenumber)}' \
               f' ({self.get_status_display()}) - id {self.id}'

    @classmethod
    def correct_phone_number(cls, number):
        return ' ☎️ 8('+str(number)[2:5]+')'+str(number)[5:8]+'-'+str(number)[8:10]+'-'+str(number)[10:]


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

    objects = OrderStateQuerySet.as_manager()

    class Meta:
        verbose_name = 'Состояние заказа'
        verbose_name_plural = 'Заказы из корзины'

    def __str__(self):
        return f'{self.product} [{self.quantity}]'
