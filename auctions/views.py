
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Watchlist
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
        "watchlist":watchlist_items.auctions.all()
    })

def item(request,p_id):
    item = Listing.objects.get(pk = p_id)
    return render(request,"auctions/item.html",{
        "item":item,
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