from random import choices
from django.forms import ModelForm, Textarea, TextInput, IntegerField
from django import forms
from .models import Listing, User, Comments, Bids


class ListingForm(ModelForm):

    class Meta:
        model = Listing
        fields = ["title", "content", "image", "price", "category"]


class CommentForm(ModelForm):
    #comment = forms.Textarea(attrs={'cols':40, 'rows':10})
    class Meta:
        model = Comments
        fields = ['comment']


class Bidform(ModelForm):
    #bid = forms.IntegerField()

    class Meta:
        model = Bids
        fields = ['bid']