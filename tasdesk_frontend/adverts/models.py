from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Advert(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name='Kullanıcı', related_name="adverts", on_delete=False)
    category = models.ForeignKey('home.Categories', verbose_name='Kategori', on_delete=False, null=True)
    advert_title = models.CharField(max_length=120, verbose_name='İlan Başlığı')
    advert_content = models.TextField(verbose_name='İlan İçeriği')
    publishing_date = models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True)
    advert_image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField('accounts.User', blank=True, related_name="advert_likes")
    def __str__(self):
        return self.advert_title

    def get_absolute_url(self):
        return reverse('advert:detail', kwargs={'slug': self.slug})
        #return "/post/{}".format(self.id)
    def get_create_url(self):
        return reverse('advert:create')
    def get_update_url(self):
        return reverse('advert:update', kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('advert:delete', kwargs={'slug': self.slug})
    def get_unique_slug(self):
        slug = slugify(self.advert_title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Advert.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug


    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Advert, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publishing_date', 'id']

class AdvertComment(models.Model):
    advert = models.ForeignKey('adverts.Advert', verbose_name="İlan",related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', verbose_name='Kullanıcı', on_delete=False)
    comment_content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)

class AdvertView(models.Model):
    advert = models.ForeignKey('adverts.Advert',verbose_name="İlan", related_name='views', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40, null=True)
    session = models.CharField(max_length=40,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
