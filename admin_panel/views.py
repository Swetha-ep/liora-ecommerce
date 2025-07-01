from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'admin/dashboard.html')

def products_list(request):
    return render(request, 'products/products_list.html')