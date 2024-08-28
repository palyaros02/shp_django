from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden

from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .models import Profile, News, Comment

def index(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для главной страницы. Отображает общую информацию о сайте и последние новости. Информация о количестве пользователей, новостей и комментариев берется из базы данных.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона главной страницы.
    """
    user_count = Profile.objects.count()
    news_count = News.objects.count()
    comment_count = Comment.objects.count()
    latest_news = News.objects.order_by("-created_at")[:5]

    context = {
        "user_count": user_count,
        "news_count": news_count,
        "comment_count": comment_count,
        "latest_news": latest_news,
    }
    return render(request, "index.html", context)


def about(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для страницы "О нас". Отображает информацию о сайте и его создателях.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона страницы "О нас".
    """
    return render(request, "about.html")


def news_list(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для страницы "Все новости". Отображает список всех новостей.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона страницы "Все новости".
    """
    news = News.objects.all()
    return render(request, "news_list.html", {"news": news})


def news_detail(request: WSGIRequest, news_id: int) -> HttpResponse:
    """
    Обработчик запроса для страницы конкретной новости. Отображает выбранную новость и все комментарии к ней.

    :param request: Объект HttpRequest от Django.
    :param news_id: ID новости.
    :return: HttpResponse: Отображение шаблона страницы конкретной новости.
    """
    news_item = News.objects.get(id=news_id)
    comments = news_item.comments.all()
    return render(
        request, "news_detail.html", {"news": news_item, "comments": comments}
    )


def profile_view(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для страницы профиля пользователя. Отображает информацию о пользователе.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона страницы профиля пользователя или запрет доступа.
    """
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return HttpResponseForbidden()


class LoginUser(LoginView):
    """
    Класс представления для входа пользователя в систему.
    Позволяет пользователям войти в систему, используя свои учетные данные.
    """
    pass


def logout_user(request: WSGIRequest):
    """
    Обработчик запроса для выхода пользователя из системы.
    Позволяет пользователю выйти из системы и перенаправляет его на страницу входа.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Перенаправление на страницу входа.
    """
    logout(request)
    return redirect("login")


class RegisterUser(CreateView):
    pass
    """
    Класс представления для регистрации нового пользователя.
    Позволяет новым пользователям зарегистрироваться в системе.
    """