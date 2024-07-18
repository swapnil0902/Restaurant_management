from django.db import models
from menu.models import menuItem
from customer.models import Customer

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    menu_id = models.ForeignKey(menuItem, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.menu_name = self.menu_id.name
        if self.quantity is not None and self.rate is not None:
            self.total_price = self.quantity * self.rate
        super(Order, self).save(*args, **kwargs)
        

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} ordered {self.quantity} of {self.menu_name}"
