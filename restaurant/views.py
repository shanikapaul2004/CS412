from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
from datetime import datetime, timedelta

def main(request):
    '''Main restaurant page with basic information'''
    
    template_name = 'restaurant/main.html'
    
    context = {
        'restaurant_name': 'Pho Queen',
        'location': '444 Marlborough Ave, Boston, MA 02134',
        'Phone': '(000) 000-0000 ',
        'Hours': [
            {'day': 'Monday - Thursday', 'time': '11:00 AM - 9:00 PM'},
            {'day': 'Friday - Saturday', 'time': '11:00 AM - 10:00 PM'},
            {'day': 'Sunday', 'time': '12:00 PM - 8:00 PM'},
        ]

    }
    return render(request, template_name, context)

def order(request):
    '''Order page'''
    template_name = "restaurant/order.html"
    
    menu_items = [
         {'name': 'Pho Sao Mai', 'price': 17.00, 'id': 'pho_sao_mai', 'description':'House Special Pho (beef brisket, beef ball, and tripe'},
         {'name': 'Pho Tai', 'price': 17.00, 'id': 'pho_tai', 'description': 'Beef Eye Round Pho (thinly sliced rare beef)'},
         {'name': 'Pho Chin Nam', 'price': 17.00, 'id': 'pho_chin_nam', 'description': 'Beef Brisket Pho'},
         {'name': 'Pho Bo Vien', 'price': 15.00, 'id': 'pho_bo_vien', 'description': 'Beef Ball Pho'},
         {'name': 'Pho Ga', 'price': 15.00, 'id': 'pho_ga', 'description':'Chicken Pho (chicken, carrots, broccoli and celery) in a chicken broth'},
         {'name': 'Pho Do Chay', 'price': 15.00, 'id': 'pho_do_chay', 'description':'Vegetarian Pho (tofu and mixed veggies) in a vegetarian broth'},
         {'name': 'Pho Do Bien', 'price': 15.00, 'id': 'pho_do_bien', 'description':'Seafood Pho (shrimp, squid, fish ball and fish cake) in a chicken broth'},  
    ]
    
    daily_specials = [
        {'name': 'Bun Bo Hue', 'price': 16.50, 'description': 'Spicy beef noodle soup'},
        {'name': 'Banh Mi Combo', 'price': 12.99, 'description': 'Vietnamese sandwich with pho'},
        {'name': 'Pho Dac Biet', 'price': 19.99, 'description': 'House special with all meats'},
    ]
    
    # Randomly select daily special
    daily_special = random.choice(daily_specials)
    context = {
        'menu_items': menu_items,
        'daily_special' : daily_special,
    }
    
    return render(request, template_name, context)

def confirmation(request):
    '''Confirmation page'''
    template_name = 'restaurant/confirmation.html'

    print(request.POST)
    
    if request.POST: 
        # Get customer information
        customer_name = request.POST['customer_name']
        customer_phone = request.POST['customer_phone']
        special_instructions = request.POST['special_instructions']
        
        # Get ordered items and calculate total
        ordered_items = []
        total_price = 0.0
        
        # Check each pho item (update these IDs to match your actual form field names)
        if 'pho_sao_mai' in request.POST:
            ordered_items.append({'name': 'Pho Sao Mai', 'price': 17.00})
            total_price += 17.00
            
        if 'pho_tai' in request.POST:
            ordered_items.append({'name': 'Pho Tai', 'price': 17.00})
            total_price += 17.00
            
        if 'pho_chin_nam' in request.POST:
            ordered_items.append({'name': 'Pho Chin Nam', 'price': 17.00})
            total_price += 17.00
            
        if 'pho_bo_vien' in request.POST:
            ordered_items.append({'name': 'Pho Bo Vien', 'price': 15.00})
            total_price += 15.00
            
        if 'pho_ga' in request.POST:
            ordered_items.append({'name': 'Pho Ga', 'price': 15.00})
            total_price += 15.00
            
        if 'pho_do_chay' in request.POST:
            ordered_items.append({'name': 'Pho Do Chay', 'price': 15.00})
            total_price += 15.00
            
        if 'pho_do_bien' in request.POST:
            ordered_items.append({'name': 'Pho Do Bien', 'price': 15.00})
            total_price += 15.00
            
        # Add this after your existing pho checking code
        if 'daily_special' in request.POST:
            special_name = request.POST['daily_special_name']
            special_price = float(request.POST['daily_special'])
            ordered_items.append({'name': special_name, 'price': special_price})
            total_price += special_price
        
        # Calculate ready time (30-60 minutes from now)
        current_time = datetime.now()
        minutes_to_add = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=minutes_to_add)
        
        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time.strftime('%I:%M %p'),
        }
        
    return render(request, template_name, context)