from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Categories(models.Model):
    category_title = models.CharField(max_length=100, verbose_name='Kategori Başlığı')
    category_content = models.TextField( verbose_name='Kategori Açıklaması', null=True)
    publishing_date = models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True)