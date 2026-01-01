from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

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


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

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