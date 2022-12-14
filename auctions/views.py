from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comments, Bids, Categories, Wishlist
from .forms import ListingForm, CommentForm, Bidform


# Incative listings page
def inactive(request):
    listings = Listing.objects.order_by('-pk')
    return render(request, "auctions/inactive.html",{
        "listings":listings,

    })

def index(request):
    listings = Listing.objects.order_by('-pk')
    return render(request, "auctions/index.html",{
        "listings":listings,

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
def create(request):
    invalid_price_message = "Invalid Price"
    try:
        if request.method == "POST":
            form = ListingForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

                return HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/create.html",{
            "form":ListingForm()
        })
    except IntegrityError:
        return render(request, "auctions/create.html",{
            "form":ListingForm(),
            "message": invalid_price_message
        })




def listing(request, listing_id):
   
    listing = Listing.objects.get(id = listing_id)
    bids = Bids.objects.filter(post = listing).order_by('-bid')
    comments = Comments.objects.filter(post = listing).order_by('-time')


    invalid_bid_message = "The bid must be higher or equal to it's starting bid!"
    checkbox = ""

    if len(bids) > 0:
        active_bid = bids[0]
    else:
        active_bid = None

    # Variable to access the owner of the listing
    IS_USER = False
    if request.user == listing.user:
            IS_USER = True
    if request.user.is_authenticated:
        # Adding item to the wishlist
        add_wishlist = request.POST.get("wishlist")
        if add_wishlist == "Add To Wishlist":
            add_wishlist = Wishlist.objects.update_or_create(user=request.user, post=listing)
            return HttpResponseRedirect(reverse('index'))
        # CLOSING THE LISTING
        if IS_USER:
            checkbox = request.POST.get("close")
            if checkbox == "Close":
                listing.active = False
                listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comment_form":CommentForm(),
                "comments": comments,
                "bids": bids,
                "bid_form": Bidform(),
                "IS_USER": IS_USER,
                "active_bid": active_bid,

            })  
        
        
        if (request.method == "POST"):  
            #comment form and bidding form
            comment_form = CommentForm(request.POST)     
            bid_form = Bidform(request.POST)

            if bid_form.is_valid():
                bid_list = []
                try:
                    
                    instance = bid_form.save(commit=False)
                    instance.user = request.user
                    if instance.bid < listing.price:
                        raise ValidationError("Price isn't valid")
                    for bid in bids:
                        bid_list.append(bid)
                        if instance.bid <= bid.bid:
                            invalid_bid_message = "Bid must be higher than any other bid!"
                            raise ValidationError("Bid must be higher than older bids")
                    instance.post = listing
                    instance.save()
                    return HttpResponseRedirect(reverse('index'))
                    
                
                except ValidationError:
                    return render(request, "auctions/listing.html", {
                        "message": invalid_bid_message,
                        "listing": listing,
                        "comment_form":CommentForm(),
                        "comments": comments,
                        "bids": bids,
                        "bid_form": Bidform(),
                        "IS_USER": IS_USER,
                        "active_bid":  active_bid,
                    })
            # IF COMMENT FORM'S VALID
            if comment_form.is_valid(): 
                instance = comment_form.save(commit=False)
                instance.user = request.user
                instance.post = listing
                instance.save()
                return HttpResponseRedirect(reverse('index'))

        return render(request, "auctions/listing.html",{
        "listing": listing,
        "comment_form":CommentForm(),
        "comments": comments,
        "bids": bids,
        "bid_form": Bidform(),
        "active_bid":  active_bid,
    })

    else: #if user's not logged in
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "comments": comments,
            "bids": bids,
            "active_bid": active_bid,
           

        })


def categories(request):
    categories = Categories.objects.all().distinct().order_by('category')
    return render(request, "auctions/categories.html",{
        "categories": categories,

    })

def category(request, category_id):
    category = Categories.objects.get(id = category_id)
    listings = Listing.objects.filter(category = category)

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,

    })

def wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    return render(request, "auctions/wishlist.html", {
        "wishlist": wishlist,
        "user": request.user,

    })