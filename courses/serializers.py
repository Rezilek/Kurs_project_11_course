# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Payment
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_is_subscribed(self, obj):
        """Определяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj,
                is_active=True
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']
    
    def create(self, validated_data):
        """Автоматически устанавливаем текущего пользователя"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
