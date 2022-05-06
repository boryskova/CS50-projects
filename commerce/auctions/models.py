from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Auction(models.Model):
    AUCTION_CATEGORY_CHOICES = [
    ('1', 'Furniture'),
    ('2', 'Books'),
    ('3', 'Gadgets'),
    ('4', 'Household appliances'),
    ('5', 'Accessories'),
    ('6', 'Clothing'),
    ('7', 'Makeup'),
    ('8', 'For children'),
    ('9', 'For animals'),
    ('10', 'Car accessories'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    name = models.CharField("lot name", max_length=255)
    minimum_bid = models.DecimalField("lot minimum bid", max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    description = models.CharField("lot description", max_length=3000)
    image = models.ImageField("lot image", upload_to='images', default='images/placeholder.jpg', blank=True)
    category = models.CharField("lot category", choices=AUCTION_CATEGORY_CHOICES, max_length=30, blank=True)
    current_bid = models.DecimalField("current lot bid", max_digits=7, decimal_places=2, default=0.00)
    active = models.BooleanField("is active", default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winner")

    def save(self, *args, **kwargs):
        if self.current_bid == 0.00:
            self.current_bid = self.minimum_bid
        super(Auction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}:{self.name}"


class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.DecimalField("bid", max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment_text = models.CharField("comment", max_length=300)
    added = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, null=True, on_delete=models.SET_NULL)



