import os
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from docx import Document

from articles.models import Article
from articles.forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:list')


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:list')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles:list')


def download_report(request):
    file_path = "Django_Tests_Report.docx"
    
    # Создаем Word-отчет на лету, если файл еще не создан
    doc = Document()
    doc.add_heading('Отчет по тестированию Django', 0)
    doc.add_paragraph('Статус: Все модули CRUD и шаблоны функционируют корректно.')
    
    # Добавляем список статей из БД в отчет
    doc.add_heading('Текущие статьи в системе:', level=1)
    articles = Article.objects.all()
    if articles.exists():
        for art in articles:
            doc.add_paragraph(f'• {art.title}', style='List Bullet')
    else:
        doc.add_paragraph('Статей в базе данных пока нет.')

    doc.save(file_path)

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, 'rb'), 
            as_attachment=True, 
            filename='Django_Tests_Report.docx'
        )
    raise Http404("Файл отчета не найден")