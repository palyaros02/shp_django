from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile, News, Comment, User
from .forms import LoginUserForm, RegisterUserForm, EditUserProfileForm

def index(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для главной страницы. Отображает общую информацию о сайте и последние новости. Информация о количестве пользователей, новостей и комментариев берется из базы данных.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона главной страницы.
    """
    user_count = User.objects.count() - 1 # админа не учитываем
    news_count = News.objects.count()
    comment_count = Comment.objects.count()
    latest_news = News.objects.order_by("-created_at")[:3]

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
    news = News.objects.order_by("-created_at")
    return render(request, "news_list.html", {"news_list": news})


def news_detail(request: WSGIRequest, news_id: int) -> HttpResponse:
    """
    Обработчик запроса для страницы конкретной новости. Отображает выбранную новост, лайки, просмотры,
    комментарии и форму для добавления комментария.

    :param request: Объект HttpRequest от Django.
    :param news_id: ID новости.
    :return: HttpResponse: Отображение шаблона страницы конкретной новости.
    """
    news = get_object_or_404(News, id=news_id)

    # Обновляем количество просмотров
    news.views += 1
    news.save()

    # Обработка формы добавления комментария
    if request.method == 'POST':
        if request.user.is_authenticated:
            text = request.POST.get('text')
            if text:
                Comment.objects.create(news=news, author=request.user.profile, text=text)
                return redirect('news_detail', news_id=news_id)
        else:
            return redirect('login')

    comments = news.comments.all()

    context = {
        'news': news,
        'comments': comments,
    }
    return render(request, 'news_detail.html', context)

@login_required
def profile_view(request: WSGIRequest) -> HttpResponse:
    """
    Обработчик запроса для страницы профиля пользователя. Отображает информацию о пользователе.

    :param request: Объект HttpRequest от Django.
    :return: HttpResponse: Отображение шаблона страницы профиля пользователя или запрет доступа.
    """
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Перенаправление на главную после сохранения
    else:
        form = EditUserProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form})


class LoginUser(LoginView):
    """
    Класс представления для входа пользователя в систему.
    Позволяет пользователям войти в систему, используя свои учетные данные.
    """
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')



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
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = Profile(user=user, full_name=form.cleaned_data['full_name'], email=form.cleaned_data['email'], bio=form.cleaned_data['bio'], birth_date=form.cleaned_data['birth_date'], )
        profile.save()
        login(self.request, user)
        return redirect('index')