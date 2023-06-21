import django_filters
from .models import Lesson, Discipline, City, Teacher
from django import forms
from django_filters import DateFromToRangeFilter
from django.db.models import Q


class LessonFilter(django_filters.FilterSet):
    discipline_search = django_filters.CharFilter(
        field_name='discipline__title',
        lookup_expr='icontains',
        label='Поиск дисциплины',
        method='filter_discipline_search',
        widget=forms.TextInput(attrs={"class": "form-control form-control-inline",
                                      "style": "display: inline-block; width: 250px; margin-right: 10px;"})
    )
    date_range = DateFromToRangeFilter(
        field_name='start_date',
        label='Дата проведения',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control form-control-inline',
                                                         'style': 'display: inline-block;'
                                                                  'width: 125px; margin-right: 10px;'})
    )
    discipline = django_filters.ModelChoiceFilter(
        queryset=Discipline.objects.all(),
        label="Дисциплина",
        widget=forms.Select(attrs={"class": "form-control form-control-inline",
                                   "style": "display: inline-block; width: 255px; margin-right: 10px;"})
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        label="Город",
        widget=forms.Select(attrs={"class": "form-control form-control-inline",
                                   "style": "display: inline-block; width: 125px; margin-right: 10px;"})
    )
    teacher = django_filters.ModelChoiceFilter(
        queryset=Teacher.objects.all(),
        label="Преподаватель",
        widget=forms.Select(attrs={"class": "form-control form-control-inline",
                                   "style": "display: inline-block; width: 255px; margin-right: 10px;"})
    )




    def filter_discipline_search(self, queryset, name, value):
        value = value.lower()  # Преобразование значения поиска в нижний регистр
        return queryset.filter(
            Q(discipline__title__icontains=value) |
            Q(discipline__title__icontains=value.capitalize()) |
            Q(discipline__title__icontains=value.upper())
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Приведение вывода к нижнему регистру
        self.filters['discipline_search'].field.widget.attrs['autocomplete'] = 'off'
    
    

    class Meta:
        model = Lesson
        fields = ['discipline', 'teacher', 'city', 'date_range']
