from django.forms import ModelForm, Textarea, TextInput, IntegerField
from django import forms
from .models import Listing, User, Comments, Bids


class ListingForm(ModelForm):
    title = forms.CharField(max_length=64)
    content = forms.Textarea(attrs={'cols': 40, 'rows': 10})
    image = forms.CharField(required=False)
    price = forms.IntegerField()
    class Meta:
        model = Listing
        fields = ["title", "content", "image", "price"]


class CommentForm(ModelForm):
    comment = forms.Textarea(attrs={'cols':40, 'rows':10})
    class Meta:
        model = Comments
        fields = ['comment']


class Bidform(ModelForm):
    bid = forms.IntegerField()

    class Meta:
        model = Bids
        fields = ['bid']