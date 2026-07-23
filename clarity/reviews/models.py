from django.db import models
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Review(models.Model):
    STARS_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    stars = models.IntegerField(choices=STARS_CHOICES)
    message = models.TextField()
    used = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='ReviewCategory', blank=True)
    tutor = models.ForeignKey(CustomUser, related_name='review_of_tutor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class ReviewCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.review.user.first_name