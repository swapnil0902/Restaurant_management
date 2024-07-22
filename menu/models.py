from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class menuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

@receiver(post_save, sender=Restaurant)
def update_restaurant_fields(sender, instance, created, **kwargs):
    if created:
        instance.owner = instance.owner
        instance.email = instance.owner.email
        instance.save()