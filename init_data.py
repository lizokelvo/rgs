#!/usr/bin/env python
from app import app, db
from database import Product

with app.app_context():
    # Создаем таблицы
    db.create_all()
    
    # Проверяем, есть ли товары
    if Product.query.count() == 0:
        print("Добавляем тестовые товары...")
        
        test_products = [
            Product(
                name="Диван угловой",
                description="Комфортный угловой диван",
                price=45000.00,
                category="Диваны",
                stock=5
            ),
            Product(
                name="Кровать двуспальная",
                description="Ортопедическая кровать",
                price=38000.00,
                category="Кровати",
                stock=3
            ),
            Product(
                name="Стол обеденный",
                description="Деревянный обеденный стол",
                price=25000.00,
                category="Столы",
                stock=8
            )
        ]
        
        for product in test_products:
            db.session.add(product)
        
        db.session.commit()
        print(f"Добавлено {len(test_products)} тестовых товаров")
    else:
        print(f"В базе уже есть {Product.query.count()} товаров")