from django.test import TestCase
from django.urls import reverse
from blog.models import Blog


class BlogTestCase(TestCase):

    def setUp(self):
        """Создание тестовых данных перед запуском каждого теста."""
        self.blog1 = Blog.objects.create(
            title="Тестовый блог 1",
            body="Описание первого блога",
            is_published=True
        )
        self.blog2 = Blog.objects.create(
            title="Тестовый блог 2",
            body="Описание второго блога",
            is_published=True
        )

    # -------------------------------------------------------------------
    # Задание 1: 5 вариантов проверки List и Detail views
    # -------------------------------------------------------------------

    def test_1_list_view_status_and_content(self):
        """1. Проверка получения данных списка (получаем контент или нет)."""
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый блог 1")

    def test_2_detail_view_id_and_content(self):
        """2. Проверка детальной страницы (получаем ли id и корректный контент)."""
        response = self.client.get(reverse('blog:view', kwargs={'pk': self.blog1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].pk, self.blog1.pk)
        self.assertContains(response, "Описание первого блога")

    def test_3_detail_view_not_found(self):
        """3. Проверка запроса несуществующего id (404 Not Found)."""
        response = self.client.get(reverse('blog:view', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_4_list_view_queryset_count(self):
        """4. Проверка количества опубликованных объектов в списке."""
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(len(response.context['object_list']), 2)

    def test_5_list_navigation_links(self):
        """5. Проверка перехода по ссылкам из списка на детальную страницу."""
        detail_url = reverse('blog:view', kwargs={'pk': self.blog1.pk})
        list_response = self.client.get(reverse('blog:list'))
        self.assertContains(list_response, detail_url)
        
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, 200)

    # -------------------------------------------------------------------
    # Задание 2: Проверка счетчика просмотров / лайков
    # -------------------------------------------------------------------

    def test_initial_views_count_is_zero(self):
        """Проверка: у нового блога количество просмотров/лайков изначально равно 0."""
        new_blog = Blog.objects.create(
            title="Новый блог",
            body="Контент"
        )
        self.assertEqual(new_blog.views_count, 0)

    def test_views_count_increment_on_detail_view(self):
        """Проверка: GET-запрос к детальной странице увеличивает число просмотров на 1."""
        self.assertEqual(self.blog1.views_count, 0)

        # Выполняем GET-запрос к детальной странице
        url = reverse('blog:view', kwargs={'pk': self.blog1.pk})
        self.client.get(url)

        # Обновляем объект из базы данных
        self.blog1.refresh_from_db()

        # Проверяем, что число просмотров стало равным 1
        self.assertEqual(self.blog1.views_count, 1)