from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class video(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    video=models.FileField(upload_to='videos', max_length=100)

