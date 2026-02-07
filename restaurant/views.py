from django.shortcuts import render
import random
import time

# Create your views here.

specials = [
    {"name": "Arroz Meloso", "price": 16},
    {"name": "Carpaccio de Pulpo", "price": 18},
    {"name": "Salmorejo", "price": 12}
]

def main(request):

    template_name = "restaurant/main.html"
    return render(request, template_name)


def order(request):
    template_name = "restaurant/order.html"
    
    daily_special = random.choice(specials)
    
    context = {
        'daily_special': daily_special
    }
    
    return render(request, template_name, context=context)



def submit(request):
    template_name = "restaurant/confirmation.html"
    
    if request.POST:
        name = request.POST.get('name', '')
        phone_num = request.POST.get('phone_num', '')
        dietary_restrictions = request.POST.get('dietary_restrictions', '')
        
        ordered_items = []
        total_price = 0
        
        if request.POST.get('food1'):
            ordered_items.append("Ceviche")
            total_price += 12
            
        if request.POST.get('food2'):
            ordered_items.append("Patatas Bravas")
            total_price += 14
            
        if request.POST.get('food3'):
            ordered_items.append("Montaditos")
            total_price += 10
            
        if request.POST.get('food4'):
            ordered_items.append("Montaditos - Chorizo Jam + Goat Cheese")
            
        if request.POST.get('food5'):
            ordered_items.append("Montaditos - Pan con Tomate")
            
        if request.POST.get('food6'):
            ordered_items.append("Carilleras")
            total_price += 34
            
        if request.POST.get('daily_special'):
            special_name = request.POST.get('daily_special_name', '')
            special_price = int(request.POST.get('daily_special_price', 0))
            ordered_items.append(f"{special_name} (Daily Special)")
            total_price += special_price
        
        current_time = time.time()
        minutes_to_wait = random.randint(30, 60)
        ready_time = current_time + (minutes_to_wait * 60)
        ready_time_final = time.ctime(ready_time)
        
        context = {
            'name': name,
            'phone_num': phone_num,
            'ordered_items': ordered_items,
            'dietary_restrictions': dietary_restrictions,
            'total_price': total_price,
            'ready_time': ready_time_final
        }
        
        return render(request, template_name, context=context)
 
