from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=200) # ชื่อการ์ด
    series = models.CharField(max_length=200) # ชุดการ์ด
    price = models.DecimalField(max_digits=10, decimal_places=2) # ราคา
    rarity = models.CharField(max_length=10) # ระดับความหายาก (RRR, RR, SP)
    clan = models.CharField(max_length=100) # แคลน/เนชั่น
    stock = models.IntegerField(default=0) # จำนวนสินค้าในสต็อก
    image = models.ImageField(upload_to='cards/') # รูปภาพการ์ด
    
    def __str__(self):
        return self.name