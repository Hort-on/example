from django.contrib import admin
from authentication.models import CustomUser



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'first_name', 'last_name', 'is_superuser', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'last_name']
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = [
        ("Personal information", {"fields": ["first_name", "middle_name", "last_name", "email", "password"]}),
        ("Permission information", {"fields": [("role", "is_staff", "is_superuser")]}),
        ("Date information", {"fields": ('created_at', 'updated_at')})
    ]

    def save_model(self, request, obj, form, change):
        # Hash the password before saving the user
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)

