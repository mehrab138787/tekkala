
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Game(models.Model):
    category = models.ForeignKey(Category, related_name='games', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration in minutes")
    available_slots = models.IntegerField(default=0)
    image = models.ImageField(upload_to='game_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Reservation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    reserved_by = models.CharField(max_length=255)
    reserved_on = models.DateTimeField(auto_now_add=True)
    reservation_date = models.DateTimeField()
    num_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')

    def __str__(self):
        return f"Reservation for {self.game.title} on {self.reservation_date} by {self.reserved_by}"
