from django.contrib import admin
from store.models import Product, Category


# admin.site.register(Product)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'is_available', 'total_price')
    # list_display_links = ('name', 'price', 'quantity')
    list_editable = ('price', 'quantity', 'is_available')
    # list_filter = ('is_available',)
    search_fields = ('name', 'description')
    # readonly_fields = ('quantity',)

    actions = ('make_available', 'make_not_available')

    @admin.action(description='Mark as available')
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Mark as not available')
    def make_not_available(self, request, queryset):
        queryset.update(is_available=False)

    @admin.display(description='Total Price')
    def total_price(self, obj):
        return obj.price * obj.quantity