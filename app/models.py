from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Модель профиля пользователя. Связана с встроенной моделью пользователя User (username, password) через отношение один к одному. Служит для хранения дополнительной информации о пользователе, такой как

    user: Связь с моделью User.
    full_name: Полное имя пользователя. (мах. 255 символов)
    birth_date: Дата рождения пользователя. (необязательное поле)
    email: Адрес электронной почты пользователя. (уникальное поле)
    bio: Биография пользователя. (необязательное поле)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    email = models.EmailField(unique=True, verbose_name='Email')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.full_name

class News(models.Model):
    """
    Модель новости. Связана с моделью профиля пользователя Profile через отношение многие к одному. Содержит информацию о новости, такую как

    author: Связь с моделью Profile.
    image: Изображение в шапке новости. Хранится в папке news_images/ внутри папки media. (необязательное поле)
    title: Заголовок новости. (мах. 255 символов)
    description: Описание новости. (неограниченное поле)
    created_at: Дата и время создания новости. (автоматически заполняемое поле)
    updated_at: Дата и время последнего обновления новости. (автоматически заполняемое поле)
    likes: Количество лайков новости. (положительное целое число)
    views: Количество просмотров новости. (положительное целое число)

    comments: Связь с моделью Comment через отношение один ко многим по обратному отношению. Позволяет получить все комментарии к новости.

    """
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='news', verbose_name='Автор')
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Текст статьи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ('-created_at', '-updated_at', 'title', 'author', 'views')


    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    """
    Модель комментария к новости. Связана с моделью новости News и моделью профиля пользователя Profile через отношения многие к одному. Содержит информацию о комментарии, такую как:

    news: Связь с моделью News через отношение многие к одному.
    author: Связь с моделью Profile, многие к одному.
    text: Текст комментария. (неограниченное поле)
    created_at: Дата и время создания комментария. (автоматически заполняемое поле)
    """
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE, verbose_name='Новость')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Комментарий пользователя {self.author.user.username} к статье "{self.news.title}"'


class Like(models.Model):
    """
    Модель лайка к новости. Связана с моделью пользователя User и моделью новости News через отношение многие ко многим. Служит для хранения информации о лайках к новостям, такой как:

    user: Связь с моделью User.
    news: Связь с моделью News.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    news = models.ForeignKey(News, related_name='likes', on_delete=models.CASCADE, verbose_name='Новость')

    class Meta:
        unique_together = ('user', 'news')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f'{self.user.username} likes {self.news.title}'
