from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from .models import Category, Tour, Booking, Comment


class AuthCaptchaAndProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testrider', password='StrongPassword123!')

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post(reverse('horse_tours:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecretPassword123!',
            'password_confirm': 'SecretPassword123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_fails_with_wrong_captcha(self):
        """Тест авторизации: вход блокируется при неверной капче"""
        # Сначала открываем страницу входа, чтобы в сессии сгенерировалась капча
        self.client.get(reverse('horse_tours:login'))

        response = self.client.post(reverse('horse_tours:login'), {
            'username': 'testrider',
            'password': 'StrongPassword123!',
            'captcha': '99999',  # Заведомо неверный ответ
        })
        # Ожидаем код 200 (остались на странице входа с ошибкой), пользователь не авторизован
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_succeeds_with_valid_captcha(self):
        """Тест авторизации: успешный вход при правильном вводе капчи"""
        self.client.get(reverse('horse_tours:login'))
        correct_answer = self.client.session['captcha_answer']

        response = self.client.post(reverse('horse_tours:login'), {
            'username': 'testrider',
            'password': 'StrongPassword123!',
            'captcha': correct_answer,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('horse_tours:profile'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profile_access_control_and_content(self):
        """Тест личного кабинета: закрыт для гостей и открыт для авторизованных"""
        # 1. Анонимный пользователь перенаправляется на вход
        anon_resp = self.client.get(reverse('horse_tours:profile'))
        self.assertEqual(anon_resp.status_code, 302)

        # 2. Авторизованный пользователь видит свой кабинет
        self.client.login(username='testrider', password='StrongPassword123!')
        auth_resp = self.client.get(reverse('horse_tours:profile'))
        self.assertEqual(auth_resp.status_code, 200)
        self.assertContains(auth_resp, 'testrider')


class HorseToursModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tourist', password='Password123!')
        self.cat_horse = Category.objects.create(name='Конный')
        self.cat_foot = Category.objects.create(name='Пеший')
        self.tour = Tour.objects.create(title='Горный маршрут', description='Поход в горы', price=5000)
        self.tour.categories.add(self.cat_horse, self.cat_foot)

    def test_many_to_many_categories(self):
        """Тест M:M категорий у тура"""
        self.assertEqual(self.tour.categories.count(), 2)

    def test_one_to_one_booking_restriction(self):
        """Тест 1:1 ограничения на бронирование"""
        Booking.objects.create(user=self.user, tour=self.tour, booking_date=timezone.now())
        with self.assertRaises(IntegrityError):
            Booking.objects.create(user=self.user, tour=self.tour, booking_date=timezone.now())

    def test_one_to_many_comments(self):
        """Тест 1:M нескольких комментариев от одного пользователя"""
        Comment.objects.create(user=self.user, tour=self.tour, text='Супер!')
        Comment.objects.create(user=self.user, tour=self.tour, text='Обязательно вернусь!')
        self.assertEqual(Comment.objects.filter(user=self.user).count(), 2)