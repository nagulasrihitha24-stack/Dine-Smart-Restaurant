# app.py (fixed - payment goes directly to receipt)
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'dinesmart-secret-key-2026'

# Complete Menu with 50+ items across categories
MENU_ITEMS = {
    'starters': {
        'name': 'Starters & Appetizers',
        'icon': '🍢',
        'items': {
            'spring_rolls': {'name': 'Spring Rolls', 'price': 120, 'emoji': '🌯', 'veg': True, 'description': 'Crispy vegetable spring rolls with sweet chili sauce'},
            'manchurian': {'name': 'Gobi Manchurian', 'price': 150, 'emoji': '🥘', 'veg': True, 'description': 'Crispy cauliflower in Indo-Chinese sauce'},
            'chicken_tikka': {'name': 'Chicken Tikka', 'price': 250, 'emoji': '🍗', 'veg': False, 'description': 'Grilled chicken marinated in aromatic spices'},
            'paneer_tikka': {'name': 'Paneer Tikka', 'price': 180, 'emoji': '🧀', 'veg': True, 'description': 'Grilled cottage cheese with bell peppers'},
            'samosa': {'name': 'Samosa', 'price': 60, 'emoji': '🥟', 'veg': True, 'description': 'Crispy pastry filled with spiced potatoes'},
            'dahi_puri': {'name': 'Dahi Puri', 'price': 90, 'emoji': '🍘', 'veg': True, 'description': 'Crispy puri with yogurt and chutney'},
            'chicken_wings': {'name': 'Chicken Wings', 'price': 280, 'emoji': '🍗', 'veg': False, 'description': 'Spicy fried chicken wings with dip'},
            'cheese_balls': {'name': 'Cheese Balls', 'price': 160, 'emoji': '🧀', 'veg': True, 'description': 'Crispy cheese filled balls'},
            'onion_rings': {'name': 'Onion Rings', 'price': 110, 'emoji': '🧅', 'veg': True, 'description': 'Crispy fried onion rings'},
            'fish_fingers': {'name': 'Fish Fingers', 'price': 220, 'emoji': '🐟', 'veg': False, 'description': 'Crispy fish strips with tartar sauce'}
        }
    },
    'pizza': {
        'name': 'Artisan Pizzas',
        'icon': '🍕',
        'items': {
            'margherita': {'name': 'Margherita', 'price': 200, 'emoji': '🍕', 'veg': True, 'description': 'Classic with tomato, mozzarella, fresh basil'},
            'pepperoni': {'name': 'Pepperoni', 'price': 280, 'emoji': '🍕', 'veg': False, 'description': 'Spicy pepperoni with extra cheese'},
            'farmhouse': {'name': 'Farmhouse', 'price': 250, 'emoji': '🥬', 'veg': True, 'description': 'Fresh bell peppers, onions, tomatoes, corn'},
            'chicken_tikka_pizza': {'name': 'Chicken Tikka', 'price': 300, 'emoji': '🍗', 'veg': False, 'description': 'Tandoori chicken with onions'},
            'bbq_chicken': {'name': 'BBQ Chicken', 'price': 310, 'emoji': '🍖', 'veg': False, 'description': 'BBQ sauce with grilled chicken'},
            'mexican_green_wave': {'name': 'Mexican Green Wave', 'price': 270, 'emoji': '🌿', 'veg': True, 'description': 'Jalapenos, bell peppers, corn, olives'},
            'cheese_corn': {'name': 'Cheese Corn', 'price': 240, 'emoji': '🌽', 'veg': True, 'description': 'Sweet corn with extra cheese'},
            'spicy_paneer': {'name': 'Spicy Paneer', 'price': 260, 'emoji': '🧀', 'veg': True, 'description': 'Tandoori paneer with spicy sauce'}
        }
    },
    'burgers': {
        'name': 'Gourmet Burgers',
        'icon': '🍔',
        'items': {
            'classic_veggie': {'name': 'Classic Veggie', 'price': 100, 'emoji': '🍔', 'veg': True, 'description': 'Lettuce, tomato, onion, cheese'},
            'chicken_burger': {'name': 'Chicken Burger', 'price': 150, 'emoji': '🍔', 'veg': False, 'description': 'Grilled chicken patty with mayo'},
            'double_cheese': {'name': 'Double Cheese', 'price': 180, 'emoji': '🧀', 'veg': True, 'description': 'Two cheese slices with special sauce'},
            'mushroom_swiss': {'name': 'Mushroom Swiss', 'price': 190, 'emoji': '🍄', 'veg': True, 'description': 'Sautéed mushrooms with Swiss cheese'},
            'bacon_burger': {'name': 'Bacon Burger', 'price': 250, 'emoji': '🥓', 'veg': False, 'description': 'Crispy bacon with beef patty'},
            'spicy_crispy_chicken': {'name': 'Spicy Crispy Chicken', 'price': 170, 'emoji': '🐔', 'veg': False, 'description': 'Crispy chicken with spicy mayo'},
            'vegan_burger': {'name': 'Vegan Burger', 'price': 160, 'emoji': '🌱', 'veg': True, 'description': 'Plant-based patty with avocado'}
        }
    },
    'pasta': {
        'name': 'Pasta & Noodles',
        'icon': '🍝',
        'items': {
            'white_sauce': {'name': 'White Sauce Pasta', 'price': 150, 'emoji': '🍝', 'veg': True, 'description': 'Creamy Alfredo sauce with herbs'},
            'red_sauce': {'name': 'Red Sauce Pasta', 'price': 140, 'emoji': '🍝', 'veg': True, 'description': 'Tangy tomato and basil sauce'},
            'pink_sauce': {'name': 'Pink Sauce Pasta', 'price': 160, 'emoji': '🎀', 'veg': True, 'description': 'Creamy tomato sauce'},
            'chicken_alfredo': {'name': 'Chicken Alfredo', 'price': 220, 'emoji': '🐔', 'veg': False, 'description': 'Grilled chicken with creamy sauce'},
            'arrabiata': {'name': 'Arrabiata Pasta', 'price': 155, 'emoji': '🌶️', 'veg': True, 'description': 'Spicy tomato and garlic sauce'},
            'pesto_pasta': {'name': 'Pesto Pasta', 'price': 170, 'emoji': '🌿', 'veg': True, 'description': 'Fresh basil pesto with pine nuts'},
            'hakka_noodles': {'name': 'Hakka Noodles', 'price': 130, 'emoji': '🥢', 'veg': True, 'description': 'Indo-Chinese style noodles'},
            'chicken_noodles': {'name': 'Chicken Noodles', 'price': 180, 'emoji': '🥢', 'veg': False, 'description': 'Noodles with chicken and vegetables'}
        }
    },
    'main_course': {
        'name': 'Main Course',
        'icon': '🍛',
        'items': {
            'butter_chicken': {'name': 'Butter Chicken', 'price': 280, 'emoji': '🍗', 'veg': False, 'description': 'Creamy tomato gravy with tender chicken'},
            'paneer_butter_masala': {'name': 'Paneer Butter Masala', 'price': 220, 'emoji': '🧀', 'veg': True, 'description': 'Cottage cheese in rich gravy'},
            'dal_makhani': {'name': 'Dal Makhani', 'price': 180, 'emoji': '🥘', 'veg': True, 'description': 'Creamy black lentils'},
            'chicken_biryani': {'name': 'Chicken Biryani', 'price': 260, 'emoji': '🍚', 'veg': False, 'description': 'Fragrant rice with spiced chicken'},
            'veggie_biryani': {'name': 'Veg Biryani', 'price': 200, 'emoji': '🍚', 'veg': True, 'description': 'Aromatic rice with mixed vegetables'},
            'fish_curry': {'name': 'Fish Curry', 'price': 290, 'emoji': '🐟', 'veg': False, 'description': 'Tangy coconut fish curry'},
            'kadai_paneer': {'name': 'Kadai Paneer', 'price': 210, 'emoji': '🧀', 'veg': True, 'description': 'Paneer cooked with bell peppers'},
            'egg_curry': {'name': 'Egg Curry', 'price': 160, 'emoji': '🥚', 'veg': False, 'description': 'Spicy boiled eggs in curry'},
            'mutton_rogan_josh': {'name': 'Mutton Rogan Josh', 'price': 350, 'emoji': '🍖', 'veg': False, 'description': 'Kashmiri style lamb curry'},
            'palak_paneer': {'name': 'Palak Paneer', 'price': 200, 'emoji': '🥬', 'veg': True, 'description': 'Paneer in spinach gravy'}
        }
    },
    'sides': {
        'name': 'Sides & Extras',
        'icon': '🍟',
        'items': {
            'french_fries': {'name': 'French Fries', 'price': 80, 'emoji': '🍟', 'veg': True, 'description': 'Crispy golden fries with seasoning'},
            'garlic_bread': {'name': 'Garlic Bread', 'price': 90, 'emoji': '🥖', 'veg': True, 'description': 'Toasted bread with garlic butter'},
            'cheesy_dip': {'name': 'Cheesy Dip', 'price': 50, 'emoji': '🧀', 'veg': True, 'description': 'Melted cheese dip'},
            'masala_papad': {'name': 'Masala Papad', 'price': 40, 'emoji': '🍘', 'veg': True, 'description': 'Crispy papad with toppings'},
            'salad_bowl': {'name': 'Fresh Salad Bowl', 'price': 70, 'emoji': '🥗', 'veg': True, 'description': 'Mixed greens with dressing'},
            'onion_rings_small': {'name': 'Onion Rings', 'price': 60, 'emoji': '🧅', 'veg': True, 'description': 'Crispy onion rings'}
        }
    },
    'desserts': {
        'name': 'Desserts',
        'icon': '🍰',
        'items': {
            'gulab_jamun': {'name': 'Gulab Jamun', 'price': 80, 'emoji': '🍡', 'veg': True, 'description': 'Soft milk dumplings in sugar syrup'},
            'brownie': {'name': 'Chocolate Brownie', 'price': 120, 'emoji': '🍫', 'veg': True, 'description': 'Warm brownie with chocolate sauce'},
            'ice_cream': {'name': 'Ice Cream', 'price': 90, 'emoji': '🍨', 'veg': True, 'description': 'Vanilla/Chocolate/Strawberry'},
            'rasmalai': {'name': 'Rasmalai', 'price': 110, 'emoji': '🍮', 'veg': True, 'description': 'Cottage cheese in sweet milk'},
            'cheesecake': {'name': 'Cheesecake', 'price': 150, 'emoji': '🍰', 'veg': True, 'description': 'New York style cheesecake'},
            'choco_lava_cake': {'name': 'Choco Lava Cake', 'price': 130, 'emoji': '🎂', 'veg': True, 'description': 'Cake with molten chocolate center'},
            'kheer': {'name': 'Rice Kheer', 'price': 90, 'emoji': '🍚', 'veg': True, 'description': 'Traditional rice pudding'}
        }
    },
    'beverages': {
        'name': 'Beverages',
        'icon': '🥤',
        'items': {
            'coke': {'name': 'Coca Cola', 'price': 40, 'emoji': '🥤', 'veg': True, 'description': '330ml can'},
            'soda': {'name': 'Soda', 'price': 30, 'emoji': '🥤', 'veg': True, 'description': 'Sparkling water'},
            'fresh_lime': {'name': 'Fresh Lime Soda', 'price': 50, 'emoji': '🍋', 'veg': True, 'description': 'Sweet/salted lime soda'},
            'buttermilk': {'name': 'Buttermilk', 'price': 40, 'emoji': '🥛', 'veg': True, 'description': 'Spiced yogurt drink'},
            'mango_shake': {'name': 'Mango Shake', 'price': 90, 'emoji': '🥭', 'veg': True, 'description': 'Fresh mango milkshake'},
            'cold_coffee': {'name': 'Cold Coffee', 'price': 80, 'emoji': '☕', 'veg': True, 'description': 'Chilled coffee with ice cream'},
            'masala_chai': {'name': 'Masala Chai', 'price': 40, 'emoji': '🍵', 'veg': True, 'description': 'Indian spiced tea'},
            'mineral_water': {'name': 'Mineral Water', 'price': 20, 'emoji': '💧', 'veg': True, 'description': '1 liter bottle'},
            'orange_juice': {'name': 'Orange Juice', 'price': 70, 'emoji': '🍊', 'veg': True, 'description': 'Freshly squeezed'},
            'mint_mojito': {'name': 'Mint Mojito', 'price': 85, 'emoji': '🌿', 'veg': True, 'description': 'Refreshing mint drink'}
        }
    }
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', 'Guest')
        session['username'] = username
        return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        order = {}
        total = 0
        
        for category_key, category in MENU_ITEMS.items():
            for item_id, item in category['items'].items():
                qty = int(request.form.get(item_id, 0))
                if qty > 0:
                    order[item_id] = {
                        'name': item['name'],
                        'price': item['price'],
                        'qty': qty,
                        'emoji': item['emoji'],
                        'category': category_key
                    }
                    total += qty * item['price']
        
        if not order:
            return render_template('menu.html', menu_items=MENU_ITEMS, error="Please select at least one item!")
        
        session['order'] = order
        session['total_amount'] = total
        return redirect(url_for('booking'))
    
    return render_template('menu.html', menu_items=MENU_ITEMS)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        persons = request.form.get('persons')
        
        if not date or not time or not persons:
            return render_template('booking.html', error="Please fill all booking details!")
        
        session['booking'] = {'date': date, 'time': time, 'persons': persons}
        return redirect(url_for('bill'))
    
    return render_template('booking.html')

@app.route('/bill', methods=['GET', 'POST'])
def bill():
    total = session.get('total_amount', 0)
    order = session.get('order', {})
    
    if request.method == 'POST':
        payment_method = request.form.get('payment')
        session['payment_method'] = payment_method
        # After payment, go directly to receipt
        return redirect(url_for('receipt'))
    
    # Get order details for display
    order_items = []
    for item_id, item_data in order.items():
        order_items.append({
            'name': item_data['name'],
            'qty': item_data['qty'],
            'price': item_data['price'],
            'subtotal': item_data['qty'] * item_data['price']
        })
    
    return render_template('bill.html', total=total, order_items=order_items)

@app.route('/receipt')
def receipt():
    """Generate and display receipt after payment"""
    order = session.get('order', {})
    total = session.get('total_amount', 0)
    booking = session.get('booking', {})
    username = session.get('username', 'Guest')
    payment_method = session.get('payment_method', 'Not Specified')
    
    # Get current date and time
    now = datetime.now()
    receipt_number = f"DS{now.strftime('%Y%m%d%H%M%S')}"
    
    # Prepare order items
    order_items = []
    for item_id, item_data in order.items():
        order_items.append({
            'name': item_data['name'],
            'qty': item_data['qty'],
            'price': item_data['price'],
            'subtotal': item_data['qty'] * item_data['price']
        })
    
    # Calculate taxes
    gst = round(total * 0.05, 2)
    service_charge = round(total * 0.10, 2)
    grand_total = round(total + gst + service_charge, 2)
    
    receipt_data = {
        'receipt_number': receipt_number,
        'date': now.strftime('%d/%m/%Y'),
        'time': now.strftime('%H:%M:%S'),
        'customer_name': username,
        'order_items': order_items,
        'total': total,
        'booking_date': booking.get('date', 'N/A'),
        'booking_time': booking.get('time', 'N/A'),
        'persons': booking.get('persons', 'N/A'),
        'payment_method': payment_method,
        'gst': gst,
        'service_charge': service_charge,
        'grand_total': grand_total
    }
    
    return render_template('receipt.html', receipt=receipt_data)

@app.route('/download-receipt')
def download_receipt():
    """Download receipt as HTML file"""
    order = session.get('order', {})
    total = session.get('total_amount', 0)
    booking = session.get('booking', {})
    username = session.get('username', 'Guest')
    payment_method = session.get('payment_method', 'Not Specified')
    
    now = datetime.now()
    receipt_number = f"DS{now.strftime('%Y%m%d%H%M%S')}"
    
    order_items = []
    for item_id, item_data in order.items():
        order_items.append({
            'name': item_data['name'],
            'qty': item_data['qty'],
            'price': item_data['price'],
            'subtotal': item_data['qty'] * item_data['price']
        })
    
    gst = round(total * 0.05, 2)
    service_charge = round(total * 0.10, 2)
    grand_total = round(total + gst + service_charge, 2)
    
    receipt_data = {
        'receipt_number': receipt_number,
        'date': now.strftime('%d/%m/%Y'),
        'time': now.strftime('%H:%M:%S'),
        'customer_name': username,
        'order_items': order_items,
        'total': total,
        'booking_date': booking.get('date', 'N/A'),
        'booking_time': booking.get('time', 'N/A'),
        'persons': booking.get('persons', 'N/A'),
        'payment_method': payment_method,
        'gst': gst,
        'service_charge': service_charge,
        'grand_total': grand_total
    }
    
    # Create HTML content for download
    html_content = render_template('receipt_print.html', receipt=receipt_data)
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = f'attachment; filename=receipt_{receipt_number}.html'
    return response

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating')
        feedback_text = request.form.get('feedback')
        session['feedback'] = {'rating': rating, 'text': feedback_text}
        return render_template('thankyou.html')
    
    return render_template('feedback.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/clear-session')
def clear_session():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)