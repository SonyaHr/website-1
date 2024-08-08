from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from .forms import ReviewForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    for product in products:
        product.avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    recommended_products = Product.objects.filter(available=True).order_by('-popularity')[:5]
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'recommended_products': recommended_products,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
    else:
        review_form = ReviewForm()

    # Recommended products except the current one
    recommended_products = Product.objects.filter(available=True).exclude(id=product.id).order_by('-popularity')[:5]

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'recommended_products': recommended_products,
    })
