from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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

def listing(request, id):
    comment_list = Comments.objects.all()
    listing_list = Listing.objects.all()
    bid_list = Bids.objects.all()
    if request.user.is_authenticated:

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            form_bid = Bidform(request.POST)
            if form_bid.is_valid():
                post = get_object_or_404(Listing, pk = id)
                form_bid.instance.user = request.user
                form_bid.instance.post = post
                form_bid.save()
           
            if comment_form.is_valid():
                post = get_object_or_404(Listing, pk=id)
                comment_form.instance.user = request.user
                comment_form.instance.post = post
                comment_form.save()
                
            return HttpResponseRedirect(reverse('index'))
        return render(request, "auctions/listing.html",{
            "listing_list": listing_list,
            "id": id,
            "comment_form" : CommentForm(),
            "comment_list": comment_list,
            "form_bid": Bidform(),
            "bid_list": bid_list,
            

        })
    else:
        return render(request, "auctions/listing.html",{
            "listing_list": listing_list,
            "id" : id,
            "comment_list": comment_list,

        })
