from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые данные для разработки'

    def handle(self, *args, **kwargs):
        # Создаем пользователя
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'phone': '+79991234567',
                'city': 'Москва'
            }
        )
        if created:
            user.set_password('TestPass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Создан тестовый пользователь'))

        # Создаем курсы
        course1, _ = Course.objects.get_or_create(
            title='Python для начинающих',
            defaults={
                'description': 'Базовый курс по Python',
                'owner': user
            }
        )

        course2, _ = Course.objects.get_or_create(
            title='Django REST Framework',
            defaults={
                'description': 'Продвинутый курс по Django DRF',
                'owner': user
            }
        )

        # Создаем уроки
        lesson1, _ = Lesson.objects.get_or_create(
            title='Введение в Python',
            defaults={
                'description': 'Основы языка Python',
                'video_url': 'https://example.com/video1',
                'course': course1,
                'owner': user
            }
        )

        lesson2, _ = Lesson.objects.get_or_create(
            title='Установка Django',
            defaults={
                'description': 'Как установить и настроить Django',
                'video_url': 'https://example.com/video2',
                'course': course2,
                'owner': user
            }
        )

        # Создаем платежи
        Payment.objects.get_or_create(
            user=user,
            paid_course=course1,
            amount=5000.00,
            payment_method='transfer'
        )

        Payment.objects.get_or_create(
            user=user,
            paid_lesson=lesson1,
            amount=1000.00,
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы'))