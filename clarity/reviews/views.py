"""This is a views file that holds functions or renders activated via url."""

from django.shortcuts import render, redirect
from .forms import ReviewForm
from services.models import Service
from .models import Review
from django.db.models import Q, Avg

# This is the review page view.
def reviews(request):
    form = None

    # Checking if user is logged in.
    if request.user.is_authenticated:

        # Checking if user is sending a response to the form.
        if request.method == "POST":
            form = ReviewForm(request.POST)

            # If form is valid then save user to the review and determining if it is a verifed review.
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
            
        # If not sending response to the form then just display form.
        else:
            form = ReviewForm()

    # Collecting variables to display on the page.
    reviews = Review.objects.all().order_by("-created")
    avg_rating = Review.objects.aggregate(Avg('stars'))['stars__avg']
    context = {"form": form, "reviews": reviews, "avg_rating":avg_rating, 'star_range': range(1, 6),}

    # Rendering 'reviews.html' and parsing in context defined above.
    return render(request, "reviews.html", context)