#!/usr/bin/env python
import os
import sys
import subprocess

print("ПОЛНЫЙ СБРОС И ЗАПУСК ПРИЛОЖЕНИЯ")

# 1. Удаляем базу данных
db_file = 'furniture_store.db'
if os.path.exists(db_file):
    os.remove(db_file)
    print(f"✓ Удален файл базы: {db_file}")

# 2. Создаем папку для картинок
os.makedirs('static/images', exist_ok=True)

# 3. Создаем тестовые картинки
images = ['milan.jpg', 'Neapol.jpg', 'tokyo.jpg', 'ergo.jpg', '3door.jpg']
for img in images:
    with open(f'static/images/{img}', 'w') as f:
        f.write(f"Test image for {img}")
print("✓ Созданы тестовые картинки")

# 4. Инициализируем базу данных
print("\nИнициализация базы данных...")
try:
    from app import app, db
    from database import Product, User
    
    with app.app_context():
        db.create_all()
        print("✓ Таблицы созданы")
        
        # Проверяем, есть ли товары
        if Product.query.count() == 0:
            # Добавляем тестовые товары
            products = [
                Product(
                    name='Диван угловой "Милан"',
                    description='Угловой диван с ортопедическим основанием, ткань велюр',
                    price=45000.00,
                    category='Диваны',
                    image_url='milan.jpg',
                    stock=5
                ),
                Product(
                    name='Кровать двуспальная "Неаполь"',
                    description='Кровать из массива дуба с ортопедическим основанием',
                    price=38000.00,
                    category='Кровати',
                    image_url='Neapol.jpg',
                    stock=7
                ),
                Product(
                    name='Обеденный стол "Токио"',
                    description='Стол раздвижной, стеклянная столешница',
                    price=28000.00,
                    category='Столы',
                    image_url='tokyo.jpg',
                    stock=8
                ),
                Product(
                    name='Стул офисный "Эрго"',
                    description='Офисный стул с регулировкой высоты и подлокотниками',
                    price=8500.00,
                    category='Стулья',
                    image_url='ergo.jpg',
                    stock=20
                ),
                Product(
                    name='Шкаф-купе 3-дверный',
                    description='Шкаф-купе с зеркальными дверями, система "Командор"',
                    price=52000.00,
                    category='Шкафы',
                    image_url='3door.jpg',
                    stock=4
                )
            ]
            
            for p in products:
                db.session.add(p)
            
            # Добавляем тестового пользователя
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            admin.is_admin = True
            db.session.add(admin)
            
            user = User(username='user1', email='user1@example.com')
            user.set_password('password123')
            db.session.add(user)
            
            db.session.commit()
            print(f"✓ Добавлено {len(products)} товаров и 2 пользователя")
        
        print("✓ База данных готова")
        
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("ЗАПУСК ПРИЛОЖЕНИЯ")
print("Откройте в браузере: http://localhost:5000")
print("\nДанные для входа:")
print("  Админ: admin / admin123")
print("  Пользователь: user1 / password123")
print("\nДля остановки нажмите Ctrl+C")

# 5. Запускаем приложение
os.system('python app.py')