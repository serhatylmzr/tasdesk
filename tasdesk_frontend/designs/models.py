from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Design(models.Model):
    user = models.ForeignKey('accounts.User', verbose_name='Kullanıcı',related_name="designs", on_delete=False)
    category = models.ForeignKey('home.Categories', verbose_name='Kategori', on_delete=False, null=True)
    design_title = models.CharField(max_length=120, verbose_name='Tasarım Başlığı')
    design_content = models.TextField(verbose_name='Tasarım İçeriği')
    publishing_date = models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True)
    design_image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130,)
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField('accounts.User', blank=True, related_name="design_likes")
    def __str__(self):
        return self.design_title

    def get_absolute_url(self):
        return reverse('design:detail', kwargs={'slug': self.slug})
        #return "/post/{}".format(self.id)
    def get_create_url(self):
        return reverse('design:create')
    def get_update_url(self):
        return reverse('design:update', kwargs={'slug': self.slug})
    def get_delete_url(self):
        return reverse('design:delete', kwargs={'slug': self.slug})
    def get_unique_slug(self):
        slug = slugify(self.design_title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Design.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug


    def total_likes(self):
        return self.likes.count()
    def class_name(self):
        return self.__class__.__name__

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Design, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publishing_date', 'id']

class DesignComment(models.Model):
    design = models.ForeignKey('designs.Design', verbose_name="Tasarım",related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', verbose_name='Kullanıcı', on_delete=False)
    comment_content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)

class DesignView(models.Model):
    design = models.ForeignKey('designs.Design', verbose_name="Tasarım", related_name='views', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40,null=True)
    session = models.CharField(max_length=40, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
