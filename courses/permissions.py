from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверка, является ли пользователь модератором
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(permissions.BasePermission):
    """
    Проверка, является ли пользователь владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
