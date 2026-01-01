from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from users.models import Payment
from .models import Course, Lesson


User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичного просмотра профилей
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'city', 'avatar')
        read_only_fields = ('id', 'email', 'first_name', 'city', 'avatar')


class PrivateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра своего профиля
    """
    payment_history = PaymentSerializer(source='payments', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'phone', 'city', 'avatar', 'payment_history')
        read_only_fields = ('id', 'email', 'payment_history')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2',
                  'first_name', 'last_name', 'phone', 'city', 'avatar')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор пользователя с логикой выбора подходящего
    """

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'last_login', 'is_superuser',
                            'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def to_representation(self, instance):
        """
        Динамический выбор сериализатора в зависимости от контекста
        """
        request = self.context.get('request')

        if request and request.user == instance:
            # Для своего профиля используем приватный сериализатор
            return PrivateUserSerializer(instance, context=self.context).data
        else:
            # Для чужого профиля используем публичный сериализатор
            return PublicUserSerializer(instance, context=self.context).data