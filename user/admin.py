from django.contrib import admin
from django.db import models
from .models import UserModel
from django.forms import TextInput

admin.site.site_title = 'E-World Title'
admin.site.site_header = 'E-World Header'
admin.site.index_title = 'Models'

class UserModelAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.EmailField: {'widget': TextInput(attrs={'size':'25'})},
    }

    list_display = ['username', 'email', 'balance']
    list_editable = ['balance']
    list_display_links = ['id', 'username', 'email']
    search_fields = ['id', 'username']
    list_per_page = 20
    search_help_text = 'Search User by id or username'
    readonly_fields = ['view_profile_photo']
    
    fields = (
        ('username'),
        ('password'),
        ('email'),
        ('first_name', 'last_name'),
        ('balance'),
        ('cards'),
        ('profile_photo', 'view_profile_photo'),
        ('is_active', 'is_staff', 'is_superuser'),
        ('last_login', 'date_joined')
    )

    filter_horizontal = ["cards"]

    def set_balance(self, request, queryset):
        count = queryset.update(balance=100)
        self.message_user(request, f'You set the balance of {count} user to 100.')
    
    actions = ('set_balance',)
    set_balance.short_description = "Set selected users' balance to 100"

    def view_profile_photo_in_list(self, obj):
        from django.utils.safestring import mark_safe
        if obj.profile_photo:
            return mark_safe(f'<img src={obj.profile_photo.url} style="height:75px; width:75px;"></img>')
        return '-*-'

    list_display = ['id', 'view_profile_photo_in_list'] + list_display
    view_profile_photo_in_list.short_description = 'PROFILE PHOTO'

admin.site.register(UserModel, UserModelAdmin)
