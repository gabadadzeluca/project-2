from email.policy import default
from django.forms import ModelForm
from django import forms
from .models import Listing, User, Comments, Bids, Categories


class ListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ["title", "content", "image", "price", "category"]


class CommentForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']


class Bidform(ModelForm):

    class Meta:
        model = Bids
        fields = ['bid']