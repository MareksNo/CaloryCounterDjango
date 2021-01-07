from django.utils import timezone
from django.contrib.auth import get_user_model
from videos.validators import validate_file_extension

from django.db import models

User = get_user_model()


class Video(models.Model):
    file = models.FileField(upload_to='videos/', null=True, verbose_name="Video", validators=[validate_file_extension])
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Title', default=timezone.now())
    description = models.TextField(max_length=1000, verbose_name='Video Description', default='')

    def __repr__(self):
        return f'User {self.user.username} created a video "{self.title}"'

    def __str__(self):
        return f'{self.title} by {self.user.username}'
