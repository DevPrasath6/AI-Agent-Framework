from django.contrib import admin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_email_verified', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'job_title', 'timezone')
    list_filter = ('timezone', 'company')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'company', 'job_title')
    ordering = ('-user__created_at',)
