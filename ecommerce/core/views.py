from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Product, Category, Cart, Order, OrderItem
from .forms import ProductForm


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:8]  # latest 8 products
    return render(request, 'index.html', {'categories': categories, 'products': products})

# Admin product list
def product_list(request):
    products = Product.objects.all()
    return render(request, "core/product_list.html", {"products": products})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "core/product_form.html", {"form": form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "core/product_form.html", {"form": form})

# Delete product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")

# def product_list(request):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     return render(request, 'products/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.order_by("-created_at")
    return render(request, "core/category_detail.html", {"category": category, "products": products})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("view_cart")

def view_cart(request):
    cart_items = []  # Replace with actual Cart model query
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    discount = 0  # (later apply coupons/discounts)
    final_price = total_price - discount
    return render(request, "core/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "discount": discount,
        "final_price": final_price
    })


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("view_cart")


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    if not cart.exists():
        return redirect('cart')  # If cart empty, redirect back

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        # Create Order
        order = Order.objects.create(
            user=request.user,
            status="Pending",
            created_at=timezone.now()
        )

        # Add items from cart to order
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.delete()

        if payment_method == "COD":
            order.status = "Confirmed"
            order.save()
            return render(request, "order_success.html", {"order": order})

        elif payment_method == "Online":
            # Razorpay integration will come later
            return redirect("payment_gateway")  

    return render(request, "checkout.html", {"cart": cart})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})