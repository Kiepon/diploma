from django.db import models

# Create your models here.

def rating():
    return {i: i for i in range(0, 11)}

class Hotel(models.Model):
    title = models.CharField(max_length=45)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    rating = models.IntegerField(choices=rating, default=0)
    
    def __str__(self):
        return self.title


class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    
    def __str__(self):
        return self.name    

class Room(models.Model):
    hotel = models.ForeignKey("Hotel", related_name='rooms', on_delete=models.CASCADE)  
    room_type = models.ForeignKey("RoomType", related_name='rooms', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.room_type.name
    
    def price_with_RUB(self):
        return f'{self.price} Р.'  


      

    

