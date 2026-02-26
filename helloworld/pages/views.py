from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError

# Importamos el modelo Product desde la base de datos
# Ya no usamos la clase Product con lista hardcodeada
from .models import Product


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titile": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page .",
            "author": "Developed by: Hever Andre Alfonso Jimenez"
        })
        return context


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        # Antes: Product.products (lista hardcodeada)
        # Ahora: consultamos todos los productos reales de la base de datos
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            # Antes: buscabamos en la lista hardcodeada por indice
            # Ahora: buscamos en la BD por primary key, retorna 404 si no existe
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductForm(forms.ModelForm):
    """
    Formulario basado en el modelo Product.
    Antes usaba forms.Form con campos manuales.
    Ahora usa ModelForm que los toma directamente del modelo.
    """

    class Meta:
        # Le indica a Django que modelo usar para generar el formulario
        model = Product
        # Solo mostramos estos dos campos en el formulario
        fields = ['name', 'price']

    def clean_price(self):
        # Validacion: el precio debe ser mayor que cero
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
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
            # Antes: no guardaba nada en la BD
            # Ahora: form.save() guarda el producto nuevo directamente en la BD
            form.save()
            return redirect('product-created')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)


class ProductCreatedView(TemplateView):
    """
    Vista de confirmacion que se muestra despues de crear un producto exitosamente.
    Recibe el control despues de que ProductCreateView guarda el producto en la BD.
    """
    template_name = 'products/created.html'


class ProductListView(ListView):
    """
    Vista generica de Django para listar objetos de un modelo.
    Mas simple que ProductIndexView, Django hace el trabajo automaticamente.
    """

    model = Product
    template_name = 'product_list.html'
    # Nombre de la variable con la que accedemos a los productos en el template
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


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


class CartView(View):
    """
    Vista del carrito de compras. Usa sesiones de Django para persistir
    los productos seleccionados entre peticiones sin necesidad de base de datos.

    GET: muestra todos los productos disponibles y los que estan en el carrito.
    POST: agrega un producto al carrito guardando su ID en la sesion.
    """
    template_name = 'cart/index.html'

    def get(self, request):
        # Base de datos simulada de productos disponibles
        # En una app real esto vendria de la BD (e.g. Product.objects.all())
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}

        # Recuperamos los IDs guardados en sesion y filtramos los productos del carrito
        # request.session actua como un diccionario persistente entre peticiones
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})
        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Preparamos los datos que recibira el template
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }
        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Recuperamos el carrito actual de la sesion (o un dict vacio si no existe)
        cart_product_data = request.session.get('cart_product_data', {})

        # Agregamos el nuevo producto usando su ID como clave
        cart_product_data[product_id] = product_id

        # Guardamos el carrito actualizado en la sesion
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')


class CartRemoveAllView(View):
    """
    Vista para vaciar el carrito de compras.
    Elimina la clave 'cart_product_data' de la sesion actual.
    Solo responde a POST para seguir el patron de seguridad REST
    (las acciones destructivas no deben hacerse con GET).
    """

    def post(self, request):
        # Solo borramos si la clave existe para evitar KeyError
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')