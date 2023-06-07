from django.contrib import admin
from .models import CustomUser


uneditable_fields = ('id', 'date_created', 'date_updated')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'is_staff',
        'is_active',
        'date_joined'
    )
    fields = [field.name for field in CustomUser._meta.fields if field.name not in uneditable_fields]
