from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField('Title',max_length=64)
    content = models.TextField('Content',max_length=500)
    image = models.CharField(blank=True, max_length=400)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    price = models.IntegerField('Price')
    # ADD INVISIBLE ACTIVE FIELD TO KNOW IF THE LISTING IS ACTIVE 
    def __str__(self):
        return f"{self.title} | Posted by: {self.user}" 

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"


class Comments(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.TextField('Comment', max_length=400)
    
    def __str__(self):
        return f"{self.user}:  {self.comment}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Bids(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    bid = models.IntegerField()
    #starting_bid = models.ForeignKey(Listing, on_delete=models.CASCADE)
    #CHECK BID
    """def checkbid(self,bid):
        self.bid = bid
        self.final_bid = Bids.final_bid
        if self.bid < self.final_bid:
            return False
    """
    class Meta:
        verbose_name = "Bid"
        verbose_name_plural = "Bids"
    def __str__(self):
        return f"{self.user} has put a {self.bid}$ bid for {self.post.title}"