from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создаем группу модераторов
        self.moderator_group, _ = Group.objects.get_or_create(name='moderators')

        # Создаем пользователя и делаем его модератором
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.user.groups.add(self.moderator_group)

        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )

        # Создаем курс от имени пользователя (теперь он модератор, видит все)
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user  # Пользователь владелец и модератор
        )

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_subscription_via_subscribe_action(self):
        """Тест: создание подписки через action subscribe"""
        # Используем курс из setUp
        url = f'/api/courses/courses/{self.course.id}/subscribe/'
        print(f"Используем курс ID: {self.course.id}")

        response = self.client.post(url)
        print(f"URL: {url}")
        print(f"Статус: {response.status_code}")
        print(f"Данные: {response.data}")

        # Должен быть 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем данные
        self.assertEqual(response.data.get('status'), 'success')
        self.assertTrue(response.data.get('is_subscribed', False))

        # Проверяем в базе
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course,
            is_active=True
        ).exists())

    def test_create_subscription_via_subscriptions_endpoint(self):
        """Тест: создание подписки через endpoint /subscriptions/"""
        url = '/api/courses/subscriptions/'

        # Вариант 1: Просто ID курса
        data = {'course': self.course.id}

        print(f"URL: {url}")
        print(f"Данные POST: {data}")
        print(f"Тип course.id: {type(self.course.id)}")

        response = self.client.post(url, data, format='json')
        print(f"Статус: {response.status_code}")
        print(f"Данные ответа: {response.data}")

        # Отладка: если ошибка валидации
        if response.status_code == 400:
            print(f"Ошибка валидации: {response.data}")

        # Должен быть 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем в базе
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())


class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='testpass123'
        )

        # Создаем группу модераторов
        self.moderator_group, _ = Group.objects.get_or_create(name='moderators')
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='testpass123'
        )
        self.moderator.groups.add(self.moderator_group)

        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )

        # Создаем курс
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание курса',
            owner=self.owner
        )

        # Создаем урок с правильным полем video_url
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание урока',
            video_url='https://youtube.com/test',
            course=self.course,
            owner=self.owner
        )

    def test_lesson_update_by_moderator(self):
        """Тест: обновление урока модератором"""
        self.client.force_authenticate(user=self.moderator)

        url = f'/api/courses/lessons/{self.lesson.id}/'
        updated_data = {
            'title': 'Обновленный урок',
            'description': 'Обновленное описание',
            'video_url': 'https://youtube.com/new_video'
        }

        response = self.client.patch(url, updated_data)

        # Модератор должен иметь доступ
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Обновленный урок')
        self.assertEqual(self.lesson.video_url, 'https://youtube.com/new_video')

    def test_lesson_delete_by_other_user_denied(self):
        """Тест: запрет удаления урока другим пользователем"""
        self.client.force_authenticate(user=self.other_user)

        url = f'/api/courses/lessons/{self.lesson.id}/'
        response = self.client.delete(url)

        # Обычный пользователь не видит чужой урок - 404
        # Или если видит (через модераторские права), но не может удалить - 403
        # В вашем случае get_queryset скрывает чужие уроки, поэтому 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Урок должен остаться
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_by_owner_allowed(self):
        """Тест: удаление урока владельцем разрешено"""
        self.client.force_authenticate(user=self.owner)

        url = f'/api/courses/lessons/{self.lesson.id}/'
        response = self.client.delete(url)

        # Владелец может удалить свой урок
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())