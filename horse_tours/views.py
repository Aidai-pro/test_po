import random
import io
import unittest
import docx
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse

from .models import Tour, Booking, Comment, Category
from .forms import BookingForm, CommentForm, RegisterForm, LoginWithCaptchaForm


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'horse_tours/tour_list.html', {'tours': tours})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('horse_tours:profile')
    else:
        form = RegisterForm()
    return render(request, 'horse_tours/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginWithCaptchaForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('horse_tours:profile')
    else:
        form = LoginWithCaptchaForm(request=request)

    # Генерируем новую математическую капчу для отображения на странице
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    request.session['captcha_question'] = f"{a} + {b} = ?"
    request.session['captcha_answer'] = str(a + b)

    return render(request, 'horse_tours/login.html', {
        'form': form,
        'captcha_question': request.session['captcha_question']
    })


def logout_view(request):
    logout(request)
    return redirect('horse_tours:tour_list')


@login_required
def profile_view(request):
    booking = Booking.objects.filter(user=request.user).first()
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'horse_tours/profile.html', {
        'booking': booking,
        'comments': comments,
    })


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
                return redirect('horse_tours:profile')
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
            return redirect('horse_tours:profile')
    else:
        form = CommentForm()
    return render(request, 'horse_tours/comment_form.html', {'form': form})


def download_report(request):
    # Программно запускаем автотесты приложения horse_tours для фиксации реальных результатов
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName('horse_tours.tests')
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    test_log = stream.getvalue()

    doc = docx.Document()
    doc.add_heading('Отчет по тестированию и работе проекта HorseTours', level=0)

    # Раздел 1: Результаты автоматического тестирования
    doc.add_heading('1. Результаты автоматического тестирования (Auth, Captcha, Profile, DB)', level=1)
    status_text = "УСПЕШНО (OK)" if result.wasSuccessful() else "ЕСТЬ ОШИБКИ (FAILED)"
    doc.add_paragraph(f'Итоговый статус: {status_text}')
    doc.add_paragraph(f'Всего выполнено тестов: {result.testsRun}')
    doc.add_paragraph(f'Ошибок (Errors): {len(result.errors)} | Провалов (Failures): {len(result.failures)}')

    doc.add_heading('Подробный протокол выполнения тестов:', level=2)
    p_log = doc.add_paragraph(test_log)
    p_log.style.font.name = 'Consolas'

    # Раздел 2: Сводная статистика БД
    doc.add_heading('2. Сводная статистика базы данных', level=1)
    doc.add_paragraph(f'Всего категорий: {Category.objects.count()}')
    doc.add_paragraph(f'Всего туров: {Tour.objects.count()}')
    doc.add_paragraph(f'Забронировано туров: {Booking.objects.count()}')
    doc.add_paragraph(f'Всего отзывов: {Comment.objects.count()}')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="HorseTours_Test_Report.docx"'
    doc.save(response)
    return response