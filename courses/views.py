from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .paginators import CoursePagination, LessonPagination, SubscriptionPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    pagination_class = CoursePagination

    def get_permissions(self):
        """
        Настраиваем права доступа в зависимости от действия
        """
        if self.action == 'create':
            # Создавать курсы могут только авторизованные пользователи, не модераторы
            permission_classes = [permissions.IsAuthenticated & ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут модераторы или владельцы
            permission_classes = [permissions.IsAuthenticated & (IsModerator | IsOwner)]
        elif self.action == 'destroy':
            # Удалять могут только владельцы (не модераторы)
            permission_classes = [permissions.IsAuthenticated & IsOwner & ~IsModerator]
        else:
            # Просматривать могут все авторизованные пользователи
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Модераторы и администраторы видят все курсы, обычные пользователи - только свои
        """
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user.is_superuser or user.groups.filter(name='moderators').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Автоматически назначаем владельца при создании курса
        """
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        """Добавляем request в контекст сериализатора"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        """
        Подписаться или отписаться от курса.
        Если подписка существует - переключает её активность.
        Если не существует - создает активную подписку.
        """
        course = self.get_object()
        user = request.user

        # Получаем или создаем подписку
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course
        )

        if created:
            # Новая подписка - активируем
            subscription.is_active = True
            message = "Вы успешно подписались на курс"
        else:
            # Существующая подписка - переключаем статус
            subscription.is_active = not subscription.is_active
            message = "Вы отписались от курса" if not subscription.is_active else "Вы снова подписались на курс"

        subscription.save()

        return Response({
            'status': 'success',
            'message': message,
            'is_subscribed': subscription.is_active,
            'course_id': course.id,
            'course_title': course.title
        })


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    pagination_class = LessonPagination

    def get_permissions(self):
        """
        Настраиваем права доступа в зависимости от действия
        """
        if self.action == 'create':
            # Создавать уроки могут только авторизованные пользователи, не модераторы
            permission_classes = [permissions.IsAuthenticated & ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            # Обновлять могут модераторы или владельцы
            permission_classes = [permissions.IsAuthenticated & (IsModerator | IsOwner)]
        elif self.action == 'destroy':
            # Удалять могут только владельцы (не модераторы)
            permission_classes = [permissions.IsAuthenticated & IsOwner & ~IsModerator]
        else:
            # Просматривать могут все авторизованные пользователи
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Модераторы и администраторы видят все уроки, обычные пользователи - только свои
        """
        user = self.request.user

        if not user.is_authenticated:
            return Lesson.objects.none()

        if user.is_superuser or user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Автоматически назначаем владельца при создании урока
        """
        serializer.save(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet для управления подписками пользователя"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SubscriptionPagination

    def get_queryset(self):
        """Пользователь видит только свои подписки"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание подписки с текущим пользователем"""
        print("=" * 50)
        print("perform_create вызван")
        print(f"Данные запроса: {self.request.data}")
        print(f"Тип данных: {type(self.request.data)}")

        # Пробуем разные варианты получения course_id
        course_id = None

        # Вариант 1: Прямое значение
        if 'course' in self.request.data:
            course_id = self.request.data.get('course')
            print(f"Найдено поле 'course': {course_id}")

        # Вариант 2: Если course - это словарь (вложенный объект)
        elif 'course' in self.request.data and isinstance(self.request.data['course'], dict):
            course_id = self.request.data['course'].get('id')
            print(f"Найдено поле 'course' как словарь, ID: {course_id}")

        # Вариант 3: Поле course_id
        elif 'course_id' in self.request.data:
            course_id = self.request.data.get('course_id')
            print(f"Найдено поле 'course_id': {course_id}")

        print(f"Извлеченный course_id: {course_id}")

        if not course_id:
            print("ОШИБКА: course_id не найден в данных запроса")
            # Вызываем валидацию сериализатора, чтобы получить ошибку
            serializer.is_valid(raise_exception=True)
            return

        # Ищем курс
        try:
            course = Course.objects.get(id=course_id)
            print(f"Найден курс: {course.title} (ID: {course.id})")
        except Course.DoesNotExist:
            print(f"ОШИБКА: Курс с ID={course_id} не найден")
            raise

        # Проверяем, не существует ли уже подписка
        subscription, created = Subscription.objects.get_or_create(
            user=self.request.user,
            course=course,
            defaults={'is_active': True}
        )

        print(f"Подписка создана: {created}")

        if not created:
            # Если подписка уже существует, активируем её
            subscription.is_active = True
            subscription.save()
            print(f"Подписка обновлена, активна: {subscription.is_active}")

        print("=" * 50)

        return subscription
