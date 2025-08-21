from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Product, Category, Order
from django.utils.text import slugify
from django.contrib import messages

# Only staff/admin users
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

# ----------------- DASHBOARD HOME -----------------
@login_required
@staff_required
def dashboard_home(request):
    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
    }
    return render(request, 'dashboard/home.html', context)

# ----------------- PRODUCT MANAGEMENT -----------------
@login_required
@staff_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'dashboard/products.html', {'products': products})

@login_required
@staff_required
def add_product(request):
    # ✅ Fetch only active categories
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        description = request.POST.get("description", "")
        image = request.FILES.get("image")
        stock = request.POST.get("stock", 0)

        if not category_id:
            return render(request, "dashboard/add_product.html", {
                "categories": categories,   # ✅ use filtered categories
                "error": "Please select a category",
            })

        category = get_object_or_404(Category, id=category_id, is_active=True)  # ✅ Ensure only active category can be selected

        Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image,
            stock=stock,
            slug=slugify(name)
        )
        return redirect("manage_products")

    return render(request, "dashboard/add_product.html", {"categories": categories})  # ✅ use filtered categories


@login_required
@staff_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST["name"]
        product.price = request.POST["price"]
        category_id = request.POST["category"]
        product.category = get_object_or_404(Category, id=category_id)
        product.description = request.POST.get("description", "")
        if request.FILES.get("image"):
            product.image = request.FILES["image"]
        product.save()
        return redirect("manage_products")

    return render(request, "dashboard/edit_product.html", {
        "product": product,
        "categories": categories
    })


@login_required
@staff_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('manage_products')  # Redirect back to the products list
    return redirect('manage_products')


# ----------------- CATEGORY MANAGEMENT -----------------
@login_required
@staff_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, "dashboard/categories.html", {"categories": categories})

@login_required
@staff_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        categories = Category.objects.filter(is_active=True)  

        Category.objects.create(name=name, slug=slugify(name))
        return redirect("manage_categories")
    return render(request, "dashboard/add_category.html")



@login_required
@staff_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.slug = slugify(category.name)
        category.save()
        return redirect("manage_categories")

    return render(request, "dashboard/edit_category.html", {"category": category})


def toggle_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.is_active = not category.is_active
    category.save()
    status = "activated" if category.is_active else "deactivated"
    messages.success(request, f"Category '{category.name}' has been {status}.")
    return redirect("manage_categories")  # your categories list view name


@login_required
@staff_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect("manage_categories")



# ----------------- ORDER MANAGEMENT -----------------
@login_required
@staff_required
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, "dashboard/orders.html", {"orders": orders})

