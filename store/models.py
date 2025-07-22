from django.db import models
from user.models import User


class Camera (models.Model):
    name = models.CharField(
        max_length=255,
        null= True,
        blank= True,
        verbose_name='نام')

    resolution = models.CharField(
        max_length=255,
        null= True,
        blank= True,
        verbose_name='رزولوشن')

    description = models.TextField(
        null= True,
        blank= True,
        verbose_name='توضیحات')
    
    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = ("دوربین")
        verbose_name_plural = ("دوربین ها")

    def __str__(self):
        return self.name


class Picture (models.Model):
    file = models.FileField(
        upload_to=('product/picture/'),
        null=True,
        blank=True,
        verbose_name='تصویر'
    )

    name =  models.CharField(
        max_length=255,
        null= True,
        blank= True,
        verbose_name='نام تصویر')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name = ("تصویر")
        verbose_name_plural = ("تصاویر")

    def __str__(self):
        return self.name


class Product (models.Model):
    seller = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='product_seller',
        verbose_name='فروشنده'
    )

    name = models.CharField(
        max_length=255,
        null= True,
        blank= True,
        verbose_name='نام محصول')

    description = models.TextField(
        null= True,
        blank= True,
        verbose_name='توضیحات')

    price = models.IntegerField(
        null= True,
        blank= True,
        verbose_name='قیمت')

    brand  =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='برند')

    color =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='رنگ')

    camera = models.ManyToManyField(
        Camera,
        null=True,
        related_name='product_cmaera',
        verbose_name='دوربین'
    )

    picture = models.ManyToManyField(
        Picture,
        null=True,
        related_name='product_picture',
        verbose_name='تصاویر'
    )

    part_number =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='پارت نامبر')

    ram =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='حافظه')

    sim_card =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='تعداد سیم کارت')

    battry =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='باتری')

    battry_health =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='سلامت باتری')

    battry_change =models.BooleanField (
        default= False,
        verbose_name='باتری تعویض شده'
    )

    size =models.CharField(
        max_length=256,
        null= True,
        blank= True,
        verbose_name='سایز')

    charger =models.BooleanField (
        default= False,
        verbose_name='شارژر'
    )

    carton =models.BooleanField (
        default= False,
        verbose_name='کارتن'
    )

    TYPE_PRODUCT = [
        ('new','نو'),
        ('as new','در حد نو'),
        ('used','دست دوم'),
    ]

    type_product =models.CharField(
        max_length=25,
        choices=TYPE_PRODUCT,
        null= True,
        blank= True,
        verbose_name='وضعیت محصول')

    technical_problem = models.TextField(
        null= True,
        blank= True,
        verbose_name='مشکل فنی')

    hit_product = models.BooleanField (
        default= False,
        verbose_name='ضرب خوردگی'
    )

    register_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ رجیستری'
    )

    registered = models.BooleanField (
        default= False,
        verbose_name='رجیستر شده'
    )

    GUARANTOR = [
        ('guarantor','گارانتی'),
        ('guarantor_registered','رجیستر شده و گارانتی'),
        ('disregistered','بدون رجیستری')
    ]
    guarantor = models.CharField(
        max_length=25,
        choices=GUARANTOR,
        null= True,
        blank= True,
        verbose_name='گارانتی و رجیستری ')


    repaired = models.BooleanField (
        default= False,
        verbose_name='تعمیر شده'
    )

    STATUS_PRODUCT =[
        ('open','باز'),
        ('saled','فروخته شده'),
        ('canseled','کنسل شده'),
        ('reserved','رزرو'),
    ]

    status_product = models.CharField(
        max_length=25,
        choices=STATUS_PRODUCT,
        default='open',
        null= True,
        blank= True,
        verbose_name='وضعیت فروش محصول')

    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = ("محصول")
        verbose_name_plural = ("محصولات")
        permissions = [('can_create_products','می تواند محصولات را ایجاد کند'),('can_update_products','می تواند محصولات را بروزرسانی کند'),('can_delete_products','می تواند محصولات را حذف کند')]

    def __str__(self):
        return self.name


class Order (models.Model) :
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_product',
        verbose_name='محصول'
    )

    buyer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_buyer',
        verbose_name='خریدار'
    )

    seller = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='order_seller',
        verbose_name='فروشنده'
    )

    sell_date =models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ فروش'
    )

    STATUS =[
        ('approved','تکمیل سفارش'),
        ('confirmed','تایید سفارش'),
        ('ordering','در حال سفارش'),
        ('canceled','کنسل شده'),
    ]
    status =models.CharField(
        max_length=25,
        choices=STATUS,
        null= True,
        blank= True,
        verbose_name='وضعیت سفارش')
    
    created_at = models.DateTimeField(
        auto_now_add=True)

    updated_at = models.DateTimeField(
        auto_now=True)


    class Meta:
        verbose_name = ("سفارش")
        verbose_name_plural = ("سفارشات")
        permissions = [('can_see_all_orders','می تواند همه سفارشات را ببیند') , ('can_update_order','می تواند سفارشات را بروزرسانی کند')]

    def __str__(self):
        return f"Order: {self.product.name} by {self.buyer.username} from {self.seller.username}"
