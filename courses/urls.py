# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')  # будет /api/courses/courses/
router.register(r'lessons', LessonViewSet, basename='lessons')  # будет /api/courses/lessons/

urlpatterns = [
    path('', include(router.urls)),
]
