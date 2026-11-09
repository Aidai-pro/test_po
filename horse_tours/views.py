import docx
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse

from .models import Tour, Booking, Comment, Category
from .forms import BookingForm, CommentForm


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'horse_tours/tour_list.html', {'tours': tours})


@login_required
def create_booking(request):
    error_message = None
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.save()
                return redirect('horse_tours:tour_list')
            except IntegrityError:
                error_message = "У вас уже есть активное бронирование! Один пользователь может забронировать только один тур."
    else:
        form = BookingForm()
    return render(request, 'horse_tours/booking_form.html', {'form': form, 'error_message': error_message})


@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('horse_tours:tour_list')
    else:
        form = CommentForm()
    return render(request, 'horse_tours/comment_form.html', {'form': form})


def download_report(request):
    doc = docx.Document()
    
    # Заголовок
    doc.add_heading('Отчет по проекту HorseTours', level=0)
    
    # Сводка
    doc.add_heading('1. Общая статистика', level=1)
    doc.add_paragraph(f'Всего категорий: {Category.objects.count()}')
    doc.add_paragraph(f'Всего туров: {Tour.objects.count()}')
    doc.add_paragraph(f'Забронировано туров: {Booking.objects.count()}')
    doc.add_paragraph(f'Всего отзывов: {Comment.objects.count()}')
    
    # Связь M:M
    doc.add_heading('2. Туры и категории (Many-to-Many)', level=1)
    for tour in Tour.objects.all():
        cats = ", ".join([c.name for c in tour.categories.all()])
        doc.add_paragraph(f'• Тур: {tour.title} — {tour.price} сом | Категории: {cats or "Без категории"}')
        
    # Связь 1:1
    doc.add_heading('3. Бронирования (One-to-One)', level=1)
    for b in Booking.objects.all():
        doc.add_paragraph(f'• Пользователь {b.user.username} забронировал тур "{b.tour.title}" на {b.booking_date}')
        
    # Выгрузка в браузер
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="HorseTours_Report.docx"'
    doc.save(response)
    return response