from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создает группы пользователей с правами'

    def handle(self, *args, **kwargs):
        # Создание группы модераторов
        moderator_group, created = Group.objects.get_or_create(name='moderators')

        if created:
            # Получаем разрешения для курсов и уроков
            course_content_type = ContentType.objects.get_for_model(Course)
            lesson_content_type = ContentType.objects.get_for_model(Lesson)

            # Разрешения для курсов (только просмотр и изменение)
            course_permissions = Permission.objects.filter(
                content_type=course_content_type,
                codename__in=['view_course', 'change_course']
            )

            # Разрешения для уроков (только просмотр и изменение)
            lesson_permissions = Permission.objects.filter(
                content_type=lesson_content_type,
                codename__in=['view_lesson', 'change_lesson']
            )

            # Добавляем разрешения группе
            for perm in course_permissions:
                moderator_group.permissions.add(perm)

            for perm in lesson_permissions:
                moderator_group.permissions.add(perm)

            self.stdout.write(
                self.style.SUCCESS('Группа модераторов успешно создана с правами:')
            )
            self.stdout.write('- Просмотр курсов')
            self.stdout.write('- Изменение курсов')
            self.stdout.write('- Просмотр уроков')
            self.stdout.write('- Изменение уроков')
        else:
            self.stdout.write(
                self.style.WARNING('Группа модераторов уже существует')
            )