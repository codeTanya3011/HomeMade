import os
from django.core.management import call_command


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

import django
django.setup()

print("Починаю експорт даних...")

# Шляхи до файлів фікстур
categories_path = os.path.join(os.getcwd(), 'fixtures', 'goods', 'categories.json')
products_path = os.path.join(os.getcwd(), 'fixtures', 'goods', 'products.json')

# Створюємо fixtures/goods, якщо немає
os.makedirs(os.path.dirname(categories_path), exist_ok=True)

try:
    # Експорт goods.Categories/Products в файл
    with open(categories_path, 'w', encoding='utf-8') as file:
        call_command('dumpdata', 'goods.Categories', indent=4, stdout=file)
    print(f"Дані з goods.Categories успішно збережені в {categories_path}")
except Exception as e:
    print(f"Помилка при збереженні goods.Categories: {e}")

try:
    with open(products_path, 'w', encoding='utf-8') as file:
        call_command('dumpdata', 'goods.Products', indent=4, stdout=file)
    print(f"Дані з goods.Products успішно збережені в {products_path}")
except Exception as e:
    print(f"Помилка при збереженні goods.Products: {e}")


