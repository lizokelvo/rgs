from flask import Flask, render_template, jsonify, request, redirect, url_for # type: ignore
from flask_login import LoginManager, login_user, logout_user, login_required, current_user # type: ignore
import re
from config import Config # type: ignore
from database import db, User, Product, CartItem # type: ignore
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

#Инициализация базы данных
db.init_app(app)

#Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Валидация данных
def validate_username(username):
    """Валидация логина: только латинские буквы, цифры и знаки препинания"""
    pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]*$'
    return re.match(pattern, username) and len(username) >= 3 and len(username) <= 80

def validate_password(password):
    """Валидация пароля"""
    pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]*$'
    return re.match(pattern, password) and len(password) >= 6

def validate_email(email):
    """Валидация email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_price(price):
    """Валидация цены: должна быть положительной"""
    try:
        price_val = float(price)
        return price_val > 0
    except:
        return False

@app.context_processor
def inject_student_info():
    return {
        'student_name': app.config['STUDENT_NAME'],
        'student_group': app.config['STUDENT_GROUP']
    }


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()

        errors = []
        if not validate_username(username):
            errors.append('Логин должен содержать только латинские буквы, цифры и знаки препинания (3-80 символов)')
        
        if not validate_password(password):
            errors.append('Пароль должен содержать только латинские буквы, цифры и знаки препинания (минимум 6 символов)')
        
        if email and not validate_email(email):
            errors.append('Неверный формат email')
        
        if User.query.filter_by(username=username).first():
            errors.append('Пользователь с таким логином уже существует')
        
        if errors:
            return render_template('register.html', errors=errors)

        user = User(username=username, email=email if email else None)
        user.set_password(password)

        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    logout_user()
    
    #Удаляем пользователя и все связанные данные
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    
    return jsonify({'success': True, 'redirect': url_for('index')})

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'category': p.category,
        'image_url': p.image_url,
        'stock': p.stock
    } for p in products])

@app.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    #Проверяем, есть ли товар уже в корзине
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Товар добавлен в корзину',
        'cart_count': CartItem.query.filter_by(user_id=current_user.id).count()
    })

@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': item.id,
        'product_id': item.product_id,
        'product_name': item.product.name,
        'product_price': item.product.price,
        'quantity': item.quantity,
        'total': item.product.price * item.quantity
    } for item in cart_items])


@app.route('/api/cart/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    
    if quantity is None or quantity < 1:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    cart_item = CartItem.query.get(item_id)
    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({'error': 'Item not found'}), 404
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    
    if not cart_item or cart_item.user_id != current_user.id:
        return jsonify({'error': 'Item not found'}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    #Проверяем наличие товаров на складе
    for item in cart_items:
        if item.product.stock < item.quantity:
            return jsonify({
                'error': f'Недостаточно товара "{item.product.name}" на складе'
            }), 400
    
    #Уменьшаем количество товаров на складе
    for item in cart_items:
        item.product.stock -= item.quantity
    
    #Очищаем корзину
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Покупка оформлена успешно!',
        'redirect': url_for('index')
    })

@app.route('/api/cart/count', methods=['GET'])
def get_cart_count():
    if current_user.is_authenticated:
        count = CartItem.query.filter_by(user_id=current_user.id).count()
        return jsonify({'count': count})
    return jsonify({'count': 0})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)