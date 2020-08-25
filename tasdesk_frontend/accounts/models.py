from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   is_designer = models.BooleanField(default=True)
   is_admin = models.BooleanField(default= False)
   # you can add more fields here.

class User_Details(models.Model):

   user = models.ForeignKey("User", verbose_name="Kullanici Adi",related_name="user_detail", on_delete=models.CASCADE)

   graduations = models.TextField(verbose_name="Egitim Bilgileri")
   experiences = models.TextField(verbose_name="Deneyimler")
   skills = models.TextField(verbose_name="Yetenekler")
   location = models.TextField(verbose_name="Lokasyon")
   about = models.TextField(verbose_name="Hakkinda")
   user_profile_image = models.ImageField(null=True, blank=True,verbose_name="Profil Fotografi")
   user_job = models.CharField(max_length=75,verbose_name="Meslek")
   followers = models.IntegerField(default=0)
   followed = models.IntegerField(default=0)

   def get_user_detail(self):
      return User_Details.objects.get(user_id=self.user_id)

class User_Messages(models.Model):

   message_id = models.AutoField(primary_key=True)
   user_id = models.ForeignKey("User", verbose_name="Kullanici Adi",on_delete=False)
   message_title = models.CharField(max_length=100, verbose_name="Mesaj Basligi")
   message_content = models.TextField(verbose_name="Mesaj Icerigi")
   #target_userID = models.ForeignKey()

class User_Reviews(models.Model):
   review_id = models.AutoField(primary_key=True)
   user_id = models.ForeignKey("User",verbose_name="Kullanici Adi",on_delete=False)
   #commenter_id = models.ForeignKey()
   comment = models.TextField(verbose_name="Gorus")



