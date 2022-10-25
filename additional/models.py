from django.db import models


class Seo(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    keywords = models.TextField(verbose_name='Keywords')


class Gallery(models.Model):
    name = models.CharField(max_length=200)


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='gallery/')
