from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class District(models.Model):
    """Районы"""
    name = models.CharField(max_length=255, verbose_name='Ваш район')
    slug = models.SlugField(unique=False, verbose_name='Url')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Category(models.Model):
    """Категории"""

    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=False, verbose_name='Url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Requester(models.Model):
    """Заказщик"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    slug = models.SlugField(max_length=255, unique=False, verbose_name='Url')
    age = models.CharField(max_length=2, verbose_name='Возраст')
    phone = models.CharField(max_length=11, null=True, verbose_name='Номер телефона')
    photo = models.ImageField(upload_to='images/requesters/', null=True,
                              help_text='Размер фото не должен превышать 50кБайт', verbose_name='Ваше фото')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    class Meta:
        verbose_name = 'Заказщик'
        verbose_name_plural = 'Заказщики'


class Order(models.Model):
    """Заказ"""

    name = models.CharField(max_length=255, verbose_name='заказ')
    slug = models.SlugField(unique_for_date='publish', verbose_name='Url')
    publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, verbose_name='Категория товара')
    description = models.TextField(max_length=255, verbose_name='описание')
    image = models.ImageField(upload_to='images/orders/', null=True, blank=True, verbose_name='Изображения')
    price = models.DecimalField(max_digits=5, null=True, decimal_places=0, verbose_name='Ориентировочная цена')
    district = models.ForeignKey(District, null=True, on_delete=models.PROTECT, verbose_name='Район заказа')
    address = models.CharField(max_length=255, null=True, verbose_name='Адресс заказа')
    requester = models.ForeignKey(Requester, null=True, on_delete=models.CASCADE, verbose_name='заказщик')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-publish', 'name']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ResponseForOrder(models.Model):
    sender = models.ForeignKey('Executor', on_delete=models.CASCADE, verbose_name='Отправитель')
    text = models.TextField(max_length=400, verbose_name='Текст отклика')
    time = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время отклика')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ для отклика')

    def __str__(self):
        return self.order.name

    class Meta:
        verbose_name = 'Отклик для заказа'
        verbose_name_plural = 'Отклики для заказа'


class MyOrders(models.Model):
    """Работы исполнителя"""
    name = models.CharField(max_length=100, verbose_name='Примеры моих работ')
    description = models.TextField(max_length=255, verbose_name='Описание выполненых работы')
    image = models.ImageField(upload_to='images/complete_orders/', null=True, blank=True, verbose_name='Изображения')
    executor = models.ForeignKey('Executor', null=True, on_delete=models.CASCADE, verbose_name='Исполнитель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Выполненый заказ'
        verbose_name_plural = 'Выполненые заказы'


class Executor(models.Model):
    """"Исполнитель"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    slug = models.SlugField(max_length=255, unique=False, verbose_name='Url')
    photo = models.ImageField(upload_to='images/executors/', help_text='Рекомендуем загружать реальные фото',
                              blank=True, null=True, verbose_name='Ваше фото')
    text = models.TextField(max_length=500, null=True, verbose_name='Расскажите о себе')
    age = models.CharField(max_length=2, null=True, blank=True, verbose_name='Возраст')
    phone = models.CharField(max_length=11, null=True, verbose_name='Номер телефона')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 null=True, verbose_name='Выберите категорию для деятельности')
    district = models.ForeignKey(District, on_delete=models.PROTECT,
                                 null=True, verbose_name='Район(ы) выполнение заказов')
    time_work = models.CharField(max_length=255, null=True, verbose_name='Рабочее время')
    days_of_work = models.CharField(max_length=255, null=True, verbose_name='Дни работы')
    education = models.CharField(max_length=255, null=True, blank=True, verbose_name='Образование')
    certificates = models.ImageField(upload_to='image', null=True, blank=True, verbose_name='Мои сертификаты')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

    class Meta:
        verbose_name = 'Исполитель'
        verbose_name_plural = 'Исполнители'



