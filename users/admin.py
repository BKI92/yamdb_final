from django.contrib import admin

# Register your models here.
from users.models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'bio')
    fields = ('username', 'email', 'role', 'first_name', 'last_name', 'bio')
    search_fields = ('username', 'email', 'role')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, UserAdmin)
