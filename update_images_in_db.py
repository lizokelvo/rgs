#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from database import Product

with app.app_context():
    products = Product.query.all()
    
    # Обновляем расширения файлов
    image_updates = {
        'milan.jpg': 'milan.svg',
        'Neapol.jpg': 'Neapol.svg',
        'tokyo.jpg': 'tokyo.svg',
        'ergo.jpg': 'ergo.svg',
        '3door.jpg': '3door.svg'
    }
    
    updated = 0
    for product in products:
        if product.image_url in image_updates:
            product.image_url = image_updates[product.image_url]
            updated += 1
    
    db.session.commit()
    print(f"✓ Обновлено {updated} товаров")
    print("✓ Теперь используются SVG изображения")