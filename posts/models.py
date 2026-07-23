from django.db import models
from django.db.models import CASCADE, PROTECT
from users.models import User
from categories.models import Category

# Create your models here.
class Post(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    miniature = models.ImageField(upload_to='posts/images/')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=PROTECT,
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'

