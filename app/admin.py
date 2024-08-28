from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, News, Comment

class ProfileInline(admin.StackedInline):
    """
    Класс для отображения профиля пользователя в административной панели Django.
    """
    model = Profile
    can_delete = False
    verbose_name = "Профиль"


class UserAdmin(BaseUserAdmin):
    """
    Класс для отображения пользователей в административной панели Django.
    """
    inlines = (ProfileInline,)
    list_display = ("username", "email", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)

class ProfileAdmin(admin.ModelAdmin):
    """
    Класс для отображения профилей пользователей в административной панели Django.
    """
    list_display = ("user", "full_name", "email", "birth_date")
    search_fields = ("user__username", "full_name", "email")
    verbose_name = "Профиль"
    verbose_name_plural = "Профили"


class NewsAdmin(admin.ModelAdmin):
    """
    Класс для отображения новостей в административной панели Django.
    """
    list_display = ("title", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "author__full_name", "description")
    prepopulated_fields = {"title": ("description",)}
    verbose_name = "Новость"
    verbose_name_plural = "Новости"


class CommentAdmin(admin.ModelAdmin):
    """
    Класс для отображения комментариев к новостям в административной панели Django.
    """
    list_display = ("author", "news", "created_at")
    search_fields = ("author__full_name", "news__title", "text")
    list_filter = ("created_at",)
    verbose_name = "Комментарий"
    verbose_name_plural = "Комментарии"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)