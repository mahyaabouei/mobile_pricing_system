from django.contrib import admin
from .models import Camera, Picture, Product, Order


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('name', 'resolution')
    search_fields = ('name', 'resolution')
    list_filter = ('resolution',)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller','brand', 'price', 'color', 'type_product', 'status_product', 'registered', 'guarantor')
    search_fields = ('name', 'brand', 'part_number')
    list_filter = ('type_product', 'status_product', 'brand', 'registered', 'guarantor', 'repaired', 'hit_product')
    list_editable = ('status_product', 'registered')
    ordering = ('-id',)
    autocomplete_fields = ('camera', 'picture')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'brand', 'color')}),
        ('اطلاعات فنی', {
            'fields': (
                'camera', 'picture', 'part_number', 'ram', 'sim_card',
                'battry', 'battry_health', 'battry_change',
                'size', 'charger', 'carton'
            )
        }),
        ('فروشنده', {
            'fields': ('seller',)
        }),
        ('وضعیت محصول', {
            'fields': (
                'type_product', 'technical_problem', 'hit_product',
                'register_date', 'registered', 'guarantor', 'repaired', 'status_product'
            )
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'seller', 'sell_date', 'status')
    search_fields = ('product__name', 'buyer__username', 'seller__username')
    list_filter = ('status', 'sell_date')
    autocomplete_fields = ('product', 'buyer', 'seller')
    ordering = ('-sell_date',)
