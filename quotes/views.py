# file: quotes/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Global lists for quotes and images (all from the same famous person)
# Using Walt Disney
quotes = [
    "All our dreams can come true, if we have the courage to pursue them.",
    "First, think. Second, believe. Third, dream. And finally, dare",
    "When you believe in a thing, believe in it all the way, implicitly and unquestionable.",
    "The more you like yourself, the less you are like anyone else, which makes you unique.",
    "Our greatest natural resource is the minds of our children."
]

images = [
    "https://www.archbridgeinstitute.org/wp-content/uploads/2020/08/walt_disney-01-e1643252504901.webp",
    "https://m.media-amazon.com/images/I/81ZCz35CxGL._UF1000,1000_QL80_.jpg",
    "https://i.ebayimg.com/images/g/N3EAAOSwiSlkspaK/s-l1200.jpg",
    "https://hips.hearstapps.com/hmg-prod/images/1_american-producer-director-and-animator-walt-disney-1901---1966-uses-a-baton-to-point-to-sketches-of-disneyland-1955-photo-by-hulton-archivegetty-images.jpg",
    "https://d23.com/app/uploads/2018/01/047_372-205c.jpg",
]

def home(request):
    '''Function that responds to the "home" request.'''
    
    response_text = f'''
    <html> 
        <h1> Hello, world  </h1>
        The current time is {time.ctime()}.
    </html>
    '''
    
    return HttpResponse(response_text)

def home(request):
    '''Home page view - shows random quote and image (same as quote page)'''
    
    template_name = 'quotes/quote.html'  # Uses the same template as quote
    
    # Select random quote and image
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    
    context = {
        "time": time.ctime(), 
        "letter1": chr(random.randint(65,90)), 
        "letter2": chr(random.randint(65,90)), 
        "number": random.randint(1,10),
        "quote": random_quote,
        "image": random_image,
    }
    
    return render(request, template_name, context)

def quote(request):
    '''Main page view - shows random quote and image'''
    
    template_name = 'quotes/quote.html'
    
    # Select random quote and image
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    
    context = {
        "time": time.ctime(), 
        "letter1": chr(random.randint(65,90)), 
        "letter2": chr(random.randint(65,90)), 
        "number": random.randint(1,10),
        "quote": random_quote,
        "image": random_image,
    }
    
    return render(request, template_name, context)

def home_page(request):
    '''Respond to the URL, delegate work to a template'''
    
    template_name = 'quotes/home.html'
    
    #this is the dictionary for context variables 
    context = {
        "time": time.ctime(), 
        "letter1": chr(random.randint(65,90)), 
        "letter2": chr(random.randint(65,90)), 
        "number": random.randint(1,10), 
    }
    
    return render(request, template_name, context)

def show_all(request):
    '''Show all quotes and images'''
    
    template_name = 'quotes/show_all.html'
    
    context = {
        "time": time.ctime(), 
        "letter1": chr(random.randint(65,90)), 
        "letter2": chr(random.randint(65,90)), 
        "number": random.randint(1,10),
        "quotes": quotes,  # Pass entire list
        "images": images,  # Pass entire list
    }
    
    return render(request, template_name, context)

def about(request):
    '''Respond to the URL 'about', delegate work to a template'''
    
    template_name = 'quotes/about.html'
    
    #this is the dictionary for context variables 
    context = {
        "time": time.ctime(), 
        "letter1": chr(random.randint(65,90)), 
        "letter2": chr(random.randint(65,90)), 
        "number": random.randint(1,10), 
    }
    
    return render(request, template_name, context)