from django.views.generic import DetailView, ListView
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object