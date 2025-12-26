#!/usr/bin/env python
import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def create_database():
    print("Создание базы данных...")
    
    with app.app_context():
        try:
            # Удаляем старую базу, если она есть
            db_file = 'furniture_store.db'
            if os.path.exists(db_file):
                os.remove(db_file)
                print(f"Удален старый файл: {db_file}")
            
            # Создаем все таблицы
            db.create_all()
            print("✓ Таблицы созданы успешно!")
            
            # Проверяем, что таблицы созданы
            from sqlalchemy import inspect # type: ignore
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Созданные таблицы: {tables}")
            
            return True
            
        except Exception as e:
            print(f"✗ Ошибка при создании БД: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = create_database()
    if success:
        print("\nБаза данных успешно создана!")
        print("Запустите приложение: python app.py")
    else:
        print("\nНе удалось создать базу данных")