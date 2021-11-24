from django.db import models
from datetime import datetime
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField


# Create your models here.
class Categories(models.TextChoices):
    ROCK = 'rock'
    CLASIC = 'clasic'
    JAZZ = 'jazz'
    POP = 'pop'


class Songs(models.Model):
    song = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50, choices=Categories.choices, default=Categories.ROCK)
    thumbnail = models.ImageField(upload_to='photos/%Y/%m/%d/')
    content = models.TextField()
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads_owner')
    urlvideo = EmbedVideoField(null=True)
    #comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='comments_owned')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_ads')

    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.song

class Fav(models.Model) :
    ad = models.ForeignKey(Songs, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.ad.title[:10])