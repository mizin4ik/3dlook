from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'birthday')
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'username', 'first_name', 'last_name', 'email')

    fields = (
        'date_joined', 'last_login', 'username', 'first_name', 'last_name',
        'email', 'avatar', 'birthday', 'is_active', 'is_staff', 'is_superuser',
        'groups', 'user_permissions'
    )

    readonly_fields = ('date_joined', 'last_login', )
