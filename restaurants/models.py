from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.restaurant_name} - {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=255)
    security_answer_1 = models.CharField(max_length=255)

    security_question_2 = models.CharField(max_length=255)
    security_answer_2 = models.CharField(max_length=255)

    security_question_3 = models.CharField(max_length=255)
    security_answer_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username