from django.contrib import admin

from .models import Order  


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'total', 'is_shipped')
    search_fields = ('order_id', 'total')
    list_filter = ('status',)
    list_editable = ('is_shipped',)
    class Meta:
        model = Order

    def save_model(self, request, obj, form, change):
        if obj.is_shipped:
            obj.status='shipped'
        super().save_model(request, obj, form, change)


admin.site.register(Order, OrderAdmin)
