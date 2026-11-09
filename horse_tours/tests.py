from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone
from .models import Category, Tour, Booking, Comment


class HorseToursTestCase(TestCase):
    def setUp(self):
        """Создание тестовых данных перед запуском тестов."""
        self.user1 = User.objects.create_user(username='aidai', password='password123')
        self.user2 = User.objects.create_user(username='beka', password='password123')

        self.cat_horse = Category.objects.create(name='Конный')
        self.cat_walk = Category.objects.create(name='Пеший')

        self.tour = Tour.objects.create(
            title='Конный тур в Ала-Арчу',
            description='Поездка на лошадях по горам',
            price=2500.00
        )
        self.tour.categories.add(self.cat_horse, self.cat_walk)

    # 1. ТЕСТ СВЯЗИ МНОГИЕ КО МНОГИМ
    def test_many_to_many_categories(self):
        """У тура может быть несколько категорий ("конный", "пеший")."""
        self.assertEqual(self.tour.categories.count(), 2)
        self.assertIn(self.cat_horse, self.tour.categories.all())
        self.assertIn(self.cat_walk, self.tour.categories.all())

    # 2. ТЕСТ СВЯЗИ 1 К 1
    def test_one_to_one_booking_restriction(self):
        """1 человек может купить только 1 тур (OneToOne restriction)."""
        Booking.objects.create(
            user=self.user1,
            tour=self.tour,
            booking_date=timezone.now()
        )
        # Второе бронирование для user1 вызовет ошибку
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                user=self.user1,
                tour=self.tour,
                booking_date=timezone.now()
            )

    # 3. ТЕСТ СВЯЗИ 1 КО МНОГИМ
    def test_one_to_many_comments(self):
        """1 человек может оставить несколько комментариев."""
        Comment.objects.create(user=self.user1, tour=self.tour, text="Супер тур!")
        Comment.objects.create(user=self.user1, tour=self.tour, text="Очень красиво.")
        self.assertEqual(self.user1.comments.count(), 2)

    # 4. ТЕСТ ОТПРАВКИ ФОРМЫ БРОНИРОВАНИЯ (POST)
    def test_booking_post_submission(self):
        """Проверка отправки формы бронирования через POST."""
        self.client.login(username='beka', password='password123')
        post_data = {
            'tour': self.tour.id,
            'booking_date': '2026-11-15 10:00:00'
        }
        response = self.client.post(reverse('horse_tours:create_booking'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(user=self.user2).exists())

    # 5. ТЕСТ ОТПРАВКИ ФОРМЫ КОММЕНТАРИЯ (POST)
    def test_comment_post_submission(self):
        """Проверка отправки формы комментария через POST."""
        self.client.login(username='aidai', password='password123')
        post_data = {
            'tour': self.tour.id,
            'text': 'Отличный гид!'
        }
        response = self.client.post(reverse('horse_tours:add_comment'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(text='Отличный гид!').exists())
