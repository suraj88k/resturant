from django.db import models

# Create your models here.
class Category(models.Model):
    title= models.CharField(max_length=100)

    def _str_(self):
        return self.title

class Momo(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    def _str_(self):
        return self.name



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def _str_(self):
        return self.email