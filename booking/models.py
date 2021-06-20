from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Table(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    image = models.ImageField(upload_to='tables/')
    description = models.TextField()
    is_booked = models.BooleanField(default=False)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='bookings')
    phone_number = models.CharField(max_length=10)
    activation_code = models.CharField(max_length=8, blank=True)
    # datetime = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        if Booking.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save(update_fields=['activation_code'])


