import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from courses.serializers import SubscriptionSerializer
from courses.models import Course, Subscription
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

User = get_user_model()

# Создаем тестовые данные
user = User.objects.create_user(email='test@example.com', password='pass')
course = Course.objects.create(title='Test Course', owner=user)

# Создаем запрос с пользователем
factory = APIRequestFactory()
request = factory.post('/')
request.user = user

# Тестируем сериализатор
print("Тест 1: Валидные данные (ID курса)")
data = {'course': course.id}
serializer = SubscriptionSerializer(data=data, context={'request': request})
print(f"Валидность: {serializer.is_valid()}")
print(f"Ошибки: {serializer.errors if not serializer.is_valid() else 'Нет'}")
print(f"Валидированные данные: {serializer.validated_data if serializer.is_valid() else 'Нет'}")

print("\nТест 2: Вложенный объект")
data = {'course': {'id': course.id}}
serializer = SubscriptionSerializer(data=data, context={'request': request})
print(f"Валидность: {serializer.is_valid()}")
print(f"Ошибки: {serializer.errors}")

print("\nТест 3: Поле course_id")
data = {'course_id': course.id}
serializer = SubscriptionSerializer(data=data, context={'request': request})
print(f"Валидность: {serializer.is_valid()}")
print(f"Ошибки: {serializer.errors}")
