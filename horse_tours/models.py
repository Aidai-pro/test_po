from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категории туров ("конный", "пеший", "на мото")."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Tour(models.Model):
    """Модель тура (Связь Многие ко Многим с Категориями)."""
    title = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    # 1. СВЯЗЬ МНОГИЕ КО МНОГИМ (ManyToManyField)
    categories = models.ManyToManyField(Category, related_name='tours', verbose_name="Категории")

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Бронирование (1 человек может купить только 1 тур на определенное время)."""
    # 2. СВЯЗЬ 1 К 1 (OneToOneField) — один пользователь имеет ровно одно бронирование
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='booking', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name="Тур")
    booking_date = models.DateTimeField(verbose_name="Дата и время тура")

    def __str__(self):
        return f"Бронь {self.user.username} на {self.tour.title}"


class Comment(models.Model):
    """Комментарии (1 человек может оставить несколько комментариев)."""
    # 3. СВЯЗЬ 1 КО МНОГИМ (ForeignKey) — один пользователь может оставить много комментариев
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='comments', verbose_name="Тур")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.tour.title}"