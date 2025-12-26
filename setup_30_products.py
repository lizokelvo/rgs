#!/usr/bin/env python
import os
import sys

print("НАСТРОЙКА СИСТЕМЫ С 30 ТОВАРАМИ")

# 1. Создаем недостающие картинки
print("\n1. Создание картинок для новых товаров...")
exec(open('create_missing_images.py').read())

# 2. Инициализируем базу с 30 товарами
print("\n2. Инициализация базы данных...")
exec(open('init_db.py').read())

print("ГОТОВО! Система настроена с 30 товарами.")

print("\nКатегории товаров:")
print("  • Диваны - 6 товаров")
print("  • Кровати - 6 товаров")
print("  • Столы - 6 товаров")
print("  • Стулья - 6 товаров")
print("  • Шкафы - 6 товаров")
print("\nДля запуска приложения выполните:")
print("python app.py")
print("\nОткройте: http://localhost:5000")