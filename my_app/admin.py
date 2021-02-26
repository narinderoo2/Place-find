from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(facility)


#for set the view on admine panel of account model
class AccountAdmin(UserAdmin):
    list_display=('id','email','username','date_joined','last_login','is_admin','is_staff','city','state','country','adress')
    search_fields=('email','fullname',)
    readonly_fields=('date_joined','last_login')

    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)

#Profile model registerd
admin.site.register(Profile)


