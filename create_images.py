#!/usr/bin/env python
import os

# Создаем папку для картинок
os.makedirs('static/images', exist_ok=True)

# Диван
sofa_svg = '''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="200" fill="#f0f8ff"/>
<rect x="50" y="100" width="200" height="60" rx="5" fill="#8b4513"/>
<rect x="50" y="160" width="200" height="10" fill="#a0522d"/>
<rect x="40" y="90" width="220" height="10" rx="5" fill="#d2691e"/>
<circle cx="70" cy="170" r="8" fill="#333"/>
<circle cx="230" cy="170" r="8" fill="#333"/>
<text x="150" y="130" text-anchor="middle" font-family="Arial" font-size="14" fill="white">Диван</text>
</svg>'''

with open('static/images/milan.svg', 'w') as f:
    f.write(sofa_svg)

# Кровать
bed_svg = '''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="200" fill="#f0f8ff"/>
<rect x="60" y="80" width="180" height="80" rx="5" fill="#4169e1"/>
<rect x="60" y="160" width="180" height="20" fill="#1e90ff"/>
<rect x="80" y="70" width="140" height="10" fill="#f0e68c"/>
<circle cx="80" cy="180" r="8" fill="#333"/>
<circle cx="220" cy="180" r="8" fill="#333"/>
<text x="150" y="120" text-anchor="middle" font-family="Arial" font-size="14" fill="white">Кровать</text>
</svg>'''

with open('static/images/Neapol.svg', 'w') as f:
    f.write(bed_svg)

# Стол
table_svg = '''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="200" fill="#f0f8ff"/>
<rect x="80" y="120" width="140" height="8" fill="#8b4513"/>
<rect x="90" y="128" width="10" height="40" fill="#a0522d"/>
<rect x="200" y="128" width="10" height="40" fill="#a0522d"/>
<circle cx="95" cy="168" r="5" fill="#333"/>
<circle cx="205" cy="168" r="5" fill="#333"/>
<rect x="85" y="110" width="130" height="10" fill="#deb887"/>
<text x="150" y="105" text-anchor="middle" font-family="Arial" font-size="12" fill="#333">Стол</text>
</svg>'''

with open('static/images/tokyo.svg', 'w') as f:
    f.write(table_svg)

# Стул
chair_svg = '''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="200" fill="#f0f8ff"/>
<rect x="120" y="130" width="60" height="40" rx="3" fill="#4682b4"/>
<rect x="110" y="170" width="80" height="10" fill="#708090"/>
<rect x="125" y="125" width="50" height="5" fill="#f5deb3"/>
<rect x="135" y="110" width="30" height="15" fill="#daa520"/>
<rect x="140" y="95" width="20" height="15" fill="#daa520"/>
<circle cx="125" cy="180" r="8" fill="#333"/>
<circle cx="175" cy="180" r="8" fill="#333"/>
<text x="150" y="150" text-anchor="middle" font-family="Arial" font-size="12" fill="white">Стул</text>
</svg>'''

with open('static/images/ergo.svg', 'w') as f:
    f.write(chair_svg)

# Шкаф
wardrobe_svg = '''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
<rect width="300" height="200" fill="#f0f8ff"/>
<rect x="80" y="50" width="140" height="130" rx="5" fill="#d2b48c"/>
<rect x="90" y="60" width="40" height="110" fill="#a0522d"/>
<rect x="140" y="60" width="40" height="110" fill="#a0522d"/>
<rect x="190" y="60" width="20" height="110" fill="#a0522d"/>
<circle cx="110" cy="115" r="4" fill="#333"/>
<circle cx="160" cy="115" r="4" fill="#333"/>
<circle cx="200" cy="115" r="4" fill="#333"/>
<text x="150" y="40" text-anchor="middle" font-family="Arial" font-size="14" fill="#333">Шкаф</text>
</svg>'''

with open('static/images/3door.svg', 'w') as f:
    f.write(wardrobe_svg)

print("✓ Созданы SVG изображения в static/images/")
print("  - milan.svg (Диван)")
print("  - Neapol.svg (Кровать)")
print("  - tokyo.svg (Стол)")
print("  - ergo.svg (Стул)")
print("  - 3door.svg (Шкаф)")