from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comments, Bids
from .forms import ListingForm, CommentForm, Bidform



def index(request):
    listing_list = Listing.objects.order_by('-pk')
    return render(request, "auctions/index.html",{
        "listings":listing_list,

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
    success_message = "Successfully Posted Listing"
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
    comments = Comments.objects.filter(post = listing)
    
    # CHECK IF BID IS VALID AND APEND THE BID LIST
    bid_list=[]
    for bid in bids:
        if bid.bid > listing.price:
            bid_list.append(bid)
    #BIGGEST BID SO FAR
    active_bid = bid_list[0]

    
    if request.user.is_authenticated:
        
        if request.method == "POST":  
            
            #comment form and bidding form
            comment_form = CommentForm(request.POST)     
            bid_form = Bidform(request.POST)
            
            
            if bid_form.is_valid():
                # ADD BID VALDIATION HERE, CHANGE THE CODE YOU IMPLEMENTED
                instance = bid_form.save(commit=False)
                instance.user = request.user
                instance.post = listing
                instance.save()
                return HttpResponseRedirect(reverse('index'))


            if comment_form.is_valid(): 
                instance = comment_form.save(commit=False)
                instance.user = request.user
                instance.post = listing
                instance.save()
                return HttpResponseRedirect(reverse('index'))

        return render(request, "auctions/listing.html",{
        "id":listing_id,
        "listing": listing,
        "comment_form":CommentForm(),
        "comments": comments,
        "bids": bid_list,
        #"bids": bids,
        "bid_form": Bidform(),
        "active_bid": active_bid
        
    })

    else: #if user's not logged in
        return render(request, "auctions/listing.html",{
            "id":listing_id,
            "listing": listing,
            "comments": comments,
            "bids": bids,
        })
