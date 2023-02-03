from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    image = models.ImageField(upload_to="images")