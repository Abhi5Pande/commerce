
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    MOTORS = "MOT"
    FASHION = "FAS"
    ELECTRONICS = "ELE"
    COLLECTIBLES_ARTS = "ART"
    HOME_GARDES = "HGA"
    SPORTING_GOODS = "SPO"
    TOYS = "TOY"
    BUSSINES_INDUSTRIAL = "BUS"
    MUSIC = "MUS"
    CATEGORY = [
        (MOTORS,"Motors"),
        (FASHION,"Fashion"),
        (ELECTRONICS, "Electronics"),
        (COLLECTIBLES_ARTS, "Collectibles & Art"),
        (HOME_GARDES, "Home & Garden"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys"),
        (BUSSINES_INDUSTRIAL, "Business & Industrial"),
        (MUSIC, "Music"),
    ]
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    descritption = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default =0.0)
    category = models.CharField(max_length=3,choices=CATEGORY,default=MOTORS)
    image_url = models.URLField(blank=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction id : {self.id}, title: {self.title}, seller: {self.seller}"

class Watchlist(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, related_name='watchlist')
    auctions = models.ManyToManyField('Listing',related_name='item',blank=True)

    def __str__(self):
        return f"Watchlist for {self.user}"
class Bid(models.Model):
    item = models.ForeignKey('Listing', on_delete=models.CASCADE,related_name='item_bid')
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name="user")
    bid = models.DecimalField(max_digits=11, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.item} - {self.bid}"

