
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Watchlist,Bid
from django import forms

class NewItemForm(forms.Form):
    title = forms.CharField(label="title" , max_length=20, required=True, widget=forms.TextInput(attrs={
                                                                            "autocomplete": "off",
                                                                            "aria-label": "title",
                                                                            "class": "form-control"
                                                                        }))

    description = forms.CharField(label="Description", widget = forms.Textarea(attrs={
        "placeholder":"More about the Product",
        "class":"form-control"
    }))
    image_url = forms.URLField(label="Image URL", required=True, widget=forms.URLInput(attrs={
                                        "class": "form-control"
                                    }))
    category = forms.ChoiceField(required=True, choices=Listing.CATEGORY, widget=forms.Select(attrs={
        "class": "form-control"
    }))

def index(request):
    l = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings":l
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            watchlist = Watchlist(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request):
    l = Listing.objects.all()
    watchlist_items = Watchlist.objects.get(user=request.user)
    return render(request,"auctions/listing.html",{
        "listings":l,
        "watchlist":watchlist_items.auctions.all(),
        "user":request.user
    })

def close_item(request,p_id):
    item = Listing.objects.get(pk=p_id)
    item.closed = True
    item.save()
    return HttpResponseRedirect(reverse('listing'))
    

def show_category(request,category):
    items = Listing.objects.filter(category=category)
    return render(request,"auctions/listing.html",{
        "listings":items,
        "cat": category
    })


def item(request,p_id):
    item = Listing.objects.get(pk = p_id)
    bid = Bid.objects.filter(item = item)
    if bid:
        return render(request,"auctions/item.html",{
            "item":item,
            "bid":bid.order_by('-bid')[0]
        })
    return render(request,"auctions/item.html",{
            "item":item,
            "msg":"No bids yet"
        })

def view_watchlist(request):
     watchlist_items = Watchlist.objects.get(user=request.user)
     return render(request, "auctions/watchlist.html", {
        "watchlist":watchlist_items.auctions.all()
     })

def add_watchlist(request, p_id):
    item = Listing.objects.get(pk=p_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.auctions.add(item)
    watchlist.save()
    return render(request,"auctions/watchlist.html",{
        "watchlist": watchlist.auctions.all()
    })

def remove_watchlist(request,p_id):
    item = Listing.objects.get(pk=p_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.auctions.remove(item)
    watchlist.save()
    return render(request,"auctions/watchlist.html",{
        "watchlist": watchlist.auctions.all()
    })
    
def add_item(request):
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]
            listing = Listing(
                seller = request.user,
                title = title,
                descritption = description,
                category = category,
                image_url = image_url
            )
            listing.save()
            return HttpResponseRedirect(reverse('listing'))
        else:
            return render(request, "auctions/addItem.html",{
                "message":"Invalid Data",
                "form":form
            })
    
    return render(request, "auctions/addItem.html",{
        "form":NewItemForm()
    })

def addBid(request,p_id):
    if request.method == "POST":
        bid_price = request.POST['bid_price']
        item = Listing.objects.get(pk=p_id)
        if request.user == item.seller:
            return render(request, "auctions/item.html",{
                "item":item,
                "msg":"Seller cannot place a bid"
            })
        bid_item = Bid(item=item, user = request.user , bid = bid_price)
        bid_item.save()
        bid = Bid.objects.filter(item = item)
    return render(request,"auctions/item.html",{
        "item":item,
        "msg":"Bid Placed",
        "bid":bid.order_by('-bid')[0]
    })
