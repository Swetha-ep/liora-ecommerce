from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def products(request):
    return render(request,'products.html')

def shop(request):
    categories = Categories.objects.all()
    return render(request,'shop.html',{'categories' : categories})