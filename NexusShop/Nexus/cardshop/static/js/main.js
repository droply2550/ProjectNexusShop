/* ============================================
   VANGUARD NEXUS - Main JavaScript
   D Format Card Shop
   ============================================ */

// ========================
// UTILITY FUNCTIONS
// ========================

// Get CSRF Token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast Notification System
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = {
        'success': '✓',
        'error': '✕',
        'info': 'ℹ',
        'warning': '⚠'
    }[type] || '✓';
    
    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-msg">${message}</span>
        <div class="toast-bar"></div>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastOut 0.3s ease-out forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// ========================
// SHOPPING CART
// ========================

function addToCart(cardId) {
    fetch(`/cart/add/${cardId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('เพิ่มลงตะกร้าเรียบร้อยแล้ว! 🛒', 'success');
            updateCartCount(data.total_items);
        } else {
            showToast('ไม่สามารถเพิ่มเข้าตะกร้าได้', 'error');
        }
    })
    .catch(error => {
        showToast('เกิดข้อผิดพลาด', 'error');
        console.error('Error:', error);
    });
}

function updateCartCount(count) {
    const cartCounts = document.querySelectorAll('.cart-count');
    cartCounts.forEach(element => {
        element.textContent = count;
        element.style.display = count > 0 ? 'flex' : 'none';
    });
}

function removeFromCart(cardId) {
    if(!confirm('คุณต้องการลบสินค้านี้ออกจากตะกร้าหรือไม่?')) {
        return;
    }
    
    fetch(`/cart/remove/${cardId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('ลบสินค้าออกจากตะกร้าแล้ว ✓', 'success');
            updateCartCount(data.total_items);
            
            // Remove the item row from cart display
            const itemElement = document.querySelector(`[data-cart-item="${cardId}"]`);
            if (itemElement) {
                itemElement.style.animation = 'fadeOut 0.3s ease-out forwards';
                setTimeout(() => itemElement.remove(), 300);
            }
            
            // Update totals
            updateCartTotals(data.total);
            
            // If cart is empty, reload page
            if (data.total_items === 0) {
                setTimeout(() => location.reload(), 500);
            }
        } else {
            showToast('ไม่สามารถลบสินค้าได้', 'error');
        }
    })
    .catch(error => {
        showToast('เกิดข้อผิดพลาด', 'error');
        console.error('Error:', error);
    });
}

function updateCartQuantity(cardId, action) {
    const qtyInput = document.querySelector(`[data-qty-input="${cardId}"]`);
    let newQty = parseInt(qtyInput.value) || 1;
    
    if (action === 'increase') {
        newQty += 1;
    } else if (action === 'decrease') {
        newQty = Math.max(0, newQty - 1);
    }
    
    fetch(`/cart/update/${cardId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `qty=${newQty}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (newQty === 0) {
                // Item removed, show message and reload
                showToast('ลบสินค้าออกจากตะกร้าแล้ว', 'success');
                const itemElement = document.querySelector(`[data-cart-item="${cardId}"]`);
                if (itemElement) {
                    itemElement.style.animation = 'fadeOut 0.3s ease-out forwards';
                    setTimeout(() => itemElement.remove(), 300);
                }
                if (data.total_items === 0) {
                    setTimeout(() => location.reload(), 500);
                }
            } else {
                // Update quantity input
                qtyInput.value = newQty;
                
                // Update subtotal
                const price = parseFloat(document.querySelector(`[data-price="${cardId}"]`).textContent);
                const subtotal = (price * newQty).toFixed(2);
                const subtotalElement = document.querySelector(`[data-subtotal="${cardId}"]`);
                if (subtotalElement) {
                    subtotalElement.textContent = subtotal + ' ฿';
                }
                
                showToast('อัปเดตจำนวนเรียบร้อย', 'success');
            }
            
            updateCartCount(data.total_items);
            updateCartTotals(data.total);
        } else {
            showToast('ไม่สามารถอัปเดตจำนวนได้', 'error');
        }
    })
    .catch(error => {
        showToast('เกิดข้อผิดพลาด', 'error');
        console.error('Error:', error);
    });
}

function updateCartTotals(newTotal) {
    const subtotalElement = document.getElementById('summary-subtotal');
    const totalElement = document.getElementById('summary-total');
    
    if (subtotalElement) {
        subtotalElement.textContent = newTotal.toFixed(2) + ' ฿';
    }
    if (totalElement) {
        totalElement.textContent = newTotal.toFixed(2) + ' ฿';
    }
}


const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

function initializeAnimations() {
    document.querySelectorAll('.animate-up').forEach(el => {
        observer.observe(el);
    });
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// ========================
// EVENT LISTENERS
// ========================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize animations
    initializeAnimations();
    
    // Add to cart button handlers
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const cardId = button.getAttribute('data-id');
            if (cardId) {
                addToCart(cardId);
            }
        });
    });
    
    // Add to cart via button press (if form exists)
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            showToast('โปรดรอ...กำลังประมวลผล', 'info');
        });
    }
    
    // Form submission handlers
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'กำลังโหลด...';
            }
        });
    });
});

// ========================
// KEYBOARD SHORTCUTS
// ========================

document.addEventListener('keydown', (e) => {
    // Press '/' to focus search
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        const searchInput = document.querySelector('input[type="search"]') || 
                           document.querySelector('input[placeholder*="ค้นหา"]');
        if (searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    }
});

// ========================
// UTILITY SCRIPTS
// ========================

// Auto-hide alert messages after 5 seconds
window.addEventListener('load', () => {
    const alerts = document.querySelectorAll('[role="alert"]');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});