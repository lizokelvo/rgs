#!/usr/bin/env python
import os
import sys

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from database import Product

def main():
    print("=" * 50)
    print("ИСПРАВЛЕНИЕ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 1. Создаем таблицы
            print("1. Создаем таблицы...")
            db.create_all()
            print("   ✓ Таблицы созданы")
            
            # 2. Добавляем тестовые товары
            print("2. Добавляем тестовые товары...")
            if Product.query.count() == 0:
                products = [
                    Product(
                        name="Диван угловой",
                        description="Комфортный угловой диван",
                        price=45000,
                        category="Диваны",
                        stock=5
                    ),
                    Product(
                        name="Кровать двуспальная",
                        description="Ортопедическая кровать",
                        price=38000,
                        category="Кровати",
                        stock=3
                    ),
                    Product(
                        name="Стол обеденный",
                        description="Деревянный обеденный стол",
                        price=25000,
                        category="Столы",
                        stock=8
                    )
                ]
                db.session.add_all(products)
                db.session.commit()
                print(f"   ✓ Добавлено {len(products)} товаров")
            else:
                print(f"   ✓ Товары уже есть: {Product.query.count()} шт.")
            
            # 3. Проверяем
            print("3. Проверяем...")
            print(f"   ✓ Всего товаров: {Product.query.count()}")
            
            print("\n" + "=" * 50)
            print("ГОТОВО! База данных исправлена.")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n✗ Ошибка: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()