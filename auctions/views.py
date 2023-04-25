from .models import User, Category, Listing, Comment, Bid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from faker import Faker


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Check if user logged in with demo user
        if "demo_user" in request.POST:
            fake = Faker()

            # Generate random user info
            username = fake.user_name()
            email = fake.email()
            password = fake.password()

            # Register demo user
            demo_user = User.objects.create_user(username, email, password)
            demo_user.save()

            # Log user in
            login(request, demo_user)

            # Redirect user to home page
            return HttpResponseRedirect(reverse("index"))

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    if request.method == "POST":
        # Get form information
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST.get("starting_bid", False)
        categories = Category.objects.filter(pk__in=request.POST.getlist("categories"))
        image = request.POST["image"]

        # Save listing
        listing = Listing(user=user, title=title, description=description, image=image, price=starting_bid)
        listing.save()
        listing.categories.set(categories)

        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

    categories = Category.objects.all()
    return render(request, "auctions/new_listing.html", {"categories": categories})


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    if request.method == "POST":
        user = request.user

        # Watchlist
        if request.POST["form"] == "watchlist":
            if listing in user.watchlist.all():
                user.watchlist.remove(listing)
            else:
                user.watchlist.add(listing)

        # Close Auction
        if request.POST["form"] == "close_auction":
            listing.closed = True
            listing.save()

        # Bid
        if request.POST["form"] == "bid":
            value = request.POST["value"]

            # Validate bid
            if (listing.bids.all() and float(value) <= float(listing.bids.last().value)) or (
                float(value) < float(listing.price)
            ):
                print("There is a bid, and value is less or equal to current price.")
                return render(
                    request,
                    "auctions/listing.html",
                    {"listing": listing, "message": "Bid must be higher than current price."},
                )

            # Save bid
            bid = Bid(user=user, listing=listing, value=value)
            bid.save()

        # Comment
        if request.POST["form"] == "comment":
            text = request.POST["text"]
            comment = Comment(user=user, listing=listing, text=text)
            comment.save()

    return render(request, "auctions/listing.html", {"listing": listing})


@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html")


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, url_name):
    category = Category.objects.get(url_name=url_name)
    return render(request, "auctions/category.html", {"category": category})
