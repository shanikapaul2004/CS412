from django.shortcuts import render
from django.views.generic import DetailView
from .models import Joke, Picture
import random
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JokeSerializer, PictureSerializer

def random_view(request):
    """Show one random joke and one random picture."""
    jokes = list(Joke.objects.all())
    pictures = list(Picture.objects.all())
    
    random_joke = random.choice(jokes) if jokes else None
    random_picture = random.choice(pictures) if pictures else None
    
    context = {
        'joke': random_joke,
        'picture': random_picture,
    }
    return render(request, 'dadjokes/random.html', context)

def all_jokes(request):
    """Show all jokes."""
    jokes = Joke.objects.all().order_by('-created_at')
    context = {'jokes': jokes}
    return render(request, 'dadjokes/all_jokes.html', context)

def all_pictures(request):
    """Show all pictures."""
    pictures = Picture.objects.all().order_by('-created_at')
    context = {'pictures': pictures}
    return render(request, 'dadjokes/all_pictures.html', context)

class JokeDetailView(DetailView):
    """Show one joke by primary key."""
    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'

class PictureDetailView(DetailView):
    """Show one picture by primary key."""
    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'
    
    
class JokeListAPIView(generics.ListCreateAPIView):
    '''
    API view to return a listing of Jokes and to create a Joke.
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API view to retrieve, update, or delete a single Joke.
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    '''
    API view to return a listing of Pictures.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    '''
    API view to retrieve a single Picture.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

@api_view(['GET'])
def random_joke_api(request):
    '''
    API view to return one random joke.
    '''
    jokes = list(Joke.objects.all())
    if jokes:
        random_joke = random.choice(jokes)
        serializer = JokeSerializer(random_joke)
        return Response(serializer.data)
    return Response({})

@api_view(['GET'])
def random_picture_api(request):
    '''
    API view to return one random picture.
    '''
    pictures = list(Picture.objects.all())
    if pictures:
        random_picture = random.choice(pictures)
        serializer = PictureSerializer(random_picture)
        return Response(serializer.data)
    return Response({})