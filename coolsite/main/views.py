from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from .filters import LessonFilter
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import CharField
from django.shortcuts import render, get_object_or_404



menu = ["О Нас", "Войти"]


def index(request):
    types = StudentType.objects.all()
    return render(request, 'index.html', {'types': types, 'menu': menu, 'title': 'Главная'})


def about(request):
    return render(request, 'about.html', {'menu': menu, 'title': 'О Нас'})


def login_v(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('about')
            else:
                print(request, "Why is this not returned for invalid")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'menu': menu, 'title': 'Вход на сайт'})


def logout_view(request):
    logout(request)
    return redirect('about')


def lesson(request):
    error = 'No db'
    query = request.GET.get('discipline_search')

    if query:
        data = Lesson.objects.filter(Q(discipline__title__icontains=query) | Q(discipline__title__icontains=query.capitalize()))
    else:
        data = Lesson.objects.all()

    lesson_filter = LessonFilter(request.GET, queryset=data)
    context = {
        'lesson_filter': lesson_filter,
        'title': 'Список текущих занятий',
        'header': 'Занятия',
        'data': lesson_filter.qs,
        'error': error,
    }
    return render(request, 'lesson.html', context)






def mylesson(request):
    error = 'No db'
    current_user_lessons_id = LessonListeners.objects.filter(student=request.user, ).values_list('lesson_id')
    current_user_lessons = Lesson.objects.filter(id__in=current_user_lessons_id, start_date__gt=datetime.now())
    context = {
        'title': 'Список текущих занятии',
        'header': 'Занятия',
        'data': current_user_lessons,
        'error': error,
    }
    return render(request, 'mylessons.html', context)


def requests(request):
    error = 'No db'
    data = Request.objects.filter(student=request.user)
    context = {
        'title': 'Список заявок',
        'header': 'Мои заявки',
        'data': data,
        'error': error,
    }
    return render(request, 'requests.html', context)


def lessons(request):
    print(request.GET)


def archive(request):
    print(request.GET)


def about(request):
    return render(request, 'base.html', {'title': 'Высшая Школа Бизнеса AlmaU (ранее МАБ)'})


def coach(request):
    error = 'No db'
    data = Teacher.objects.all()
    context = {
        'title': 'Преподаватели',
        'header': 'Занятия',
        'data': data,
        'error': error,
    }
    return render(request, 'coach.html', context)


def disciplines(request):
    error = 'No db'
    data = Discipline.objects.all()
    context = {
        'title': 'Дисциплины',
        'header': 'Занятия',
        'data': data,
        'error': error,
    }
    return render(request, 'disciplines.html', context)


def select_view(request, id=0):
    if id == 0:
        lesson = Lesson.objects.first()
    else:
        try:
            lesson = Lesson.objects.get(pk=id)
        except Lesson.DoesNotExist:
            lesson = Lesson.objects.first()
    form = RequestForm(initial={'lesson': lesson})
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.student = request.user
            req.status = RequestStatus.objects.get(type="Отправлено")
            req.save()
            return redirect('requests')
    return render(request, 'addrequest.html', {'form': form})





