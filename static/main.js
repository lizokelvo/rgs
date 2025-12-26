// main.js - Основные функции для онлайн-магазина мебели

document.addEventListener('DOMContentLoaded', function() {
    console.log('Мебельный магазин загружен');
    
    // Инициализация всех компонентов
    initCartSystem();
    initFormValidations();
    initProductInteractions();
    initUIEnhancements();
});

/**
 * Система корзины
 */
function initCartSystem() {
    // Обновление счетчика корзины
    updateCartCount();
    
    // Обновление каждые 30 секунд
    setInterval(updateCartCount, 30000);
}

/**
 * Обновление счетчика товаров в корзине
 */
async function updateCartCount() {
    try {
        const response = await fetch('/api/cart/count');
        if (!response.ok) throw new Error('Ошибка сети');
        
        const data = await response.json();
        const cartCountElements = document.querySelectorAll('#cart-count, .cart-count');
        
        cartCountElements.forEach(element => {
            element.textContent = data.count || 0;
        });
    } catch (error) {
        console.error('Ошибка при обновлении счетчика корзины:', error);
    }
}

/**
 * Добавление товара в корзину
 */
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });
        
        if (!response.ok) throw new Error('Ошибка сети');
        
        const data = await response.json();
        
        if (data.success) {
            // Обновляем счетчик
            await updateCartCount();
            
            // Показываем уведомление
            showNotification('Товар добавлен в корзину', 'success');
            return true;
        } else {
            showNotification(data.error || 'Ошибка при добавлении в корзину', 'error');
            return false;
        }
    } catch (error) {
        console.error('Ошибка при добавлении в корзину:', error);
        showNotification('Ошибка сети. Попробуйте позже.', 'error');
        return false;
    }
}

