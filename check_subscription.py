# -*- coding: utf-8 -*-
from django.urls import reverse

# Пробуем найти subscription URLs
print("Проверка subscription URLs:")

# Возможные имена
possible_names = [
    'subscriptions-list',
    'subscription-list',
    'courses:subscriptions-list',
    'courses:subscription-list',
]

for name in possible_names:
    try:
        url = reverse(name)
        print(f"✓ {name} -> {url}")
    except Exception as e:
        print(f"✗ {name} -> {e}")

# Также проверяем, есть ли вообще эндпоинт
print("\nПроверка прямого доступа к /api/courses/subscriptions/")
try:
    from django.test import RequestFactory
    from django.urls import resolve
    
    factory = RequestFactory()
    match = resolve('/api/courses/subscriptions/')
    print(f"✓ /api/courses/subscriptions/ -> {match.view_name}")
except Exception as e:
    print(f"✗ /api/courses/subscriptions/ -> {e}")
