from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


class Discipline(models.Model):
    title = models.CharField('Наименование', max_length=255)
    about = models.TextField('Описание', blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['title']
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class City(models.Model):
    name = models.CharField('Наименование', max_length=255)
    about = models.TextField('Описание', blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Teacher(models.Model):
    name = models.CharField('ФИО преподавателя', max_length=255)
    about = models.TextField('Описание', blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Room(models.Model):
    title = models.CharField('Кабинет', max_length=255)
    address = models.CharField('Описание', max_length=255)

    def __str__(self):
        return f"{self.title} - {self.address}"

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class RequestStatus(models.Model):
    type = models.CharField('Наименование статуса', max_length=255)

    def __str__(self):
        return f"{self.type}"

    class Meta:
        verbose_name = 'Статус заявки'
        verbose_name_plural = 'Статусы заявок'


class StudentType(models.Model):
    type = models.CharField('Наименование вида', max_length=255)

    def __str__(self):
        return f"{self.type}"

    class Meta:
        verbose_name = 'Вид студента'
        verbose_name_plural = 'Виды студентов'


class Student(AbstractUser):
    type = models.ForeignKey(StudentType, on_delete=models.CASCADE, null=True)
    name = models.CharField('ФИО', max_length=255)
    number = models.IntegerField('Тел. номер', null=True)
    email = models.EmailField('Эл. почта', max_length=255)

    def __str__(self):
        return f"{self.id}: {self.username} - {self.first_name} - {self.last_name} - {self.name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Group(models.Model):
    title = models.CharField('Наименование группы', max_length=255)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Группа студента'
        verbose_name_plural = 'Группы студентов'


class GroupMember(models.Model):
    title = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.student} "

    class Meta:
        verbose_name = 'Студент группы'
        verbose_name_plural = 'Студенты группы'


class Lesson(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_date = models.DateField('Дата начала',)
    end_date = models.DateField('Дата окончания',)
    start_time = models.TimeField('Время начала',)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    listeners = models.IntegerField(default=0)
    max_listeners = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.discipline} - {self.city} - {self.start_date}"

    def is_full(self):
        if self.listeners >= self.max_listeners or self.max_listeners <= 0:
            LessonListeners.objects.filter(lesson=self).delete()
            return True
        return False

    def increment_listeners(self):
        if not self.is_full():
            self.listeners += 1
            self.save()
            self.max_listeners -= 1
            self.save()


    class Meta:
        ordering = ['discipline', 'start_date']
        verbose_name = 'Занятие (Расписание)'
        verbose_name_plural = 'Занятия (Расписание)'



class Request(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField('Комментарии', blank=True)
    status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.student.last_name}- {self.student.first_name} - {self.status} "

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)
        if not created and self.status.pk == 2:
            LessonListeners.objects.get_or_create(lesson=self.lesson, student=self.student)

    class Meta:
        verbose_name = 'Запрос от студента'
        verbose_name_plural = 'Запросы от студентов'


class LessonListeners(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Проверяем, что объект еще не сохранен
            self.lesson.increment_listeners()  # Увеличиваем количество слушателей в занятии
            self.lesson.max_listeners -= 1  # Уменьшаем максимальное количество слушателей в занятии
            self.lesson.save()  # Сохраняем изменения в модели Lesson
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.lesson.listeners += 1
        if self.lesson.listeners < 0:
            self.lesson.listeners = 0
        self.lesson.max_listeners -= 1  # Уменьшаем максимальное количество слушателей в занятии
        if self.lesson.max_listeners < 0:
            self.lesson.max_listeners = 0
        self.lesson.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.lesson} - {self.student}"

    class Meta:
        verbose_name = 'Слушатель занятия'
        verbose_name_plural = 'Слушатели занятия'
