from django.contrib import admin
from .models import MenuPoint


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url')
    list_filter = ('name', 'parent')


admin.site.register(MenuPoint, MenuItemAdmin)

