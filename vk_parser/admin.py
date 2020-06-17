from django import forms
from django.contrib import admin
from .models import Cities, VKGroups, ProductСategory

admin.site.register(Cities)
admin.site.register(ProductСategory)


class VKGroupsAdminForm(forms.ModelForm):
    class Meta:
        model = VKGroups
        fields = '__all__'


class VKGroupsAdmin(admin.ModelAdmin):
    form = VKGroupsAdminForm
    list_display = ('title', 'city', 'created')
    list_filter = ('city', 'created')
    search_fields = ('title', 'city', 'chat_id')
    date_hierarchy = 'created'
    ordering = ('created', 'city')


admin.site.register(VKGroups, VKGroupsAdmin)
