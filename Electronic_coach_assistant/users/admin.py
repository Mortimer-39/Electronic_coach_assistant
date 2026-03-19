from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Как отображать список
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']

    # Как группировать поля при редактировании
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация CRM', {'fields': ('phone_number', 'address', 'discount', 'role', 'avatar')}),
    )
    # Поля при создании (регистрации через админку)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
    )

    ordering = ('email',)
