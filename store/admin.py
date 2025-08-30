from django.contrib import admin

from .models import Picture, Product, Order, ModelMobile, Color, PardNumber                                                             


@admin.register(Color)
class CoLorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')
    search_fields = ('name',)

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'seller', 'price', 'color', 'type_product', 'status_product', 'guarantor', 'auction', 'created_at')
    list_filter = ('type_product', 'status_product', 'guarantor', 'repaired', 'auction', 'battry_change', 'model_mobile')
    list_editable = ('status_product', 'price')
    ordering = ('-created_at',)
    search_fields = ('description', 'part_num', 'seller__username')
    autocomplete_fields = ('seller', 'model_mobile', 'color')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('model_mobile', 'description', 'price', 'color')
        }),
        ('توضیحات تکمیلی', {
            'fields': ('description_appearance', 'technical_problem'),
            'classes': ('collapse',)
        }),
        ('اطلاعات فنی', {
            'fields': (
                'battry_health', 'battry_change',
                'part_num', 'carton'
            )
        }),
        ('فروشنده', {
            'fields': ('seller',)
        }),
        ('وضعیت و تنظیمات', {
            'fields': (
                'type_product', 'status_product',
                'guarantor', 'repaired', 'auction'
            )
        }),
        ('تصاویر', {
            'fields': ('picture',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_product_name(self, obj):
        if obj.model_mobile:
            return f"{obj.model_mobile.brand} {obj.model_mobile.model_name}"
        return f"محصول {obj.id}"

    get_product_name.short_description = 'نام محصول'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'buyer', 'seller', 'sell_date', 'status')
    search_fields = ('product__description', 'buyer__username', 'seller__username')
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
        (None, {'fields': ('model_name', 'brand', 'colors', 'is_apple', 'link')}),
        ('تصاویر', {
            'fields': ('picture',)
        }),
    )
    
    def get_colors(self, obj):
        return ', '.join([color.name for color in obj.colors.all()])
    get_colors.short_description = 'رنگ‌ها'

@admin.register(PardNumber)
class PardNumberAdmin(admin.ModelAdmin):
    list_display = ('pard_number', 'description', 'created_at', 'updated_at')
    search_fields = ('pard_number', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
