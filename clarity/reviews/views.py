from django.shortcuts import render, redirect
from .forms import ReviewForm
from services.models import Service
from .models import Review
from django.db.models import Q, Avg

# Create your views here.
def reviews(request):
    form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.used = Service.objects.filter(
                    Q(caregiver=request.user) |
                    Q(student=request.user) |
                    Q(tutor=request.user)
                ).exists()
                review.save()
                return redirect("/reviews/")
        else:
            form = ReviewForm()

    reviews = Review.objects.all().order_by("-created")
    avg_rating = Review.objects.aggregate(Avg('stars'))['stars__avg']

    return render(request, "reviews.html", {"form": form, "reviews": reviews, "avg_rating":avg_rating})