from django import forms
from django.contrib import admin
from .models import TGUsers


class TGUsersAdminForm(forms.ModelForm):
    class Meta:
        model = TGUsers
        fields = '__all__'


class ArticlesAdmin(admin.ModelAdmin):
    form = TGUsersAdminForm
    list_display = ('chat_id', 'city', 'created')
    list_filter = ('city', 'created')
    search_fields = ('city', 'chat_id')
    date_hierarchy = 'created'
    ordering = ('created',)


admin.site.register(TGUsers, ArticlesAdmin)