/**
 * Удаление товара из корзины
 */
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`/api/cart/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('Ошибка сети');
        
        const data = await response.json();
        
        if (data.success) {
            await updateCartCount();
            showNotification('Товар удален из корзины', 'success');
            return true;
        } else {
            showNotification(data.error || 'Ошибка при удалении', 'error');
            return false;
        }
    } catch (error) {
        console.error('Ошибка при удалении из корзины:', error);
        showNotification('Ошибка сети. Попробуйте позже.', 'error');
        return false;
    }
}

/**
 * Валидация форм
 */
function initFormValidations() {
    // Валидация логина
    const usernameInputs = document.querySelectorAll('input[name="username"]');
    usernameInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateUsername(this.value, this);
        });
    });
    
    // Валидация пароля
    const passwordInputs = document.querySelectorAll('input[name="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            validatePassword(this.value, this);
        });
    });
    
    // Валидация email
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateEmail(this.value, this);
        });
    });
}

/**
 * Валидация логина
 */
function validateUsername(username, inputElement) {
    const pattern = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]{3,80}$/;
    const isValid = pattern.test(username);
    
    if (inputElement) {
        updateValidationStatus(inputElement, isValid, 
            isValid ? 'Корректный логин' : 'Только латинские буквы, цифры и знаки препинания (3-80 символов)');
    }
    
    return isValid;
}

/**
 * Валидация пароля
 */
function validatePassword(password, inputElement) {
    const pattern = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]{6,100}$/;
    const isValid = pattern.test(password);
    
    if (inputElement) {
        updateValidationStatus(inputElement, isValid,
            isValid ? 'Корректный пароль' : 'Минимум 6 символов, только латинские буквы, цифры и знаки препинания');
    }
    
    return isValid;
}

/**
 * Валидация email
 */
function validateEmail(email, inputElement) {
    if (!email.trim()) return true; // Email не обязателен
    
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const isValid = pattern.test(email);
    
    if (inputElement) {
        updateValidationStatus(inputElement, isValid,
            isValid ? 'Корректный email' : 'Введите корректный email адрес');
    }
    
    return isValid;
}

/**
 * Обновление статуса валидации
 */
function updateValidationStatus(element, isValid, message) {
    element.classList.remove('is-valid', 'is-invalid');
    
    if (element.value.trim() === '') {
        return;
    }
    
    if (isValid) {
        element.classList.add('is-valid');
    } else {
        element.classList.add('is-invalid');
        
        // Показываем сообщение об ошибке
        let feedback = element.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            element.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }
}

/**
 * Взаимодействия с товарами
 */
function initProductInteractions() {
    // Кнопки "Добавить в корзину"
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', async function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName || 'Товар';
            
            // Показываем индикатор загрузки
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="bi bi-hourglass"></i> Добавляем...';
            this.disabled = true;
            
            // Добавляем в корзину
            const success = await addToCart(productId, 1);
            
            // Восстанавливаем кнопку
            if (!success) {
                this.innerHTML = originalText;
                this.disabled = false;
            }
        });
    });
    
    // Фильтрация по категориям
    document.querySelectorAll('.category-filter').forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            filterProductsByCategory(category);
            
            // Обновляем активную кнопку
            document.querySelectorAll('.category-filter').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
}

/**
 * Фильтрация товаров по категории
 */
function filterProductsByCategory(category) {
    const productItems = document.querySelectorAll('.product-item');
    
    productItems.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'block';
            item.classList.add('fade-in');
        } else {
            item.style.display = 'none';
        }
    });
}

/**
 * Улучшения интерфейса
 */
function initUIEnhancements() {
    // Переключение видимости паролей
    document.querySelectorAll('[id^="togglePassword"], [id^="toggleConfirmPassword"]').forEach(button => {
        button.addEventListener('click', function() {
            const inputId = this.id.replace('toggle', '').toLowerCase();
            const input = document.getElementById(inputId);
            
            if (input) {
                const type = input.type === 'password' ? 'text' : 'password';
                input.type = type;
                
                // Меняем иконку
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye');
                    icon.classList.toggle('bi-eye-slash');
                }
            }
        });
    });
    
    // Подтверждение опасных действий
    document.querySelectorAll('[data-confirm]').forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Вы уверены?';
            if (!confirm(message)) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
    
    // Ленивая загрузка изображений
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Плавная прокрутка к якорям
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Показать уведомление
 */
function showNotification(message, type = 'info') {
    // Создаем контейнер для уведомлений, если его нет
    let container = document.getElementById('notifications');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notifications';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(container);
    }
    
    // Создаем уведомление
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        animation: slideIn 0.3s ease-out;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    `;
    
    notification.innerHTML = `
        ${getIconForType(type)} ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

/**
 * Получить иконку для типа уведомления
 */
function getIconForType(type) {
    const icons = {
        success: '<i class="bi bi-check-circle"></i>',
        error: '<i class="bi bi-exclamation-circle"></i>',
        warning: '<i class="bi bi-exclamation-triangle"></i>',
        info: '<i class="bi bi-info-circle"></i>'
    };
    return icons[type] || icons.info;
}

/**
 * Форматирование цены
 */
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(price);
}

/**
 * Проверка авторизации
 */
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/check');
        return response.ok;
    } catch (error) {
        return false;
    }
}

/**
 * Загрузка данных пользователя
 */
async function loadUserData() {
    try {
        const response = await fetch('/api/user/profile');
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.error('Ошибка при загрузке данных пользователя:', error);
    }
    return null;
}

/**
 * Обработка ошибок AJAX запросов
 */
function handleAjaxError(error) {
    console.error('AJAX ошибка:', error);
    
    if (error.message === 'Failed to fetch') {
        showNotification('Ошибка соединения с сервером', 'error');
    } else if (error.status === 401) {
        showNotification('Требуется авторизация', 'warning');
        setTimeout(() => {
            window.location.href = '/login';
        }, 1500);
    } else if (error.status === 403) {
        showNotification('Доступ запрещен', 'error');
    } else if (error.status >= 500) {
        showNotification('Ошибка сервера. Попробуйте позже.', 'error');
    }
}

// Добавляем CSS для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    img[data-src] {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    img.loaded {
        opacity: 1;
    }
    
    .is-valid {
        border-color: #198754 !important;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 8'%3e%3cpath fill='%23198754' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right calc(0.375em + 0.1875rem) center;
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    }
    
    .is-invalid {
        border-color: #dc3545 !important;
        background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right calc(0.375em + 0.1875rem) center;
        background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
    }
`;
document.head.appendChild(style);

// Экспорт функций для использования в других скриптах
window.FurnitureStore = {
    addToCart,
    removeFromCart,
    updateCartCount,
    showNotification,
    formatPrice,
    validateUsername,
    validatePassword,
    validateEmail
};