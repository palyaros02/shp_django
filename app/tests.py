from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Profile, News, Like, Comment
from django.urls import reverse
from app.forms import RegisterUserForm, LoginUserForm, EditUserProfileForm

### Тесты моделей ###
class ProfileModelTest(TestCase):
    def setUp(self):
        # Создание пользователя и профиля
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, full_name='Test User')

    def test_profile_creation(self):
        # Проверка создания профиля пользователя
        self.assertEqual(self.profile.full_name, 'Test User')
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str(self):
        # Проверка метода __str__ модели Profile
        self.assertEqual(str(self.profile), 'Test User')

class NewsModelTest(TestCase):
    def setUp(self):
        # Создание пользователя и профиля
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, full_name='Test User')
        self.news = News.objects.create(author=self.profile, title='Test News', description='This is a test news.')

    def test_news_creation(self):
        # Проверка создания новости
        self.assertEqual(self.news.title, 'Test News')
        self.assertEqual(self.news.description, 'This is a test news.')
        self.assertEqual(self.news.like_count(), 0)

    def test_news_like_count(self):
        # Проверка создания лайка для новости
        Like.objects.create(user=self.user, news=self.news)
        self.assertEqual(self.news.like_count(), 1)

    def test_news_str(self):
        # Проверка метода __str__ модели News
        self.assertEqual(str(self.news), 'Test News')

class CommentModelTest(TestCase):
    def setUp(self):
        # Создание пользователя и профиля
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, full_name='Test User')
        self.news = News.objects.create(author=self.profile, title='Test News', description='This is a test news.')

    def test_comment_creation(self):
        # Проверка создания комментария
        comment = Comment.objects.create(news=self.news, author=self.profile, text='Test comment.')
        self.assertEqual(comment.text, 'Test comment.')
        self.assertEqual(comment.news, self.news)
        self.assertEqual(comment.author, self.profile)

### ======= ###

### Тесты форм ###

class RegisterFormTest(TestCase):
    def test_register_form_valid(self):
        # Тест формы регистрации с валидными данными
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'New User',
            'birth_date': '2000-01-01',
            'bio': 'Test bio',
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_password_mismatch(self):
        # Тест формы регистрации с невалидными данными (пароли не совпадают)
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
            'full_name': 'New User',
            'birth_date': '2000-01-01',
            'bio': 'Test bio',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_form_invalid_username_exists(self):
        # Тест формы регистрации с невалидными данными (пользователь с таким именем уже существует)
        User.objects.create_user(username='newuser', password='12345')
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'full_name': 'New User',
            'birth_date': '2000-01-01',
            'bio': 'Test bio',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_register_form_invalid_email_exists(self):
        # Тест формы регистрации с невалидными данными (пользователь с таким email уже существует)
        User.objects.create_user(username='newuser', password='12345', email='existed@mail.com')
        form_data = {
            'username': 'newuser2',
            'email': 'existed@mail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'full_name': 'New User',
            'birth_date': '2000-01-01',
            'bio': 'Test bio',
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('email', form.errors)

class LoginFormTest(TestCase):
    def test_login_form_valid(self):
        # Тест формы входа с валидными данными
        user = User.objects.create_user(username='testuser', password='12345')
        form_data = {
            'username': 'testuser',
            'password': '12345',
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        # Тест формы входа с невалидными данными
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

class EditUserProfileFormTest(TestCase):
    def setUp(self):
        # Создание пользователя и профиля
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, full_name='Test User')

    def test_edit_user_profile_form_valid(self):
        # Тест формы редактирования профиля с валидными данными
        self.client.force_login(self.user)
        form_data = {
            'username': self.user.username,
            'full_name': 'New Full Name',
            'birth_date': '2000-01-01',
            'email': 'test@test.com',
            'bio': 'New bio',
        }
        form = EditUserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_edit_user_profile_form_invalid_email_exists(self):
        # Тест формы редактирования профиля с невалидными данными (пользователь с таким email уже существует)
        User.objects.create_user(username='newuser', password='12345', email='test@test.com')
        form_data = {
            'username': 'newuser2',
            'full_name': 'New Full Name',
            'birth_date': '2000-01-01',
            'email': 'test@test.com',
            'bio': 'New bio',
        }
        form = EditUserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        self.assertNotIn('email', form.errors)

### ======= ###

### Тесты представлений ###
class ViewsTest(TestCase):
    def setUp(self):
        # Создание пользователя, профиля и новости
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, full_name='Test User')
        self.news = News.objects.create(author=self.profile, title='Test News', description='This is a test news.')

    def test_index_view(self):
        # Проверка доступности главной страницы
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_news_list_view(self):
        # Проверка доступности страницы со списком новостей
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_list.html')

    def test_news_detail_view(self):
        # Проверка доступности страницы с конкретной новостью
        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_detail.html')

    def test_profile_view(self):
        # Проверка доступности страницы профиля пользователя
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_unlogged_user(self):
        # Проверка доступности страницы профиля неавторизованному пользователю
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_after_exit(self):
        # Проверка перенаправления после выхода из системы
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
