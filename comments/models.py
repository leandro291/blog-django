from django.db import models
from django.db.models import ForeignKey, CASCADE

from users.models import User
from posts.models import Post

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = ForeignKey(
        User,
        on_delete=CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=CASCADE,
    )

    def __str__(self):
        return f"{self.user} - {self.post}"

    class Meta:
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
