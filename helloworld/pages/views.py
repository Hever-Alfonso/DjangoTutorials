from django import forms
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

class HomePageView (TemplateView):
    template_name = 'pages/home.html'

class AboutPageView (TemplateView):
    template_name = 'pages/about.html'

    def get_context_data (self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titile": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page .",
            "author": "Developed by: Hever Andre Alfonso Jimenez"
        })
        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 200},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 999},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 80},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 120}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView (View):
    template_name = 'products/show.html'

    def get(self, request, id):

        # Intentar convertir el id a entero

        try:
            index = int(id) - 1
        except ValueError:
            return HttpResponseRedirect(reverse('home'))
        
        # Validar que el índice exista dentro de la lista
        if index < 0 or index >= len(Product.products):
            return HttpResponseRedirect(reverse('home'))
        
        # Si es válido, renderizar el producto
        product = Product.products[index]
        
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {}
            viewData["title"] = "Product Created"
            viewData["subtitle"] = "Product Created Successfully"
            viewData["product"] = form.cleaned_data
            return render(request, "products/show.html", viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contact - Online Store"
        context["subtitle"] = "Contact"
        context["email"] = "contact@onlinestore.com"
        context["address"] = "Calle falsa 123, Medellín, Antioquia"
        context["phone"] = "+57 300 000 0000"
        return context