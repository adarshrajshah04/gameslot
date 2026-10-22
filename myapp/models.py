from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Profile model
class Profile(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    profile_image = models.ImageField(upload_to="profiles/",blank=False,null=False)

    age = models.IntegerField(blank=False,null=False)
    
    gender=models.CharField(max_length=10,blank=False,null=False)

    def __str__(self):
        return self.user.username
    
