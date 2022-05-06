import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User, Auction, Bid, Comment, Wishlist
from .forms import AddNewAuction, AddNewBid, AddNewComment


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Auction.objects.filter(active=True).only("name", "description", "current_bid", "image")
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


@login_required
def add_auction(request):
    if request.method == 'POST':
        form = AddNewAuction(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/new_auction.html", {
        "form": form
    })
    
    return render(request, "auctions/new_auction.html", {
        "form": AddNewAuction()
    })


def auction_page(request, lot_id):
    lot = Auction.objects.get(id=lot_id)

    in_wishlist = False
    if Wishlist.objects.filter(user=request.user, auction=lot_id):
        in_wishlist = True

    comments = Comment.objects.filter(auction=lot_id)
    
    context = {
        "lot": lot,
        "comments": comments,
        "in_wishlist": in_wishlist,
        "biddingform": AddNewBid(),
        "commentingform": AddNewComment()
    }

    if request.method == 'POST':

        if 'add-to-wishlist-btn' in request.POST:
            Wishlist.objects.create(user=request.user, auction=lot)
            return HttpResponseRedirect(reverse("auction_page", args=[lot_id, ]))

        if 'remove-from-wishlist-btn' in request.POST:
            Wishlist.objects.get(user=request.user, auction=lot_id).delete()
            return HttpResponseRedirect(reverse("auction_page", args=[lot_id, ]))

        if 'add-comment-btn' in request.POST:
            comment_form = AddNewComment(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.auction = lot
                comment.save()
                return HttpResponseRedirect(reverse("auction_page", args=[lot_id, ]))

        if lot.user == request.user:
            if 'close-auction-btn' in request.POST:
                if Bid.objects.filter(auction=lot_id):
                    lot.winner = Bid.objects.filter(auction=lot_id).latest('added').user

                lot.active = False
                lot.save(update_fields=['active', 'winner'])
                return HttpResponseRedirect(reverse("auction_page", args=[lot_id, ]))
            else:
                return render(request, "auctions/auction_page.html", context)
        else:
            bid_form = AddNewBid(request.POST)
            if bid_form.is_valid():
                new_bid = bid_form.cleaned_data["bid"]
                if new_bid > lot.current_bid:
                    lot.current_bid = new_bid
                    lot.save(update_fields=['current_bid'])
                    
                    bid = bid_form.save(commit=False)
                    bid.user = request.user
                    bid.auction = lot
                    bid.save()
                    return HttpResponseRedirect(reverse("auction_page", args=[lot_id, ]))
                else:
                    messages.add_message(request, messages.ERROR, message='Your bid must be higher than current bid!')
            else:
                return render(request, "auctions/auction_page.html", context)
    
    if lot.active == False and request.user == lot.winner:
        messages.add_message(request, messages.INFO, message='Congratulations! You are winner! Contact auction owner for details.')
    
    return render(request, "auctions/auction_page.html", context)


@login_required
def wishlist(request):
    auctions_id = Wishlist.objects.filter(user=request.user).values_list('auction', flat=True)
    wishlist_listings = Auction.objects.filter(id__in=auctions_id).only("name", "description", "current_bid", "image")

    if request.method == 'POST':
        lot_id = request.POST.get('lot_id')
        Wishlist.objects.get(user=request.user, auction=lot_id).delete()
        return HttpResponseRedirect(reverse("wishlist_page"))

    return render(request, "auctions/wishlist_page.html", {
        "wishlist_listings": wishlist_listings
    })

        
def categories(request):
    categories = Auction.AUCTION_CATEGORY_CHOICES
    return render(request, "auctions/categories_page.html", {
        "categories": categories
    })


def category_listing(request, cat_name, cat_id):

    listing = Auction.objects.filter(category=cat_id, active=True).only("name", "description", "current_bid", "image")
    
    return render(request, "auctions/category_page.html", {
        "category_listing": listing,
        "category_name": cat_name
    })
