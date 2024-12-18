import os
from django.core.management import call_command

# Устанавливаем настройки Django для корректной работы скрипта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

import django
django.setup()

print("Начинаю экспорт данных...")

# Пути к файлам фикстур
categories_path = os.path.join(os.getcwd(), 'fixtures', 'goods', 'categories.json')
products_path = os.path.join(os.getcwd(), 'fixtures', 'goods', 'products.json')

# Создаем папку fixtures/goods, если она отсутствует
os.makedirs(os.path.dirname(categories_path), exist_ok=True)

try:
    # Экспорт данных модели goods.Categories в файл
    with open(categories_path, 'w', encoding='utf-8') as file:
        call_command('dumpdata', 'goods.Categories', indent=4, stdout=file)
    print(f"Данные из goods.Categories успешно сохранены в {categories_path}")
except Exception as e:
    print(f"Ошибка при сохранении goods.Categories: {e}")

try:
    # Экспорт данных модели goods.Products в файл
    with open(products_path, 'w', encoding='utf-8') as file:
        call_command('dumpdata', 'goods.Products', indent=4, stdout=file)
    print(f"Данные из goods.Products успешно сохранены в {products_path}")
except Exception as e:
    print(f"Ошибка при сохранении goods.Products: {e}")


