from app import app, db
from database import User, Product, CartItem
from werkzeug.security import generate_password_hash # type: ignore
import sys

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    
    with app.app_context():
        try:
            # Пробуем подключиться к БД
            print(f"Подключение к БД: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Создаем все таблицы
            print("\nСоздание таблиц...")
            db.create_all()
            print("✓ Таблицы успешно созданы")
            
            # Проверяем, есть ли уже пользователи
            user_count = User.query.count()
            product_count = Product.query.count()
            
            print(f"\nТекущее состояние БД:")
            print(f"  Пользователей: {user_count}")
            print(f"  Товаров: {product_count}")
            
            # Создаем администратора, если его нет
            if not User.query.filter_by(username='admin').first():
                print("\nСоздание администратора...")
                admin = User(
                    username='admin',
                    email='admin@furniture-store.com',
                    is_admin=True
                )
                admin.set_password('admin_password123')
                db.session.add(admin)
                print("✓ Администратор создан")
            else:
                print("\n✓ Администратор уже существует")
            
            # Создаем тестового пользователя
            if not User.query.filter_by(username='user1').first():
                print("Создание тестового пользователя...")
                user1 = User(
                    username='user1',
                    email='user1@example.com'
                )
                user1.set_password('password123')
                db.session.add(user1)
                print("✓ Тестовый пользователь создан")
            else:
                print("✓ Тестовый пользователь уже существует")
            
            # Добавляем товары (мебель), если их нет
            if Product.query.count() == 0:
                print("\nДобавление товаров...")
                
                products = [
                    # Диваны (10 позиций)
                    Product(
                        name='Диван угловой "Милан"',
                        description='Угловой диван с ортопедическим основанием, ткань велюр. Размер: 220x160 см',
                        price=45000.00,
                        category='Диваны',
                        image_url='https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=Sofa+Milan',
                        stock=5
                    ),
                    Product(
                        name='Диван прямой "Барселона"',
                        description='Прямой диван с механизмом трансформации, натуральная кожа. Размер: 200x90 см',
                        price=62000.00,
                        category='Диваны',
                        image_url='https://via.placeholder.com/300x200/50E3C2/FFFFFF?text=Sofa+Barcelona',
                        stock=3
                    ),
                    Product(
                        name='Диван-кровать "Афины"',
                        description='Раскладной диван с ортопедическим матрасом. Размер в разложенном виде: 190x140 см',
                        price=38000.00,
                        category='Диваны',
                        image_url='https://via.placeholder.com/300x200/9013FE/FFFFFF?text=Sofa+Athens',
                        stock=8
                    ),
                    Product(
                        name='Диван модульный "Токио"',
                        description='Модульный диван, можно собрать любую конфигурацию. Каждый модуль 80x80 см',
                        price=75000.00,
                        category='Диваны',
                        image_url='https://via.placeholder.com/300x200/F5A623/FFFFFF?text=Sofa+Tokyo',
                        stock=2
                    ),
                    Product(
                        name='Диван компактный "Мини"',
                        description='Небольшой диван для малогабаритных квартир. Размер: 150x80 см',
                        price=28000.00,
                        category='Диваны',
                        image_url='https://via.placeholder.com/300x200/7ED321/FFFFFF?text=Sofa+Mini',
                        stock=12
                    ),
                    
                    # Кровати (10 позиций)
                    Product(
                        name='Кровать двуспальная "Неаполь"',
                        description='Кровать из массива дуба с ортопедическим основанием. Размер: 200x180 см',
                        price=38000.00,
                        category='Кровати',
                        image_url='https://via.placeholder.com/300x200/417505/FFFFFF?text=Bed+Naples',
                        stock=7
                    ),
                    Product(
                        name='Кровать односпальная "Олимп"',
                        description='Кровать с ящиками для белья, ДСП. Размер: 200x90 см',
                        price=22000.00,
                        category='Кровати',
                        image_url='https://via.placeholder.com/300x200/BD10E0/FFFFFF?text=Bed+Olimp',
                        stock=10
                    ),
                    Product(
                        name='Кровать двуспальная "Империал"',
                        description='Кровать с мягким изголовьем, тканевая обивка. Размер: 200x160 см',
                        price=52000.00,
                        category='Кровати',
                        image_url='https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=Bed+Imperial',
                        stock=4
                    ),
                    Product(
                        name='Кровать детская "Радуга"',
                        description='Детская кровать с бортиками, яркий дизайн. Размер: 160x70 см',
                        price=19000.00,
                        category='Кровати',
                        image_url='https://via.placeholder.com/300x200/F8E71C/000000?text=Bed+Rainbow',
                        stock=15
                    ),
                    Product(
                        name='Кровать чердак "Студент"',
                        description='Двухъярусная кровать с рабочим местом внизу. Размер: 200x90 см',
                        price=34000.00,
                        category='Кровати',
                        image_url='https://via.placeholder.com/300x200/8B572A/FFFFFF?text=Bed+Loft',
                        stock=6
                    ),
                    
                    # Столы (10 позиций)
                    Product(
                        name='Обеденный стол "Токио"',
                        description='Стол раздвижной, стеклянная столешница. Размер: 120x80 см (раскладывается до 180x80 см)',
                        price=28000.00,
                        category='Столы',
                        image_url='https://via.placeholder.com/300x200/50E3C2/FFFFFF?text=Table+Tokyo',
                        stock=8
                    ),
                    Product(
                        name='Компьютерный стол "Модерн"',
                        description='Угловой компьютерный стол с полками. Размер: 140x120 см',
                        price=15000.00,
                        category='Столы',
                        image_url='https://via.placeholder.com/300x200/9013FE/FFFFFF?text=Table+Modern',
                        stock=12
                    ),
                    Product(
                        name='Письменный стол "Классик"',
                        description='Деревянный письменный стол с ящиками. Размер: 120x60 см',
                        price=21000.00,
                        category='Столы',
                        image_url='https://via.placeholder.com/300x200/F5A623/FFFFFF?text=Table+Classic',
                        stock=9
                    ),
                    Product(
                        name='Кофейный столик "Минимализм"',
                        description='Небольшой столик для гостиной, металл и стекло. Размер: 60x60 см',
                        price=8500.00,
                        category='Столы',
                        image_url='https://via.placeholder.com/300x200/7ED321/FFFFFF?text=Table+Coffee',
                        stock=20
                    ),
                    Product(
                        name='Барный стол "Паб"',
                        description='Высокий стол для кухни-гостиной. Высота: 110 см, диаметр: 70 см',
                        price=12500.00,
                        category='Столы',
                        image_url='https://via.placeholder.com/300x200/417505/FFFFFF?text=Table+Bar',
                        stock=7
                    ),
                    
                    # Стулья (10 позиций)
                    Product(
                        name='Стул офисный "Эрго"',
                        description='Офисный стул с регулировкой высоты и подлокотниками',
                        price=8500.00,
                        category='Стулья',
                        image_url='https://via.placeholder.com/300x200/BD10E0/FFFFFF?text=Chair+Ergo',
                        stock=20
                    ),
                    Product(
                        name='Табурет кухонный "Базовый"',
                        description='Деревянный табурет, высота 45 см',
                        price=2500.00,
                        category='Стулья',
                        image_url='https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=Stool+Basic',
                        stock=25
                    ),
                    Product(
                        name='Стул обеденный "Винтаж"',
                        description='Деревянный стул с мягким сиденьем, винтажный дизайн',
                        price=6500.00,
                        category='Стулья',
                        image_url='https://via.placeholder.com/300x200/F8E71C/000000?text=Chair+Vintage',
                        stock=18
                    ),
                    Product(
                        name='Кресло компьютерное "Геймер"',
                        description='Игровое кресло с подсветкой и поддержкой поясницы',
                        price=22000.00,
                        category='Стулья',
                        image_url='https://via.placeholder.com/300x200/8B572A/FFFFFF?text=Chair+Gamer',
                        stock=5
                    ),
                    Product(
                        name='Стул складной "Пикник"',
                        description='Легкий складной стул для дачи и пикников',
                        price=1800.00,
                        category='Стулья',
                        image_url='https://via.placeholder.com/300x200/50E3C2/FFFFFF?text=Chair+Folding',
                        stock=30
                    ),
                    
                    # Шкафы (10 позиций)
                    Product(
                        name='Шкаф-купе 3-дверный',
                        description='Шкаф-купе с зеркальными дверями, система "Командор". Размер: 240x60x220 см',
                        price=52000.00,
                        category='Шкафы',
                        image_url='https://via.placeholder.com/300x200/9013FE/FFFFFF?text=Wardrobe+3door',
                        stock=4
                    ),
                    Product(
                        name='Книжный шкаф "Библио"',
                        description='Книжный шкаф на 6 полок, ДСП. Размер: 180x40x200 см',
                        price=18000.00,
                        category='Шкафы',
                        image_url='https://via.placeholder.com/300x200/F5A623/FFFFFF?text=Bookcase+Bibli',
                        stock=6
                    ),
                    Product(
                        name='Гардеробная система "Минима"',
                        description='Модульная система для гардеробной. Размеры модулей: 100x60x200 см',
                        price=45000.00,
                        category='Шкафы',
                        image_url='https://via.placeholder.com/300x200/7ED321/FFFFFF?text=Wardrobe+System',
                        stock=3
                    ),
                    Product(
                        name='Тумба прикроватная "Ночка"',
                        description='Небольшая тумба с ящиком для мелочей. Размер: 45x45x55 см',
                        price=7500.00,
                        category='Шкафы',
                        image_url='https://via.placeholder.com/300x200/417505/FFFFFF?text=Nightstand',
                        stock=15
                    ),
                    Product(
                        name='Комод 4-х ящичный "Практик"',
                        description='Комод для белья с 4 ящиками. Размер: 120x45x80 см',
                        price=16500.00,
                        category='Шкафы',
                        image_url='https://via.placeholder.com/300x200/BD10E0/FFFFFF?text=Dresser',
                        stock=8
                    ),
                    
                    # Комоды и тумбы (5 позиций)
                    Product(
                        name='Комод 6-ти ящичный "Стандарт"',
                        description='Большой комод для хранения вещей. Размер: 160x50x90 см',
                        price=24500.00,
                        category='Комоды',
                        image_url='https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=Chest+Standard',
                        stock=5
                    ),
                    Product(
                        name='Тумба под TV "Медиа"',
                        description='Тумба для телевизора с отделениями для техники. Размер: 180x45x50 см',
                        price=19500.00,
                        category='Комоды',
                        image_url='https://via.placeholder.com/300x200/F8E71C/000000?text=TV+Stand',
                        stock=7
                    ),
                    Product(
                        name='Прихожая "Холл"',
                        description='Набор для прихожей: вешалка, банкетка, зеркало. Размер: 200x40x200 см',
                        price=32000.00,
                        category='Прихожие',
                        image_url='https://via.placeholder.com/300x200/8B572A/FFFFFF?text=Hallway+Set',
                        stock=4
                    ),
                    Product(
                        name='Стеллаж "Офисный"',
                        description='Стеллаж для документов и книг. Размер: 180x30x200 см',
                        price=12500.00,
                        category='Стеллажи',
                        image_url='https://via.placeholder.com/300x200/50E3C2/FFFFFF?text=Shelving',
                        stock=10
                    ),
                    Product(
                        name='Пуфик "Куб"',
                        description='Мягкий пуфик, можно использовать как сиденье или подставку для ног. Размер: 50x50x50 см',
                        price=6500.00,
                        category='Пуфики',
                        image_url='https://via.placeholder.com/300x200/9013FE/FFFFFF?text=Ottoman',
                        stock=12
                    )
                ]
                
                db.session.add_all(products)
                print(f" Добавлено {len(products)} товаров")
            else:
                print("\n Товары уже существуют в базе")
            
            # Сохраняем все изменения
            db.session.commit()
            
            print("ИНИЦИАЛИЗАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
            
            print("\nДАННЫЕ ДЛЯ ВХОДА:")
            print("Администратор:")
            print("  Логин: admin")
            print("  Пароль: admin_password123")
            print("\nТестовый пользователь:")
            print("  Логин: user1")
            print("  Пароль: password123")
            print("\nОбщее количество товаров:", Product.query.count())
            
        except Exception as e:
            print(f"\n ОШИБКА: {e}")
            print("\nПРОВЕРЬТЕ:")
            print("1. Запущен ли сервер PostgreSQL")
            print("2. Правильность настроек в .env файле:")
            print(f"   DB_USER={app.config.get('DB_USER', 'не задан')}")
            print(f"   DB_PASSWORD={'***' if app.config.get('DB_PASSWORD') else 'не задан'}")
            print(f"   DB_HOST={app.config.get('DB_HOST', 'не задан')}")
            print(f"   DB_PORT={app.config.get('DB_PORT', 'не задан')}")
            print(f"   DB_NAME={app.config.get('DB_NAME', 'не задан')}")
            print("3. Существует ли база данных")
            print("4. Правильность пароля для подключения")
            
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    init_database()