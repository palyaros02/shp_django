from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Comment, Like, News, Profile


class ProfileInline(admin.StackedInline):
    """
    Класс для отображения профиля пользователя в административной панели Django.
    """

    model = Profile
    can_delete = False


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
    list_filter = ("full_name",)


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ("user",)


class NewsAdmin(admin.ModelAdmin):
    """
    Класс для отображения новостей в административной панели Django.
    """

    list_display = (
        "title",
        "author",
        "created_at",
        "updated_at",
        "like_count",
        "views",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "author__full_name", "description")
    inlines = [LikeInline]
    prepopulated_fields = {"title": ("description",)}

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = "Количество лайков"


class CommentAdmin(admin.ModelAdmin):
    """
    Класс для отображения комментариев к новостям в административной панели Django.
    """

    list_display = ("author", "news", "created_at")
    search_fields = ("author__full_name", "news__title", "text")
    list_filter = ("author", "created_at")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
