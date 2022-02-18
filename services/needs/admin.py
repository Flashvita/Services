from django.contrib import admin

from .models import Requester, Order, Category, District, Executor, ResponseForOrder, MyOrders


class AdminDistrict(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'id')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'district', 'requester', 'id', 'publish', )
    list_filter = ('category', 'district', 'publish')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class RequesterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'id',)
    prepopulated_fields = {'slug': ('user',)}


class ExecutorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('user',)}
    list_display = ('__str__', 'user', 'id', )


class CategorySlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class MyOrderAdmin(admin.ModelAdmin):

    list_display = ('name',)


admin.site.register(MyOrders, MyOrderAdmin)
admin.site.register(Requester, RequesterAdmin)
admin.site.register(Executor, ExecutorAdmin)
admin.site.register(District, AdminDistrict)
admin.site.register(Category, CategorySlug)
admin.site.register(Order, OrderAdmin)
admin.site.register(ResponseForOrder)
