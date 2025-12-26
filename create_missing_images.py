#!/usr/bin/env python
import os

os.makedirs('static/images', exist_ok=True)

# Список новых картинок для 25 товаров
new_images = [
    # Диваны
    ('sofa_compact.svg', 'Диван компактный', '#8B4513'),
    ('sofa_corner.svg', 'Диван прямой', '#A0522D'),
    ('sofa_bed.svg', 'Диван-кровать', '#D2691E'),
    ('sofa_modular.svg', 'Диван модульный', '#8B4513'),
    ('sofa_leather.svg', 'Диван кожаный', '#D2691E'),
    
    # Кровати
    ('bed_single.svg', 'Кровать односпальная', '#4169E1'),
    ('bed_double.svg', 'Кровать двуспальная', '#1E90FF'),
    ('bed_children.svg', 'Кровать детская', '#4682B4'),
    ('bed_loft.svg', 'Кровать чердак', '#4169E1'),
    ('bed_imperial.svg', 'Кровать империал', '#1E90FF'),
    
    # Столы
    ('table_computer.svg', 'Стол компьютерный', '#8B4513'),
    ('table_writing.svg', 'Стол письменный', '#A0522D'),
    ('table_coffee.svg', 'Стол кофейный', '#D2691E'),
    ('table_bar.svg', 'Стол барный', '#8B4513'),
    ('table_extendable.svg', 'Стол раздвижной', '#A0522D'),
    
    # Стулья
    ('stool_bar.svg', 'Табурет барный', '#4682B4'),
    ('chair_dining.svg', 'Стул обеденный', '#3CB371'),
    ('chair_gaming.svg', 'Кресло игровое', '#DC143C'),
    ('chair_folding.svg', 'Стул складной', '#4682B4'),
    ('chair_office.svg', 'Стул офисный', '#2E8B57'),
    
    # Шкафы
    ('wardrobe_2door.svg', 'Шкаф 2-дверный', '#D2B48C'),
    ('wardrobe_4door.svg', 'Шкаф 4-дверный', '#BC8F8F'),
    ('wardrobe_sliding.svg', 'Шкаф-купе', '#D2B48C'),
    ('closet.svg', 'Гардероб', '#BC8F8F'),
    ('wardrobe_builtin.svg', 'Шкаф встроенный', '#D2B48C')
]

for filename, title, color in new_images:
    svg_content = f'''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
    <rect width="300" height="200" fill="#f8f9fa"/>
    <rect x="50" y="50" width="200" height="100" rx="10" fill="{color}"/>
    <rect x="60" y="60" width="180" height="80" rx="5" fill="{color}" opacity="0.8"/>
    <text x="150" y="100" text-anchor="middle" font-family="Arial" font-size="16" fill="white" font-weight="bold">
        {title}
    </text>
    <circle cx="80" cy="170" r="8" fill="#6c757d"/>
    <circle cx="220" cy="170" r="8" fill="#6c757d"/>
    </svg>'''
    
    with open(f'static/images/{filename}', 'w') as f:
        f.write(svg_content)
    
    print(f"✓ Создан: {filename}")

print(f"\nСоздано {len(new_images)} новых изображений")
print("Всего изображений в папке static/images/:")
os.system('ls -la static/images/ | grep .svg')