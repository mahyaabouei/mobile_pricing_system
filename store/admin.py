from django.contrib import admin

from .models import Picture, Product, Order, ModelMobile, Color


@admin.register(Color)
class CoLorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'seller', 'price', 'color', 'type_product', 'status_product', 'guarantor')
    list_filter = ('type_product', 'status_product', 'guarantor', 'repaired', 'hit_product')
    list_editable = ('status_product',)
    ordering = ('-id',)
    search_fields = ('description', 'color', 'ram', 'guarantor')
    fieldsets = (
        (None, {'fields': ( 'description', 'price', 'color')}),
        ('اطلاعات فنی', {
            'fields': (
                'ram', 'sim_card',
                'battry_health', 'battry_change',
                'size'
            )
        }),
        ('فروشنده', {
            'fields': ('seller',)
        }),
        ('وضعیت محصول', {
            'fields': (
                'type_product', 'technical_problem', 'hit_product',
                'guarantor', 'repaired', 'status_product'
            )
        }),
        ('تصاویر', {
            'fields': ('picture',)
        }),

    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'seller', 'sell_date', 'status')
    search_fields = ('product__name', 'buyer__username', 'seller__username')
    list_filter = ('status', 'sell_date')
    autocomplete_fields = ('product', 'buyer', 'seller')
    ordering = ('-sell_date',)


@admin.register(ModelMobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'brand', 'get_colors', 'is_apple', 'link')
    list_filter = ('is_apple',)
    ordering = ('-id',)
    search_fields = ('model_name', 'brand', 'link')
    fieldsets = (
        (None, {'fields': ('model_name', 'brand', 'colors', 'is_apple', 'registered', 'link')}),
        ('تصاویر', {
            'fields': ('picture',)
        }),
    )
    
    def get_colors(self, obj):
        return ', '.join([color.name for color in obj.colors.all()])
    get_colors.short_description = 'رنگ‌ها'

