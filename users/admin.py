from django.contrib import admin
from users.models import Member


# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('nick', 'username', 'email', 'password', 'avatar', 'rating')

admin.site.register(Member, MemberAdmin)
