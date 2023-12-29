from django.contrib import admin
from django.db import models
from .models import Card, Faction
from django.forms import TextInput, Textarea


class CardModelAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':60})},
    }

    list_display = ['cardname', 'faction', 'power', 'price']
    list_editable = ['price']
    list_display_links = ['id', 'cardname']
    search_fields = ['id', 'cardname']
    search_help_text = 'Search Card by id or username'
    readonly_fields = ['view_image']
    
    fields = (
        ('cardname'),
        ('detail'),
        ('faction'),
        ('power', 'price'),
        ('image', 'view_image'),
    )

    def view_image_in_list(self, obj):
        from django.utils.safestring import mark_safe
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} style="height:80px; width:60px;"></img>')
        return '-*-'

    list_display = ['id', 'view_image_in_list'] + list_display
    view_image_in_list.short_description = 'Image'


class FactionModelAdmin(admin.ModelAdmin):
     
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':60})},
    }
     
    list_display = ['faction_name']
    list_display_links = ['id', 'faction_name']
    readonly_fields = ['view_flag']
    
    fields = (
        ('faction_name'),
        ('history'),
        ('flag', 'view_flag'),
    )

    def view_flag_in_list(self, obj):
        from django.utils.safestring import mark_safe
        if obj.flag:
            return mark_safe(f'<img src={obj.flag.url} style="height:80px; width:60px;"></img>')
        return '-*-'

    list_display = ['id', 'view_flag_in_list'] + list_display
    view_flag_in_list.short_description = 'Flag'

admin.site.register(Card, CardModelAdmin)
admin.site.register(Faction, FactionModelAdmin)