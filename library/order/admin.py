from django.contrib import admin
from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'end_at']
    list_filter = ['end_at']


admin.site.register(Order, OrderAdmin)
