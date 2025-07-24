
from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='tweets/', blank=True, null=True)

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}..."
