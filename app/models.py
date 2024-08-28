from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Модель профиля пользователя. Связана с встроенной моделью пользователя User (username, password) через отношение один к одному. Служит для хранения дополнительной информации о пользователе, такой как

    user: Связь с моделью User.
    full_name: Полное имя пользователя. (мах. 255 символов)
    birth_date: Дата рождения пользователя. (необязательное поле)
    email: Адрес электронной почты пользователя. (уникальное поле)
    bio: Биография пользователя. (необязательное поле)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

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
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Модель комментария к новости. Связана с моделью новости News и моделью профиля пользователя Profile через отношения многие к одному. Содержит информацию о комментарии, такую как:

    news: Связь с моделью News через отношение многие к одному.
    author: Связь с моделью Profile, многие к одному.
    text: Текст комментария. (неограниченное поле)
    created_at: Дата и время создания комментария. (автоматически заполняемое поле)
    """
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий пользователя {self.author.user.username} к статье "{self.news.title}"'
