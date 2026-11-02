from django.test import TestCase
from django.urls import reverse
from articles.models import Article


class ArticleCRUDTestCase(TestCase):
    def setUp(self):
        """Создание тестовых данных перед выполнением каждого теста."""
        self.article = Article.objects.create(
            title="Тестовая статья",
            content="Содержимое тестовой статьи"
        )

    # 1. ТЕСТ READ 
    def test_article_list_view(self):
        """Проверка отображения списка статей."""
        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая статья")
        self.assertTemplateUsed(response, 'articles/article_list.html')

    def test_article_detail_view(self):
        """Проверка отображения детальной страницы статьи."""
        response = self.client.get(reverse('articles:detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Содержимое тестовой статьи")
        self.assertTemplateUsed(response, 'articles/article_detail.html')

    # 2. ТЕСТ CREATE 
    def test_article_create_view(self):
        """Проверка создания новой статьи через POST-запрос."""
        data = {
            'title': 'Новая созданная статья',
            'content': 'Текст новой статьи'
        }
        response = self.client.post(reverse('articles:create'), data)
        # Проверяем перенаправление на список статей после успешного создания
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title='Новая созданная статья').exists())

    # 3. ТЕСТ UPDATE 
    def test_article_update_view(self):
        """Проверка обновления существующей статьи."""
        data = {
            'title': 'Обновленный заголовок',
            'content': 'Обновленный текст статьи'
        }
        response = self.client.post(
            reverse('articles:update', kwargs={'pk': self.article.pk}), 
            data
        )
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Обновленный заголовок')

    # 4. ТЕСТ DELETE
    def test_article_delete_view(self):
        """Проверка удаления статьи."""
        response = self.client.post(reverse('articles:delete', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    # 5. ТЕСТ ГЕНЕРАЦИИ WORD-ОТЧЕТА
    def test_download_report_view(self):
        """Проверка успешной скачиваемости Word-отчета."""
        response = self.client.get(reverse('articles:export_report'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'], 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )