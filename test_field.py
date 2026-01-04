# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from courses.models import Course
from courses.serializers import CourseSerializer

User = get_user_model()

# Создаем тестовые данные
user = User.objects.create_user(email='test@example.com', password='testpass')
course = Course.objects.create(title='Test Course', description='Test', owner=user)

# Создаем request с аутентифицированным пользователем
factory = APIRequestFactory()
request = factory.get('/')
request.user = user

# Создаем сериализатор с контекстом
serializer = CourseSerializer(course, context={'request': request})

print("Данные сериализатора:")
print(serializer.data)
print("\nЕсть ли поле is_subscribed?", 'is_subscribed' in serializer.data)
if 'is_subscribed' in serializer.data:
    print("Значение is_subscribed:", serializer.data['is_subscribed'])
