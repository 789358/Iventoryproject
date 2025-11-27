from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)  # 追加
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
