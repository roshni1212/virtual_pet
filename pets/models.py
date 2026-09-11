from django.db import models


class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('rabbit', 'Rabbit'),
    ]

    name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=20)

    hunger = models.IntegerField(default=70)
    happiness = models.IntegerField(default=70)
    energy = models.IntegerField(default=70)
    coins = models.IntegerField(default=100)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ShopItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    hunger_boost = models.IntegerField(default=0)
    happiness_boost = models.IntegerField(default=0)
    energy_boost = models.IntegerField(default=0)

    def __str__(self):
        return self.name