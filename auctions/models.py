from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField('Title',max_length=64)
    content = models.TextField('Content',max_length=500)
    image = models.CharField(blank=True, max_length=300)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    price = models.IntegerField('Price')

    def __str__(self):
        return f"Title: {self.title} Posted by: {self.user}" 

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
