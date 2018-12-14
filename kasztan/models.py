from django.db import models
from django.contrib.auth.models import User

class Picture(models.Model):
   name = models.CharField(max_length=128)
   description = models.TextField(null = True)
   date = models.DateField(auto_now_add=True)
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   picture = models.FileField(upload_to='pictures/')
   likes = models.IntegerField(default=0)
class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now_add=True)
    comment_picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1024)


class FileUpload(models.Model):

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    file = models.FileField()

    def __str__(self):
        return self.title