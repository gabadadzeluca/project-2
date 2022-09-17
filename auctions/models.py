from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass




class Listing(models.Model):


    title = models.CharField('Title',max_length=64)
    content = models.TextField('Content',max_length=500)
    image = models.CharField(blank=True, max_length=400)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    price = models.PositiveIntegerField('Price')
    time = models.DateTimeField(auto_now=True)
    active = models.BooleanField('active',default=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, default= "ELSE")


    
    def __str__(self):
        return f"{self.title} | Posted by: {self.user}" 

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"


class Comments(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.TextField('Comment', max_length=400)
    time = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.user} commented on {self.post.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

class Bids(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    bid = models.PositiveIntegerField(default=None,)
    time = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"{self.user} has put a {self.bid}$ bid for {self.post.title}"


class Categories(models.Model):

    CATEGORY_CHOICES = [
        ("ELSE", "Else"),
        ("ACCESORIES", "Accessories"),
        ("SPORT", "Sports"),
        ("CLOTHING", "Clothing"),
        ("ELECTRONICS", "Electronics"),
        ("ART", "Art"),
        ("MOVIES-AND-TV", "Movies and Television"),
        ("TOYS-AND-GAMES", "Toys and Games"),
        ("VIDEO-GAMES", "Video Games"),
        ("HOME-AND-KITCHEN", "Home and Kitchen"),
        ("SELF-CARE", "Self Care"),
        ("BOOKS", "Books"),
    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default= CATEGORY_CHOICES[0][0],
        unique=True,

    )

    class Meta:
        ordering= ('category',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.category}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} added {self.post} to wishlist"