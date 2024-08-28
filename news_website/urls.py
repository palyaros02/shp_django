from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    # Маршрут к административной панели Django.
    path('admin/', admin.site.urls),

    # Маршрут к главной странице.
    path('', views.index, name='index'),

    # Маршрут к "О нас"
    path('about/', views.about, name='about'),

    # Маршрут к "Все новости"
    path('news/', views.news_list, name='news_list'),

    # Маршрут к конкретной новости
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),

    # Маршрут к странице входа
    path('login/', views.LoginUser.as_view(), name='login'),

    # Маршрут к выходу
    path('logout/', views.logout_user, name='logout'),

    # Маршрут к странице регистрации
    path('register/', views.RegisterUser.as_view(), name='register'),

    # Маршрут к профилю
    path('profile/', views.profile_view, name='profile'),
]
