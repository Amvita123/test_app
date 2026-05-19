from django.contrib import admin
from users.models.users import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'email_verified', 'sms_verified')

admin.site.register(User, UserAdmin)